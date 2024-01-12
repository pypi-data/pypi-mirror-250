# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

import inspect
from collections import defaultdict
from functools import wraps
from typing import (
    Iterable,
    List,
)

from qctrlcommons.node.base import Node
from qctrlcommons.node.wrapper import Operation

from . import node_data

# pylint:disable=unused-wildcard-import, wildcard-import
from .arithmetic_binary import *
from .arithmetic_unary import *
from .attribute import *
from .differentiation import *
from .documentation import create_documentation_sections
from .filter_function import *
from .fock_space import *
from .infidelity import *
from .ms import *
from .optimization import *
from .oqs import *
from .pwc import *
from .sparse import *
from .stf import *
from .stochastic import *
from .tensor import *

# Registry of all types created by operations.
TYPE_REGISTRY = [
    node_data.ConvolutionKernel,
    node_data.FilterFunction,
    node_data.Pwc,
    node_data.SparsePwc,
    node_data.Stf,
    node_data.Target,
    node_data.Tensor,
]


class _LegacyNodeRegistry:
    """
    Register all the imported Node type class.
    """

    def __init__(self, nodes):
        self._nodes = {}
        self._module_map = defaultdict(list)

        for node in nodes:
            if node.name in self._nodes:
                raise ValueError(f"duplicate name: {node.name}")
            module = node.__module__
            submodule = module.split(".")[-1]
            self._module_map[submodule].append(node.name)
            self._nodes[node.name] = node

    def get_node_cls(self, name: str) -> Node.__class__:
        """
        Get the Node class by name from the operation.

        Parameters
        ----------
        name : str
            the requested name.

        Returns
        -------
        Node
            the match Node class.

        Raises
        ------
        KeyError
            if the node doesn't exist in registry.
        """
        if name not in self._nodes:
            raise KeyError(f"unknown node: {name}")

        return self._nodes[name]

    def as_list(self, exclude_node_types=None) -> List:
        """
        Convert the nodes to a list.

        This method allows exclusion of certain nodes, if not all nodes are needed.

        Parameters
        ----------
        exclude_node_types : List[string]
            The node types to exclude from the list. (Default value = None)

        Returns
        -------
        List
            list of Node classes.

        Raises
        ------
        KeyError
            if `excluded_node` does not exist in registry.
        """

        if exclude_node_types is not None:
            exclusion_list = []
            for excluded_node in exclude_node_types:
                if excluded_node not in self._module_map:
                    raise KeyError(f"unknown excluded node: {excluded_node}")

                exclusion_list.extend(self._module_map[excluded_node])

            list_difference = list(set(list(self._nodes.keys())) - set(exclusion_list))
            node_subset = {key: self._nodes[key] for key in list_difference}
            return list(node_subset.values())

        # TODO order by name?
        return list(self._nodes.values())

    @classmethod
    def load(cls):
        """
        Load all the register Node class.

        Parameters
        ----------
        cls : class
            class object.

        Returns
        -------
        NodeRegistry
            an updated NodeRegistry with all different types of Node class.
        """
        nodes = []

        for obj in globals().values():
            if inspect.isclass(obj) and issubclass(obj, Node) and obj.name is not None:
                nodes.append(obj)

        return cls(nodes)


class _NodeMethod:
    """
    An instance of this class converts the placeholder of the graph method to the actual
    callable. Essentially it looks for the NodeFactory by the graph method name, and then
    handles the data conversion and validation, and adds the node to the graph.

    Note that this class is not expected to be used directly. The single instance
    in this file, `node_method`, should be used to define all graph methods.
    """

    def __init__(self, node_registry: "NodeRegistry"):
        self.node_registry = node_registry

    def __call__(self, func):
        factory = self.node_registry.get_node_factory(func.__name__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Recall the graph method is just a placeholder. We only use it to update the
            metadata of `wrapper`.
            """
            return factory(*args[1:], **kwargs).create_node(args[0])

        wrapper.__doc__ = factory.__doc__
        return wrapper


class NodeRegistry:
    """
    Register all Boulder Opal nodes.
    """

    def __init__(self, legacy_registry: _LegacyNodeRegistry):
        self._legacy_registry = legacy_registry

        self._node_no_gradient = set()
        self._optimization_nodes = set()

        self._node_factories: dict[str, NodeFactory] = {}

        for node in self._legacy_registry.as_list():
            if not node.supports_gradient:
                self._node_no_gradient.add(node.name)
            if node.optimizable_variable:
                self._optimization_nodes.add(node.name)

        for obj in globals().values():
            if (
                inspect.isclass(obj)
                and issubclass(obj, NodeFactory)
                and obj is not NodeFactory
            ):
                self._node_factories[obj.get_node_name()] = obj

    def supports_gradient(self, operation: Operation) -> bool:
        """
        Check if an operation can support gradient.
        """
        return not operation.operation_name in self._node_no_gradient

    def is_optimization_node(self, operation: Operation) -> bool:
        """
        Check if an operation is a basic optimization node.
        """
        return operation.operation_name in self._optimization_nodes

    def get_node_factory(self, name: str) -> NodeFactory:
        """
        Return the node factory by the name.
        """
        factory = self._node_factories.get(name)
        assert factory is not None
        return factory

    @property
    def legacy_registry(self) -> _LegacyNodeRegistry:
        """
        Return the legacy registry.
        """
        return self._legacy_registry

    @property
    def registry(self) -> Iterable[NodeFactory]:
        """
        Get all node factories.
        """
        return self._node_factories.values()


PRIMARY_NODE_REGISTRY = NodeRegistry(_LegacyNodeRegistry.load())

# Primary Node Namespaces.
PRIMARY_NAMESPACE_REGISTRY = [IonsNamespace, RandomNamespace]
PRIMARY_NAMESPACE_DOCS = [IonsNamespaceDoc, RandomNamespaceDoc]

# Prepare primary node documentation categories.
PRIMARY_NODE_DOCUMENTATION_SECTIONS = create_documentation_sections(
    {
        node_cls.name: node_cls.categories
        for node_cls in PRIMARY_NODE_REGISTRY.legacy_registry.as_list()
    }
)
node_method = _NodeMethod(PRIMARY_NODE_REGISTRY)

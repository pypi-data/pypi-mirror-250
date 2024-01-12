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

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import TYPE_CHECKING

import inflection
from attrs import asdict
from qctrlcommons.node.wrapper import Operation

if TYPE_CHECKING:
    from boulderopal._nodes.documentation import Category


class NodeFactory(ABC):
    """
    Interface for a node factory.
    """

    @classmethod
    @abstractmethod
    def get_doc_category(cls) -> list[Category]:
        """
        Return the documentation category for the node.
        """
        raise NotImplementedError

    @classmethod
    def get_node_name(cls) -> str:
        """
        Return the node name.
        """
        return inflection.underscore(cls.__name__)[: -len("_factory")]

    @abstractmethod
    def create_node(self, graph):
        """
        Add the node to the graph.
        """
        raise NotImplementedError

    @property
    def is_optimizable_node(self):
        """
        Indicate if the node corresponds to an optimization operation.
        Defaults to False.
        """
        return False

    def get_operation(self, graph):
        """
        Get the operation from the NodeFactory.
        """
        return Operation(
            graph=graph,
            operation_name=self.get_node_name(),
            optimizable_variable=self.is_optimizable_node,
            **asdict(self),
        )

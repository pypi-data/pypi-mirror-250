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
"""Module for NodeRegistry."""
import inspect
from functools import partial

from boulderopal._nodes.composite import (
    filter_and_resample,
    optimizable_scalar,
    optimizable_signals,
    signals,
    signals_pwc,
    signals_stf,
)
from boulderopal._nodes.composite.namespace import (
    COMPOSITE_ATTR,
    NAMESPACE_ATTR,
)


def _register(modules):
    """
    Collect exposed composite nodes from modules.
    """
    registered = []
    for module in modules:
        for _, member in inspect.getmembers(
            module, predicate=partial(_filter, module_name=module.__name__)
        ):
            registered.append(member)
    return registered


def _filter(member, module_name):
    """
    - Exposed member must be a function.
    - Exposed member must be defined in the module, not imported.
    - Exposed member must not be private.
    """
    return (
        (inspect.isfunction(member) or inspect.isclass(member))
        and member.__module__ == module_name
        and not member.__name__.startswith("_")
        and hasattr(member, COMPOSITE_ATTR)
    )


_composite_registry = _register(
    [
        optimizable_signals,
        filter_and_resample,
        optimizable_scalar,
        signals_pwc,
        signals_stf,
        signals,
    ]
)

# Collect the composite node namespaces.
COMPOSITE_NAMESPACE_REGISTRY = [
    node for node in _composite_registry if hasattr(node, NAMESPACE_ATTR)
]

# Collect the composite nodes that are not in a namespace.
COMPOSITE_NODE_REGISTRY = [
    node for node in _composite_registry if not hasattr(node, NAMESPACE_ATTR)
]

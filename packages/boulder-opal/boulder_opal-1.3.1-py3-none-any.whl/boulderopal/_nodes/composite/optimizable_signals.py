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

from typing import Optional

import numpy as np
from qctrlcommons.preconditions import check_argument

from boulderopal._nodes.composite.namespace import composite_node
from boulderopal._nodes.documentation import Category
from boulderopal._nodes.node_data import Pwc


@composite_node([Category.OPTIMIZATION_VARIABLES])
def real_optimizable_pwc_signal(
    graph: "Graph",
    segment_count: int,
    duration: float,
    maximum: float,
    minimum: float = 0.0,
    initial_values: Optional[np.ndarray | list[np.ndarray]] = None,
    name: Optional[str] = None,
) -> Pwc:
    """
    Create a real optimizable piecewise-constant signal.

    Parameters
    ----------
    graph : Graph
        The graph object where the node will belong.
    segment_count : int
        The number of piecewise-constant segments in the signal.
    duration : float
        The duration of the signal.
    maximum : float
        The upper bound for the signal values.
    minimum : float, optional
        The lower bound for the signal values. Defaults to 0.
    initial_values : np.ndarray or list[np.ndarray] or None, optional
        Initial values for the signal. You can either provide a single array,
        or a list of them. If a list of arrays is used, they must have the same length.
        Defaults to None, meaning the optimizer initializes the variables with random values.
    name : str or None, optional
        The name of the node.

    Returns
    -------
    Pwc
        The optimizable piecewise-constant signal.

    See Also
    --------
    :func:`Graph.complex_optimizable_pwc_signal` :
        Create a complex optimizable `Pwc` signal.
    :func:`Graph.optimization_variable` :
        Create optimization variables, which can be bounded, semi-bounded, or unbounded.
    :func:`Graph.pwc_signal` : Create a piecewise-constant signal.
    """

    if initial_values is not None:
        check_argument(
            np.all(np.isreal(initial_values)),
            "Initial signal values must be real.",
            {"initial_values": initial_values},
        )

    values = graph.optimization_variable(
        count=segment_count,
        lower_bound=minimum,
        upper_bound=maximum,
        initial_values=initial_values,
    )
    return graph.pwc_signal(values=values, duration=duration, name=name)


@composite_node([Category.OPTIMIZATION_VARIABLES])
def complex_optimizable_pwc_signal(
    graph: "Graph",
    segment_count: int,
    duration: float,
    maximum: float,
    initial_values: Optional[np.ndarray | list[np.ndarray]] = None,
    name: Optional[str] = None,
) -> Pwc:
    """
    Create a complex optimizable piecewise-constant signal.

    Parameters
    ----------
    graph : Graph
        The graph object where the node will belong.
    segment_count : int
        The number of segments of the signal.
    duration : float
        The duration of the signal.
    maximum : float
        The upper bound for the modulus of the signal values.
    initial_values : np.ndarray or list[np.ndarray] or None, optional
        Initial values for the signal. You can either provide a single array,
        or a list of them. If a list of arrays is used, they must have the same length.
        Defaults to None, meaning the optimizer initializes the variables with random values.
    name : str or None, optional
        The name of the node.

    Returns
    -------
    Pwc
        The optimizable piecewise-constant signal.

    See Also
    --------
    :func:`Graph.real_optimizable_pwc_signal` :
        Create a real optimizable `Pwc` signal.
    :func:`Graph.complex_pwc_signal` :
        Create a complex piecewise-constant signal from moduli and phases.
    :func:`Graph.optimization_variable` :
        Create optimization variables, which can be bounded, semi-bounded, or unbounded.
    :func:`Graph.pwc_signal` : Create a piecewise-constant signal.

    Notes
    -----
    Note that this function sets limits to the modulus of the signal.

    If you want to set (different) limits to the real and imaginary parts instead,
    consider using `graph.real_optimizable_signal` to create signals for the
    real and imaginary parts, which you can pass to `graph.complex_value`.
    """

    initial_moduli: Optional[list[np.ndarray] | np.ndarray] = None
    initial_phases: Optional[list[np.ndarray] | np.ndarray] = None

    if initial_values is not None:
        if isinstance(initial_values, list):
            initial_moduli = list(np.absolute(initial_values))
            initial_phases = list(np.angle(initial_values))
        else:
            initial_moduli = np.absolute(initial_values)
            initial_phases = np.angle(initial_values)

    moduli = graph.optimization_variable(
        count=segment_count,
        lower_bound=0.0,
        upper_bound=maximum,
        initial_values=initial_moduli,
    )
    phases = graph.optimization_variable(
        count=segment_count,
        lower_bound=-np.pi,
        upper_bound=np.pi,
        is_lower_unbounded=True,
        is_upper_unbounded=True,
        initial_values=initial_phases,
    )
    return graph.complex_pwc_signal(
        moduli=moduli, phases=phases, duration=duration, name=name
    )

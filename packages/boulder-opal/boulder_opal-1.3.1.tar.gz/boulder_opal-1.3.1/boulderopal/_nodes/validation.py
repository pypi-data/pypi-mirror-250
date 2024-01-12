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

import numpy as np

from boulderopal._nodes.node_data import Tensor
from boulderopal._validation.basic import ArrayT


class ArrayLike:
    """
    Perform type check and conversion for array like input.
    """

    def __init__(self, name: str):
        self._name = name

    def __call__(self, value: np.ndarray | Tensor):
        if isinstance(value, Tensor):
            return value
        try:
            return ArrayT.NUMERIC(self._name)(value)
        except TypeError as e:
            raise TypeError(
                f"{self._name} must either be a NumPy array or Tensor."
            ) from e

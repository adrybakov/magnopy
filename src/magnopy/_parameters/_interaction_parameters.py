# ================================== LICENSE ===================================
# Magnopy - Python package for magnons.
#
# Copyright (C) 2023 Magnopy Team
#
# e-mail: anry@uv.es, web: magnopy.org
#
# This program is free software: you  can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the  Free Software
# Foundation,  either  version 3  of the License,  or (at your option) any later
# version.
#
# This program is distributed in the  hope  that it will be useful,  but WITHOUT
# ANY WARRANTY;  without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the  GNU General Public License  along with
# this program.  If not, see <https://www.gnu.org/licenses/>.
# ================================ END LICENSE =================================

import numpy as np
from copy import deepcopy


def _get_specs(nus, alphas):
    n = len(alphas)

    nus = tuple(map(tuple, nus))
    alphas = tuple(alphas)

    combined = [(alphas[i], *nus[i]) for i in range(n)]

    if n == 1:
        p_n = 1
    elif n == 2:
        if combined[0] == combined[1]:
            p_n = 1
        else:
            p_n = 2
    elif n == 3:
        if combined[0] == combined[1] == combined[2]:
            p_n = 1
        elif (
            combined[0] == combined[1]
            or combined[0] == combined[2]
            or combined[1] == combined[2]
        ):
            p_n = 2
        else:
            p_n = 3
    elif n == 4:
        if combined[0] == combined[1] == combined[2] == combined[3]:
            p_n = 1
        elif (
            combined[0] == combined[1] == combined[2]
            or combined[0] == combined[1] == combined[3]
            or combined[0] == combined[2] == combined[3]
            or combined[1] == combined[2] == combined[3]
        ):
            p_n = 2
        elif (
            (combined[0] == combined[1] and combined[2] == combined[3])
            or (combined[0] == combined[2] and combined[1] == combined[3])
            or (combined[0] == combined[3] and combined[1] == combined[2])
        ):
            p_n = 3
        elif (
            combined[0] == combined[1]
            or combined[0] == combined[2]
            or combined[0] == combined[3]
            or combined[1] == combined[2]
            or combined[1] == combined[3]
            or combined[2] == combined[3]
        ):
            p_n = 4
        else:
            p_n = 5

    if nus[0] != (0, 0, 0):
        new_nus = []
        for site in range(n):
            new_nus.append(tuple([nus[site][_] - nus[0][_] for _ in range(3)]))

        nus = tuple(new_nus)

    return (n, p_n, nus[1:], alphas)


class _InteractionParameters:
    """
    Interaction parameters of spin Hamiltonian.

    This class assumes:

    * Order of parameters by the specs = [n, p_n, nus, alphas].
    * Only one parameter for each set of alphas & nus.
    * That shape of the parameter's tensor matches n.
    * That n and/or p_n are correct for corresponding alphas and nus.
    * Keeps track of positions of parameters with different n and p_n in the container via
      ``_slices`` attribute.
    """

    def __init__(self):
        # Elements of the container are
        # [(n, p_n, (nu_2, ..., nu_n), (alpha_1, ..., alpha_n)), parameter]
        self._container = []
        self._slices = {
            # (n, p_n): [start, length]
            (1, 1): [0, 0],
            (2, 1): [0, 0],
            (2, 2): [0, 0],
            (3, 1): [0, 0],
            (3, 2): [0, 0],
            (3, 3): [0, 0],
            (4, 1): [0, 0],
            (4, 2): [0, 0],
            (4, 3): [0, 0],
            (4, 4): [0, 0],
            (4, 5): [0, 0],
        }

    def _get_index(self, specs):
        """
        Get an index of an interaction parameter in the container if it exists.

        Parameters
        ----------
        specs : tuple
            Tuple with the special structure tha uniquely defines the spin operators
            associated with the interaction parameter.

            .. code-block:: python

                (n, p_n, (nu_2, ..., nu_n), (alpha_1, ..., alpha_n))

        Returns
        -------
        index : int
            Index of the interaction parameter in the container if it exists, -1 otherwise.
        """

        low = 0
        high = len(self._container) - 1
        while low <= high:
            middle = (low + high) // 2
            if self._container[middle][0] > specs:
                high = middle - 1
            elif self._container[middle][0] < specs:
                low = middle + 1
            else:
                return middle
        return -1

    def _update_slices(self, n, p_n, delta):
        """
        Update tracking of positions of parameters with different n and p_n.

        Parameters
        ----------
        n : int
            n of the parameters to update the tracking for.
        p_n : int
            p_n of the parameters to update the tracking for.
        delta : int
            How many new parameters were added (positive) or removed (negative) to the
            (n, p_n) group.
        """
        for key in self._slices:
            # Update the length of the slice for the corresponding n and p_n
            if (n, p_n) == key:
                self._slices[key][1] += delta
            # Update the start for all the following slices
            elif (n, p_n) < key:
                self._slices[key][0] += delta

    def add(self, specs, parameter, when_present="raise error"):
        """
        Add arbitrary interaction parameter to the container.

        Parameters
        ----------
        specs : tuple
            Tuple with the special structure tha uniquely defines the spin operators
            associated with the interaction parameter.

            .. code-block:: python

                (n, p_n, (nu_2, ..., nu_n), (alpha_1, ..., alpha_n))

        parameter : (3, 3, ..., 3) |array-like|_
            Tensor of the interaction parameter. The number of dimensions is n.

        when_present : str, default "raise error"
            Action to take if such parameter is already present in the container. Supported
            values are:

            - ``"raise error"`` (default): raises an error.
            - ``"replace"``: replace existing value of the parameter with the new one.
            - ``"sum"``: add the value of the parameter to the existing one.
            - ``"mean"``: replace the value of the parameter with the arithmetic mean of
            existing and new parameters.
            - ``"skip"``: Leave existing parameter unchanged and continue without raising an
            error.

        Raises
        ------
        ValueError
            If the parameter is already present in the container and ``when_present`` is
            set to ``"raise error"``.
        """

        # REMOVE in September 2026
        if when_present == "add":
            when_present = "sum"
            import warnings

            warnings.warn(
                "Value 'add' for when_present is deprecated in 0.5.0 and will be removed in September 2026. Use 'sum' instead.",
                DeprecationWarning,
                stacklevel=2,
            )

        index = self._get_index(specs=specs)

        parameter = np.array(parameter, dtype=float)

        if index == -1:
            self._container.append([specs, parameter])
            self._container.sort(key=lambda x: x[0])
            self._update_slices(n=specs[0], p_n=specs[1], delta=1)
        else:
            if when_present == "raise error":
                raise ValueError("Parameter with such specs is already present.")
            elif when_present == "replace":
                self._container[index][1] = parameter
            elif when_present == "sum":
                self._container[index][1] += parameter
            elif when_present == "mean":
                self._container[index][1] = (self._container[index][1] + parameter) / 2
            elif when_present == "skip":
                pass
            else:
                raise ValueError(
                    f"Unsupported value for when_present: {when_present}. Supported values are: 'raise error', 'replace', 'sum', 'mean', 'skip'."
                )

    def remove(self, specs):
        """
        Remove an interaction parameter from the container.

        Parameters
        ----------
        specs : tuple
            Tuple with the special structure tha uniquely defines the spin operators
            associated with the interaction parameter.

            .. code-block:: python

                (n, p_n, (nu_2, ..., nu_n), (alpha_1, ..., alpha_n))
        """

        index = self._get_index(specs=specs)

        if index != -1:
            del self._container[index]
            self._update_slices(n=specs[0], p_n=specs[1], delta=-1)

    def copy(self):
        return deepcopy(self)

    def __add__(self, other):
        """
        Merge two interaction parameters containers.

        Parameters
        ----------
        other : _InteractionParameters
            Another interaction parameters container.

        Returns
        -------
        new_parameters : _InteractionParameters
            New interaction parameters container with the merged contents of both containers.
        """

        if not isinstance(other, self.__class__):
            raise TypeError(
                f"unsupported operand type(s) for +: '{self.__class__.__name__}' and '{other.__class__.__name__}'"
            )

        result = _InteractionParameters()

        i1 = 0
        L1 = len(self._container)

        i2 = 0
        L2 = len(other._container)

        while i1 < L1 or i2 < L2:
            if i1 >= L1:
                specs = other._container[i2][0]
                parameter = other._container[i2][1].copy()
                i2 += 1
            elif i2 >= L2:
                specs = self._container[i1][0]
                parameter = self._container[i1][1].copy()
                i1 += 1
            elif self._container[i1][0] < other._container[i2][0]:
                specs = self._container[i1][0]
                parameter = self._container[i1][1].copy()
                i1 += 1
            elif self._container[i1][0] > other._container[i2][0]:
                specs = other._container[i2][0]
                parameter = other._container[i2][1].copy()
                i2 += 1
            else:
                specs = self._container[i1][0]
                parameter = self._container[i1][1] + other._container[i2][1]
                i1 += 1
                i2 += 1

            result._container.append([specs, parameter])
            result._update_slices(n=specs[0], p_n=specs[1], delta=1)

        return result

    def __mul__(self, number):
        """
        Multiply all interaction parameters by a scalar.

        Parameters
        ----------
        number : float
            Number to multiply the interaction parameters by.

        Returns
        -------
        new_parameters : _InteractionParameters
            New interaction parameters container with the multiplied interaction parameters.
        """

        if not isinstance(number, int) and not isinstance(number, float):
            raise TypeError(
                f"unsupported operand type(s) for *: '{type(number)}' and '{self.__class__.__name__}'"
            )

        result = _InteractionParameters()
        result._slices = self._slices.copy()

        for specs, parameter in self._container:
            result._container.append([specs, parameter * number])

        return result

    def __rmul__(self, number):
        return self.__mul__(number=number)

    def __sub__(self, other):
        return self + (-1) * other

    def __len__(self):
        return len(self._container)

    def __contains__(self, specs):
        return self._get_index(specs=specs) != -1


INTEGER_PARTITION = {0: 0, 1: 1, 2: 2, 3: 3, 4: 5}


class _InteractionParametersIterator:
    def __init__(
        self, parameters: _InteractionParameters, n: int = None, p_n: int = None
    ):
        self.parameters = parameters

        if n is None:
            n = 0

        if p_n is None:
            p_n = 0

        if not 0 <= n <= 4:
            raise NotImplementedError(f"Parameters with {n} spins are not supported.")

        if not 0 <= p_n <= INTEGER_PARTITION[n]:
            raise ValueError(
                f"p_n for n={n} shall be between 0 and {INTEGER_PARTITION[n]}, got {p_n}."
            )

        self.n = n
        self.p_n = p_n

        if self.n == 0:
            self.start = 0
            self.length = len(self.parameters)
        elif self.p_n == 0:
            self.start = self.parameters._slices[(self.n, 1)][0]
            self.length = sum(
                [
                    self.parameters._slices[(n, p_n)][1]
                    for n, p_n in self.parameters._slices
                    if n == self.n
                ]
            )
        else:
            self.start, self.length = self.parameters._slices[(self.n, self.p_n)]

        self.index = 0

    def __next__(self):
        if self.index < self.length:
            self.index += 1
            (_, _, nus, alphas), parameter = self.parameters._container[
                self.start + self.index - 1
            ]
            return nus, alphas, parameter
        raise StopIteration

    def __getitem__(self, index: int):
        if index < 0 or index >= self.length:
            raise IndexError("index is out of range.")
        (_, _, nus, alphas), parameter = self.parameters._container[self.start + index]
        return nus, alphas, parameter

    # It is enough to provide the parameter as value, since the sites do not change
    def __setitem__(self, index: int, value):
        if index < 0 or index >= self.length:
            raise IndexError("index is out of range.")

        value = np.array(value)
        n = self.parameters._container[self.start + index][0][0]

        if len(value.shape) != n or any(_ != 3 for _ in value.shape):
            raise ValueError(
                f"Expected parameter to be a tensor with {n} components of size 3, got {value.shape}."
            )

        self.parameters._container[self.start + index][1] = np.array(value)

    def __len__(self):
        return self.length

    def __iter__(self):
        return self

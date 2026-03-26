# ================================== LICENSE ===================================
# Magnopy - Python package for magnons.
# Copyright (C) 2023-2026 Magnopy Team
#
# e-mail: anry@uv.es, web: magnopy.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ================================ END LICENSE =================================

import numpy as np


def _get_specs(alphas, nus):
    n = len(alphas)

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

    return (n, p_n, alphas, nus[1:])


class _InteractionParameters:
    """
    Interaction parameters of spin Hamiltonian.

    This class assumes:

    * Order of parameters by the specs = [n, p_n, alphas, nus].
    * Only one parameter for each set of alphas & nus.
    * That shape of the parameter's tensor matches n.
    * That n and/or p_n are correct for corresponding alphas and nus.
    """

    def __init__(self):
        # Elements of the container are
        # [(n, p_n, (alpha_1, ..., alpha_n), (nu_2, ..., nu_n)), parameter]
        self._container = []

    def _get_index(self, specs):
        """
        Get an index of an interaction parameter in the container if it exists.

        Parameters
        ----------
        specs : tuple
            Tuple with the special structure tha uniquely defines the spin operators
            associated with the interaction parameter.

            .. code-block:: python

                (n, p_n, (alpha_1, ..., alpha_n), (nu_1, ..., nu_n))

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

    def add(self, specs, parameter, when_present="raise error"):
        """
        Add arbitrary interaction parameter to the container.

        Parameters
        ----------
        specs : tuple
            Tuple with the special structure tha uniquely defines the spin operators
            associated with the interaction parameter.

            .. code-block:: python

                (n, p_n, (alpha_1, ..., alpha_n), (nu_2, ..., nu_n))

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

        index = self._get_index(specs=specs)

        parameter = np.array(parameter, dtype=float)

        if index == -1:
            self._container.append([specs, parameter])
            self._container.sort(key=lambda x: x[0])
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

                (n, p_n, (alpha_1, ..., alpha_n), (nu_2, ..., nu_n))
        """

        index = self._get_index(specs=specs)

        if index != -1:
            del self._container[index]

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

        L1 = len(self._container)
        L2 = len(other._container)
        i1 = 0
        i2 = 0
        while i1 < L1 and i2 < L2:
            if i1 >= L1:
                result._container.append(
                    [other._container[i2][0], other._container[i2][1].copy()]
                )
                i2 += 1
            if i2 >= L2:
                result._container.append(
                    [self._container[i1][0], self._container[i1][1].copy()]
                )
                i1 += 1
            elif self._container[i1][0] < other._container[i2][0]:
                result._container.append(
                    [self._container[i1][0], self._container[i1][1].copy()]
                )
                i1 += 1
            elif self._container[i1][0] > other._container[i2][0]:
                result._container.append(
                    [other._container[i2][0], other._container[i2][1].copy()]
                )
                i2 += 1
            else:
                result._container.append(
                    [
                        self._container[i1][0],
                        self._container[i1][1] + other._container[i2][1],
                    ]
                )
                i1 += 1
                i2 += 1

        return result

    def __mul__(self, scalar):
        """
        Multiply all interaction parameters by a scalar.

        Parameters
        ----------
        scalar : float
            Scalar to multiply the interaction parameters by.

        Returns
        -------
        new_parameters : _InteractionParameters
            New interaction parameters container with the multiplied interaction parameters.
        """

        if not isinstance(scalar, int) and not isinstance(scalar, float):
            raise TypeError(
                f"unsupported operand type(s) for *: '{type(scalar)}' and '{self.__class__.__name__}'"
            )

        result = _InteractionParameters()

        for specs, parameter in self._container:
            result._container.append([specs, parameter * scalar])

        return result

    def __rmul__(self, number):
        return self.__mul__(number=number)

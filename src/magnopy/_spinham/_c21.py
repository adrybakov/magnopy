# ================================== LICENSE ===================================
# Magnopy - Python package for magnons.
# Copyright (C) 2023-2025 Magnopy Team
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

from magnopy._spinham._validators import _validate_atom_index
from magnopy._spinham._units import _get_conversion_factor


@property
def _p21(spinham) -> list:
    r"""
    Parameters of (two spins & one site) term of the Hamiltonian.

    .. math::

        \boldsymbol{J}_{2,1}(\boldsymbol{r}_{\alpha})

    of the term

    .. math::

        C_{2,1}
        \sum_{\mu, \alpha, i, j}
        J^{ij}_{2,1}(\boldsymbol{r}_{\alpha})
        S_{\mu,\alpha}^i
        S_{\mu,\alpha}^j

    Returns
    -------
    parameters : list
        List of parameters. The list has a form of

        .. code-block:: python

            [[alpha, J], ...]

        ``0 <= len(parameters) <= len(spinham.atoms.names)``.

        where ``alpha`` is an index of the atom to which the parameter is assigned and
        ``J``  is a (3, ) :numpy:`ndarray`. The parameters are sorted by the index of an
        atom ``alpha`` in the ascending order.

    See Also
    --------
    add_21
    remove_21
    """

    return spinham._21


def _add_21(spinham, alpha: int, parameter, units=None, replace=False) -> None:
    r"""
    Adds a (two spins & one site) parameter to the Hamiltonian.

    Parameters
    ----------
    alpha : int
        Index of an atom, with which the parameter is associated.

        ``0 <= alpha < len(spinham.atoms.names)``.
    parameter : (3, ) |array-like|_
        Value of the parameter (:math:`3\times1` vector). Given in the units of ``units``.
    units : str, optional
        Units in which the ``parameter`` is given. Parameters have the the units of energy.
        By default assumes :py:attr:`.SpinHamiltonian.units`. For the list of the supported
        units see :py:attr:`.SpinHamiltonian.units`. If given ``units`` are different from
        :py:attr:`.SpinHamiltonian.units`, then the parameter's value will be converted
        automatically from ``units`` to :py:attr:`.SpinHamiltonian.units`.

        .. versionadded:: 0.2.2

    replace : bool, default False
        Whether to replace the value of the parameter if an atom already has a
        parameter associated with it.

    Raises
    ------
    ValueError
        If an atom already has a parameter associated with it.

    See Also
    --------
    p21
    remove_21
    """

    _validate_atom_index(index=alpha, atoms=spinham.atoms)
    spinham._reset_internals()

    parameter = np.array(parameter)

    if units is not None:
        parameter = parameter * _get_conversion_factor(
            old_units=units, new_units=spinham.units
        )

    # TD-BINARY_SEARCH
    # Try to find the place for the new one inside the list
    index = 0
    while index < len(spinham._21):
        # If already present in the model
        if spinham._21[index][0] == alpha:
            # Either replace
            if replace:
                spinham._21[index] = [alpha, parameter]
                return
            # Or raise an error
            raise ValueError(
                f"On-site quadratic anisotropy already set "
                f"for atom {alpha} ('{spinham.atoms.names[alpha]}')"
            )

        # If it should be inserted before current element
        if spinham._21[index][0] > alpha:
            spinham._21.insert(index, [alpha, parameter])
            return

        index += 1

    # If it should be inserted at the end or at the beginning of the list
    spinham._21.append([alpha, parameter])


def _remove_21(spinham, alpha: int) -> None:
    r"""
    Removes a (two spins & one site) parameter from the Hamiltonian.

    Parameters
    ----------
    alpha : int
        Index of an atom, with which the parameter is associated.

        ``0 <= alpha < len(spinham.atoms.names)``.

    See Also
    --------
    p21
    add_21
    """

    _validate_atom_index(index=alpha, atoms=spinham.atoms)

    for i in range(len(spinham._21)):
        # As the list is sorted, there is no point in resuming the search
        # when a larger element is found
        if spinham._21[i][0] > alpha:
            return

        if spinham._21[i][0] == alpha:
            del spinham._21[i]
            spinham._reset_internals()
            return

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


from copy import deepcopy
from math import ceil

import numpy as np
from wulfric import add_sugar

from magnopy._spinham._legacy_code import (
    _add_1,
    _add_21,
    _add_22,
    _add_31,
    _add_41,
    _remove_1,
    _remove_21,
    _remove_22,
    _remove_31,
    _remove_41,
)


from magnopy._spinham._convention import Convention
from magnopy._data_validation import (
    _validate_atom_index,
    _validate_unit_cell_index,
    _validated_units,
)
from magnopy._parameters._interaction_parameters import (
    _InteractionParameters,
    _InteractionParametersIterator,
    _get_specs,
)
from magnopy._parameters._symmetrization import get_equivalent


from magnopy._constants._units import _PARAMETER_UNITS, _PARAMETER_UNITS_MAKEUP
from magnopy._constants._si import BOHR_MAGNETON, ANGSTROM, VACUUM_MAGNETIC_PERMEABILITY

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _merge(list1: list, list2: list) -> list:
    r"""
    Merge two sorted parameter lists for any term.

    Lists of parameters have the form

    .. code-block:: python

        list = [[specs, parameter], ...]

    Comparison is based on specs.

    Parameter
    ---------
    list1 : list
        First list of parameters.
    list2 : list
        Second list of parameters.

    Returns
    -------
    merged_list : list
        Merged list of parameters.
    """

    list1 = deepcopy(list1)
    list2 = deepcopy(list2)

    merged_list = []

    i1 = 0
    i2 = 0

    while i1 < len(list1) or i2 < len(list2):
        if i1 >= len(list1):
            merged_list.append(list2[i2])
            i2 += 1
        elif i2 >= len(list2):
            merged_list.append(list1[i1])
            i1 += 1
        elif list1[i1][:-1] == list2[i2][:-1]:
            merged_list.append(list1[i1])
            merged_list[-1][-1] = merged_list[-1][-1] + list2[i2][-1]
            i1 += 1
            i2 += 1
        elif list1[i1][:-1] < list2[i2][:-1]:
            merged_list.append(list1[i1])
            i1 += 1
        else:
            merged_list.append(list2[i2])
            i2 += 1

    return merged_list


class SpinHamiltonian:
    r"""
    Spin Hamiltonian.

    Parameters
    ----------

    convention : :py:class:`.Convention` or str
        A convention of the spin Hamiltonian.

    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.

    atoms : dict
        Dictionary with atoms.

    units : str, default "meV"
        .. versionadded:: 0.3.0

        Units of the Hamiltonian's parameters. See :py:attr:`.SpinHamiltonian.units`
        for more details. Case-insensitive.


    Examples
    --------

    For example of usage see the page in the user guide -
    :ref:`user-guide_usage_spin-hamiltonian`.

    """

    def __init__(self, cell, atoms, convention, units="meV") -> None:
        self._cell = np.array(cell)

        self._atoms = add_sugar(atoms)

        # Only the magnetic sites
        self._magnetic_atoms = None
        self._map_to_magnetic = None
        self._map_to_all = None

        self._convention = convention

        if units.lower() not in _PARAMETER_UNITS:
            raise ValueError(
                f'Given units ("{units}") are not supported. Please use one of\n  * '
                + "\n  * ".join(list(_PARAMETER_UNITS))
            )

        self._units = units.lower()

        self._parameters = _InteractionParameters()

    ############################################################################
    #                              Cell and Atoms                              #
    ############################################################################

    @property
    def cell(self):
        r"""
        Cell of the crystal on which the Hamiltonian is build.

        Returns
        -------

        cell : (3, 3) :numpy:`ndarray`
            Matrix of the cell, rows are lattice vectors.

        Notes
        -----

        If is not recommended to change the ``cell`` property after the creation of
        :py:class:`.SpinHamiltonian`. In fact an attempt to do so will raise an
        ``AttributeError``:

        .. doctest::

            >>> import numpy as np
            >>> import magnopy
            >>> convention = magnopy.Convention()
            >>> spinham = magnopy.SpinHamiltonian(
            ...     cell=np.eye(3), atoms={}, convention=convention
            ... )
            >>> spinham.cell = 2 * np.eye(3)
            Traceback (most recent call last):
            ...
            AttributeError: Change of the cell attribute is not supported after the creation of SpinHamiltonian instance. If you need to modify cell, then use pre-defined methods of SpinHamiltonian or create a new one.

        Use pre-defined methods of the :py:class:`.SpinHamiltonian` class to safely
        modify the cell.

        If you need to change the cell attribute, then use

        .. doctest::

            >>> import numpy as np
            >>> import magnopy
            >>> convention = magnopy.Convention()
            >>> spinham = magnopy.SpinHamiltonian(
            ...     cell=np.eye(3), atoms={}, convention=convention
            ... )
            >>> spinham.cell
            array([[1., 0., 0.],
                   [0., 1., 0.],
                   [0., 0., 1.]])
            >>> spinham._cell = 2 * np.eye(3)
            >>> spinham.cell
            array([[2., 0., 0.],
                   [0., 2., 0.],
                   [0., 0., 2.]])


        In the latter case correct behavior of Magnopy **is not** guaranteed. Use only
        if you have a deep understanding of the Magnopy source code.
        """

        return self._cell

    @cell.setter
    def cell(self, new_value):
        raise AttributeError(
            "Change of the cell attribute is not allowed after the creation of SpinHamiltonian instance. SpinHamiltonian.cell is immutable."
        )

    @property
    def atoms(self) -> dict:
        r"""
        Atoms of the crystal on which the Hamiltonian is build.

        Returns
        -------

        atoms : dict (with added sugar)
            Dictionary with the atoms.

        Notes
        -----

        If is not recommended to change the atoms property after the creation of
        :py:class:`.SpinHamiltonian`. In fact an attempt to do so will raise an
        ``AttributeError``:

        .. doctest::

            >>> import numpy as np
            >>> import magnopy
            >>> convention = magnopy.Convention()
            >>> spinham = magnopy.SpinHamiltonian(
            ...     cell=np.eye(3), atoms={}, convention=convention
            ... )
            >>> spinham.atoms = {"names": ["Cr"]}
            Traceback (most recent call last):
            ...
            AttributeError: Change of the atoms dictionary is not supported after the creation of SpinHamiltonian instance. If you need to modify atoms, then use pre-defined methods of SpinHamiltonian or create a new one.

        Use pre-defined methods of the :py:class:`.SpinHamiltonian` class to safely
        modify atoms.

        If you need to change the whole dictionary at once, then use

        .. doctest::

            >>> import numpy as np
            >>> import magnopy
            >>> convention = magnopy.Convention()
            >>> spinham = magnopy.SpinHamiltonian(
            ...     cell=np.eye(3), atoms={}, convention=convention
            ... )
            >>> spinham.atoms
            {}
            >>> spinham._atoms = {"names": ["Cr"]}
            >>> spinham.atoms
            {'names': ['Cr']}

        In the latter case correct behavior of Magnopy **is not** guaranteed. Use only
        if you have a deep understanding of the Magnopy source code.
        """

        return self._atoms

    @atoms.setter
    def atoms(self, new_value):
        raise AttributeError(
            "Change of the atoms dictionary is not allowed after the creation of SpinHamiltonian instance. SpinHamiltonian.atoms is immutable."
        )

    @property
    def M_prime(self):
        r"""
        Number of atoms in the unit cell.

        .. versionadded:: 0.5.2

        Both magnetic and non-magnetic atoms are counted.

        Returns
        -------

        M_prime : int
            Number of atoms (magnetic and non-magnetic) in the unit cell.

        See Also
        --------
        M

        """

        return len(self.atoms.names)

    def _reset_internals(self):
        self._map_to_magnetic = None
        self._map_to_all = None
        self._magnetic_atoms = None

    def _update_internals(self):
        # Identify magnetic sites
        indices = set()

        for specs, _ in self._parameters._container:
            for alpha in specs[3]:
                indices.add(alpha)

        indices = sorted(list(indices))

        # Create index map from all to magnetic
        self._map_to_magnetic = [None for _ in range(len(self.atoms.names))]
        for i in range(len(indices)):
            self._map_to_magnetic[indices[i]] = i

        # Create index map from magnetic to all
        self._map_to_all = indices

        # Create magnetic atoms dictionary
        self._magnetic_atoms = add_sugar({})
        for key in self.atoms:
            self._magnetic_atoms[key] = []

            for full_index in indices:
                self._magnetic_atoms[key].append(self.atoms[key][full_index])

    @property
    def map_to_magnetic(self):
        r"""
        Index map from all atoms to the magnetic ones.

        Returns
        -------

        map_to_magnetic (L, ) list of int
            Index map. Integers. ``L = len(spinham.atoms.names)``
        """

        if self._map_to_magnetic is None:
            self._update_internals()

        return self._map_to_magnetic

    @property
    def map_to_all(self):
        r"""
        Index map from magnetic atoms to all atoms.

        Returns
        -------

        map_to_all (M, ) list of int
            Index map. Integers. ``M = len(spinham.magnetic_atoms.names)``
        """

        if self._map_to_all is None:
            self._update_internals()

        return self._map_to_all

    @property
    def magnetic_atoms(self):
        r"""
        Magnetic atoms of the spin Hamiltonian.

        Magnetic atom is defined as an atom with at least one parameter associated with
        it.

        This property is dynamically computed at every call.

        Returns
        -------

        magnetic_atoms : list of int
            Indices of magnetic atoms in the ``spinham.atoms``. Sorted.

        See Also
        --------

        M
        """

        if self._magnetic_atoms is None:
            self._update_internals()

        return self._magnetic_atoms

    @property
    def M(self):
        r"""
        Number of magnetic atoms in the unit cell.

        Returns
        -------

        M : int
            Number of magnetic atoms in the unit cell.

        See Also
        --------
        M_prime
        """

        return len(self.magnetic_atoms.names)

    ############################################################################
    #                                Convention                                #
    ############################################################################
    @property
    def convention(self) -> Convention:
        r"""
        Convention of the spin Hamiltonian.

        Returns
        -------

        convention : :py:class:`.Convention`

        See Also
        --------

        Convention
        """

        return self._convention

    @convention.setter
    def convention(self, new_convention: Convention):
        self._set_multiple_counting(new_convention._multiple_counting)

        self._set_spin_normalization(new_convention._spin_normalized)

        self._set_convention_constant(
            old_value=self.convention._c1, new_value=new_convention._c1, n=1, p_n=1
        )
        self._set_convention_constant(
            old_value=self.convention._c21, new_value=new_convention._c21, n=2, p_n=1
        )
        self._set_convention_constant(
            old_value=self.convention._c22, new_value=new_convention._c22, n=2, p_n=2
        )
        self._set_convention_constant(
            old_value=self.convention._c31, new_value=new_convention._c31, n=3, p_n=1
        )
        self._set_convention_constant(
            old_value=self.convention._c32, new_value=new_convention._c32, n=3, p_n=2
        )
        self._set_convention_constant(
            old_value=self.convention._c33, new_value=new_convention._c33, n=3, p_n=3
        )
        self._set_convention_constant(
            old_value=self.convention._c41, new_value=new_convention._c41, n=4, p_n=1
        )
        self._set_convention_constant(
            old_value=self.convention._c42, new_value=new_convention._c42, n=4, p_n=2
        )
        self._set_convention_constant(
            old_value=self.convention._c43, new_value=new_convention._c43, n=4, p_n=3
        )
        self._set_convention_constant(
            old_value=self.convention._c44, new_value=new_convention._c44, n=4, p_n=4
        )
        self._set_convention_constant(
            old_value=self.convention._c45, new_value=new_convention._c45, n=4, p_n=5
        )

        self._convention = new_convention

    def _set_multiple_counting(self, multiple_counting: bool) -> None:
        if multiple_counting is None or self.convention._multiple_counting is None:
            return

        multiple_counting = bool(multiple_counting)

        if self.convention.multiple_counting == multiple_counting:
            return

        new_parameters = _InteractionParameters()
        for (n, p_n, nus, alphas), parameter in self._parameters._container:
            equivalent_parameters = get_equivalent(
                n=n, p_n=p_n, nus=nus, alphas=alphas, parameter=parameter
            )

            degeneracy = len(equivalent_parameters)

            # It was absent before
            if multiple_counting:
                for nus, alphas, parameter in equivalent_parameters:
                    new_parameters.add(
                        specs=(n, p_n, nus, alphas), parameter=parameter / degeneracy
                    )
            # It was present before
            else:
                nus, alphas, parameter = equivalent_parameters[0]
                new_parameters.add(
                    specs=(n, p_n, nus, alphas),
                    parameter=parameter * degeneracy,
                    when_present="skip",
                )

        self._parameters = new_parameters

    def _set_spin_normalization(self, spin_normalized: bool) -> None:
        if spin_normalized is None or self.convention._spin_normalized is None:
            return

        spin_normalized = bool(spin_normalized)

        if self.convention.spin_normalized == spin_normalized:
            return

        for i, (specs, _) in enumerate(self._parameters._container):
            factor = 1.0
            for alpha in specs[3]:
                factor = factor * self.atoms.spins[alpha]
            # Before it was not normalized
            if spin_normalized:
                self._parameters._container[i][1] *= factor
            # Before it was normalized
            else:
                self._parameters._container[i][1] /= factor

    def _set_convention_constant(self, old_value, new_value, n, p_n) -> None:
        if new_value is None or old_value is None:
            return

        new_value = float(new_value)

        if old_value == new_value:
            return

        # If factor is changing one has to scale parameters.
        for i, (specs, _) in enumerate(self._parameters._container):
            if specs[:2] == (n, p_n):
                self._parameters._container[i][1] *= old_value / new_value
            elif specs[:2] > (n, p_n):
                break

    ############################################################################
    #                                   Units                                  #
    ############################################################################
    @property
    def units(self) -> str:
        r"""
        Units of the Hamiltonian's parameters.

        .. versionadded:: 0.3.0

        The parameters of the Hamiltonian are stored in some units of energy (or
        energy-like).

        When user adds a parameters to the Hamiltonian (i. e.
        :py:meth:`.SpinHamiltonian.add_21`, ...) the ``parameter`` argument is understood
        to be given in the units of :py:attr:`.SpinHamiltonian.units`.

        By default the Hamiltonian stores and expects parameters in "meV", but the user
        can choose out of the list of the supported units. See
        :ref:`user-guide_usage_units_parameters` for the full list of supported units.

        When Hamiltonian already has some parameters in it, then the change of
        :py:attr:`.SpinHamiltonian.units` will convert all parameter to the new units.
        The parameters that the user tries to add afterwards are expected to be in the new
        units already.

        Returns
        -------

        units : str

        See Also
        --------

        :ref:`user-guide_usage_units`
        """

        return _PARAMETER_UNITS_MAKEUP[self._units]

    @units.setter
    def units(self, new_units: str):
        new_units = _validated_units(units=new_units, supported_units=_PARAMETER_UNITS)

        conversion_factor = _PARAMETER_UNITS[self._units] / _PARAMETER_UNITS[new_units]

        for i in range(len(self._parameters._container)):
            self._parameters._container[i][1] *= conversion_factor

        self._units = new_units.lower()

    ############################################################################
    #                          External magnetic field                         #
    ############################################################################
    # ARGUMENT "h" DEPRECATED since 0.4.0
    # Remove in May of 2026
    def add_magnetic_field(self, B=None, alphas=None, h=None) -> None:
        r"""
        Adds external magnetic field to the Hamiltonian in the form of one spin
        parameters.

        .. math::

            \mu_B  g_{\alpha} \boldsymbol{B}\cdot\boldsymbol{S}_{\mu,\alpha}
            =
            C_1
            \boldsymbol{S}_{\mu,\alpha}
            \cdot
            \boldsymbol{J}_{Zeeman}(\boldsymbol{r}_{\alpha})

        where :math:`\boldsymbol{J}_{Zeeman}(\boldsymbol{r}_{\alpha})` is defined as

        .. math::

            \boldsymbol{J}_{Zeeman}(\boldsymbol{r}_{\alpha})
            =
            \dfrac{\mu_B g_{\alpha}}{C_1}\boldsymbol{B}

        Parameters
        ----------

        B : (3, ) |array-like|_
            Vector of magnetic field (magnetic flux density, B) given in the units of
            Tesla.

        alphas : list of int, optional
            Indices of atoms, to which the magnetic field effect should be added.

        h : (3, ) |array-like|_
            Vector of magnetic field given in the units of Tesla.

            .. deprecated:: 0.4.0
                The argument will be removed in May of 2026. Use ``B`` instead.

        Notes
        -----

        To minimize the energy the magnetic moment will be aligned with the
        direction of the external field. But spin vector will be directed opposite to the
        direction of the magnetic field.

        * If ``alphas is None``, then parameters of the magnetic field added
          only to the magnetic atoms. In other words only to atoms that already have
          at least one other parameter (any) associated with it.
        * If ``alpha is not None``, then parameters of magnetic field are added
          to the atoms with the provided indices (based on the order in
          :py:attr:`.SpinHamiltonian.atoms`)
        """

        if h is not None:
            import warnings

            warnings.warn(
                'Argument "h" is deprecated as of 0.4.0, use "B" instead. "h" will be removed in May of 2026.',
                DeprecationWarning,
                stacklevel=2,
            )
            B = h

        if B is None:
            raise TypeError(
                "SpinHamiltonian.add_magnetic_field() missing 1 required argument: 'B'"
            )

        if self.convention._c1 is None:
            self.convention._c1 = 1.0

        B = np.array(B, dtype=float)

        mu_B = BOHR_MAGNETON / _PARAMETER_UNITS[self._units]  # spinham.units / Tesla

        if alphas is None:
            alphas = self.map_to_all

        zeeman_parameters = [
            mu_B * self.atoms.g_factors[alpha] * B / self.convention.c1
            for alpha in alphas
        ]

        zeeman_term = _InteractionParameters()

        for alpha, parameter in zip(alphas, zeeman_parameters):
            zeeman_term.add(specs=(1, 1, (), (alpha,)), parameter=parameter)

        self._parameters = self._parameters + zeeman_term

        self._reset_internals()

    ############################################################################
    #                    Magnetic dipole-dipole interaction                    #
    ############################################################################

    def add_dipole_dipole(self, R_cut=None, E_cut=None, alphas=None):
        r"""
        Adds magnetic dipole dipole interaction to the Hamiltonian.

        Magnetic dipole dipole interaction is added in the form of two-spin & two-sites
        parameter

        .. math::

            C_{2,2}
            \sum_{\mu,\nu,\alpha,\beta,i,j}
            J_{dd}(\boldsymbol{r}_{\nu,\alpha\beta})^{ij}
            S_{\mu,\alpha}^i
            S_{\mu+\nu,\beta}^j

        where the parameter is defined as

        .. math::

            J_{dd}(\boldsymbol{r}_{\nu,\alpha\beta})^{ij}
            =
            \dfrac{\mu_0\mu_B^2}{8\pi C_{2,2}}
            \dfrac{g_{\alpha}g_{\beta}}{\vert\boldsymbol{r}_{\nu,\alpha\beta}\vert^3}
            (\delta_{k,l} - 3\hat{r}_{\nu,\alpha\beta}^i\hat{r}_{\nu,\alpha\beta}^j)

        if :py:attr:`.SpinHamiltonian.convention.multiple_counting` is ``True`` and as

        .. math::

            J_{dd}(\boldsymbol{r}_{\nu,\alpha\beta})^{ij}
            =
            \dfrac{\mu_0\mu_B^2}{4\pi C_{2,2}}
            \dfrac{g_{\alpha}g_{\beta}}{\vert\boldsymbol{r}_{\nu,\alpha\beta}\vert^3}
            (\delta_{k,l} - 3\hat{r}_{\nu,\alpha\beta}^i\hat{r}_{\nu,\alpha\beta}^j)

        if :py:attr:`.SpinHamiltonian.convention.multiple_counting` is ``False``.

        where :math:`g_{\alpha}` is a g-factor, :math:`\boldsymbol{\hat{r}}_{\nu,\alpha\beta}`
        is a unit vector.

        Parameters
        ----------

        R_cut : float, optional
            Cut off radius for the distance between a pair of atoms.
            :math:`R_{cut} \ge 0`.

        E_cut : float, optional
            Cut off value for the maximum value of the parameter.
            :math:`E_{cut} > 0`. Expected in the same units as
            :py:attr:`.SpinHamiltonian.units`.

        alphas : list of int, optional
            Indices of atoms, to which the magnetic field effect should be added.

        Raises
        ------

        ValueError
            * If none of the  ``R_cut`` or ``E_cut`` are provided.
            * If ``R_cut < 0``
            * If ``E_cut <= 0``

        Notes
        -----

        *   If only ``R_cut`` is given, then the dipole dipole term between the pair of
            spins :math:`S_{\mu,\alpha}^i` and :math:`S_{\mu+\nu,\beta}^j` is added if
            :math:`\vert\boldsymbol{r}_{\nu,\alpha\beta}\vert <= R_{cut}`.

        *   If only ``E_cut`` is given, then the ``R_cut`` is estimated as

            .. math::

                R_{cut}
                =
                \left(
                3\sqrt{2}
                \dfrac{\mu_0\mu_B^2g_{max}^2}{8\pi C_{2,2}E_{cut}}
                \right)^{\dfrac{1}{3}}

            if :py:attr:`.SpinHamiltonian.convention.multiple_counting` is ``True`` and as

            .. math::

                R_{cut}
                =
                \left(
                3\sqrt{2}
                \dfrac{\mu_0\mu_B^2g_{max}^2}{4\pi C_{2,2}E_{cut}}
                \right)^{\dfrac{1}{3}}

            if :py:attr:`.SpinHamiltonian.convention.multiple_counting` is ``False``.

            The dipole dipole term between the pair of spins :math:`S_{\mu,\alpha}^i` and
            :math:`S_{\mu+\nu,\beta}^j` is added if
            :math:`\vert\boldsymbol{r}_{\nu,\alpha\beta}\vert \le R_{cut}` and
            :math:`\vert J_{dd}(\boldsymbol{r}_{\nu,\alpha\beta})^{ij}\vert\ge E_{cut}`
            for some :math:`i, j`.

        *   If both ``R_cut`` and ``E_cut`` are provided, then the dipole dipole term
            between the pair of spins :math:`S_{\mu,\alpha}^i` and
            :math:`S_{\mu+\nu,\beta}^j` is added if
            :math:`\vert\boldsymbol{r}_{\nu,\alpha\beta}\vert \le R_{cut}` and
            :math:`\vert J_{dd}(\boldsymbol{r}_{\nu,\alpha\beta})^{ij}\vert \ge E_{cut}`
            for some :math:`i, j`.

        Magnetic dipole-dipole interaction is added either to magnetic atoms or
        to the list of the atoms provided by user.

        * If ``alphas is None``, then parameters of the magnetic field added
          only to the magnetic atoms. In other words only to atoms that already have
          at least one other parameter (any) associated with it.
        * If ``alpha is not None``, then parameters of magnetic field are added
          to the atoms with the provided indices (based on the order in
          :py:attr:`.SpinHamiltonian.atoms`)
        """

        # Constants
        MU_0_MU_B = (
            VACUUM_MAGNETIC_PERMEABILITY
            * BOHR_MAGNETON**2
            / ANGSTROM**3
            / _PARAMETER_UNITS[self._units]
        )  # spinham.units * Angstrom^3

        if E_cut is None and R_cut is None:
            raise ValueError("Expected either E_cut or R_cut, got neither.")

        if E_cut is not None:
            if E_cut <= 0:
                raise ValueError(f"Expected positive cut-off energy, got {E_cut}.")

            R_cut = (
                3
                * np.sqrt(2)
                * MU_0_MU_B
                * max(self.atoms.g_factors) ** 2
                / 4
                / np.pi
                / self.convention.c22
                / E_cut
            )

            if self.convention.multiple_counting:
                R_cut = R_cut / 2

            R_cut = R_cut ** (1 / 3)
        else:
            R_cut = float(R_cut)

        if R_cut < 0:
            raise ValueError(f"Expected positive cut-off radius, got {R_cut}.")

        # Get indices for unit cells of interest
        a1, a2, a3 = self.cell
        a_3_perp = abs(np.cross(a1, a2) @ a3 / np.linalg.norm(np.cross(a1, a2)))
        m_3_max = ceil(R_cut / a_3_perp)
        a_2_perp = np.cross(a2, a3) @ a1 / np.linalg.norm(np.cross(a2, a3))
        m_2_max = ceil(R_cut / a_2_perp)

        m_1_max = ceil(R_cut / np.linalg.norm(a1))

        # Run over all pairs of atoms between (0, 0, 0) and all unit cells of
        # interest
        dd_parameters = _InteractionParameters()

        if alphas is None:
            alphas = self.map_to_all

        for alpha in alphas:
            for k in range(-m_3_max, m_3_max + 1):
                for j in range(-m_2_max, m_2_max + 1):
                    for i in range(-m_1_max, m_1_max + 1):
                        for beta in alphas:
                            if ((i, j, k), beta) == ((0, 0, 0), alpha):
                                continue

                            vector = (
                                np.array([i, j, k])
                                + self.atoms.positions[beta]
                                - self.atoms.positions[alpha]
                            ) @ self.cell
                            distance = np.linalg.norm(vector)

                            if distance <= R_cut:
                                parameter = (
                                    MU_0_MU_B
                                    / 4
                                    / np.pi
                                    / self.convention.c22
                                    * self.atoms.g_factors[alpha]
                                    * self.atoms.g_factors[beta]
                                    / distance**3
                                ) * (
                                    np.eye(3, dtype=float)
                                    - 3 * np.outer(vector, vector) / distance**2
                                )
                                if self.convention.multiple_counting:
                                    parameter = parameter / 2

                                if E_cut is None or (np.abs(parameter) >= E_cut).any():
                                    if not self.convention.multiple_counting:
                                        equivalent_parameters = get_equivalent(
                                            n=2,
                                            p_n=2,
                                            nus=((i, j, k),),
                                            alphas=(alpha, beta),
                                            parameter=parameter,
                                        )

                                        nu, alphas, parameter = equivalent_parameters[0]
                                    else:
                                        nu = (i, j, k)
                                        alphas = (alpha, beta)

                                    dd_parameters.add(
                                        specs=(2, 2, (nu,), alphas),
                                        parameter=parameter,
                                        when_present="skip",
                                    )

        self._parameters = self._parameters + dd_parameters

    ############################################################################
    #                                Copy getter                               #
    ############################################################################
    def copy(self):
        R"""
        Returns a new, independent copy of the same Hamiltonian.

        Returns
        -------

        spinham : :py:class:`.SpinHamiltonian`
            A new instance of the same Hamiltonian.
        """

        return deepcopy(self)

    def get_empty(self):
        r"""
        Returns the Hamiltonian with the same cell, atoms, units and convention, but with no
        parameters present.

        Returns
        -------

        spinham : py:class:`.SpinHamiltonian`
            New instance of the spin Hamiltonian.

        Notes
        -----
        Note that in the new Hamiltonian ``spinham.M == 0`` - as there is no parameters
        present, then no atoms are considered to be magnetic.
        """

        return SpinHamiltonian(
            cell=self.cell,
            atoms=self.atoms,
            convention=self.convention,
            units=self.units,
        )

    ############################################################################
    #                           Arithmetic operations                          #
    ############################################################################
    def __mul__(self, number):
        if not isinstance(number, int) and not isinstance(number, float):
            raise TypeError(
                f"unsupported operand type(s) for *: '{type(number)}' and 'SpinHamiltonian'"
            )

        spinham = self.copy()

        spinham._parameters = spinham._parameters * number

        return spinham

    def __rmul__(self, number):
        return self.__mul__(number=number)

    def __add__(self, other):
        if not isinstance(other, SpinHamiltonian):
            raise NotImplementedError

        # Check that unit cells are the same
        if not np.allclose(self.cell, other.cell):
            raise ValueError(
                "Unit cells of two Hamiltonians are different, summation is not supported"
            )

        # Check that atoms are the same
        same_atoms = True
        if len(self.atoms.names) != len(other.atoms.names):
            same_atoms = False
        else:
            for i in range(len(self.atoms.names)):
                if (
                    self.atoms.names[i] != other.atoms.names[i]
                    or not np.allclose(
                        self.atoms.positions[i], other.atoms.positions[i]
                    )
                    or abs(self.atoms.spins[i] - other.atoms.spins[i]) > 1e-8
                    or abs(self.atoms.g_factors[i] - other.atoms.g_factors[i]) > 1e-8
                ):
                    same_atoms = False

        if not same_atoms:
            raise ValueError(
                "Atoms of two spin Hamiltonians are different, summation is not supported."
            )

        # Make sure that units are the same
        other_units = other.units
        other.units = self.units

        # Make sure that conventions are the same
        other_convention = other.convention
        other.convention = self.convention

        result = self.get_empty()
        result._parameters = self._parameters + other._parameters

        # Restore units of other Hamiltonian
        other.units = other_units

        # Restore convention of other Hamiltonian
        other.convention = other_convention

        return result

    def __sub__(self, other):
        return self + (-1) * other

    ############################################################################
    #                          Interaction parameters                          #
    ############################################################################
    # TODO: check that the implementation is reasonable
    def add(
        self,
        nus,
        alphas,
        parameter,
        units=None,
        populate_equivalent=False,
        when_present="raise error",
    ):
        r"""
        Add any parameter with at most four components of spin operator to the
        Hamiltonian.

        .. versionadded:: 0.5.0

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for the definition of the
        Hamiltonian.

        Parameters
        ----------
        nus : (n, 3) or (n-1, 3) list/tuple of tuple of int
            List of unit cell indices associated with the parameter. Each unit cell index
            is a tuple of three integers (i, j, k) corresponding to the translation by
            :math:`i\boldsymbol{a}_1 + j\boldsymbol{a}_2 + k\boldsymbol{a}_3`.

        alphas : (n,) list/tuple of int
            List of indices of atoms associated with the parameter. Based on the order in
            :py:attr:`.SpinHamiltonian.atoms`.

        units : str, optional
            Units in which the  ``parameter``  is given.  Parameters have the the units of
            energy. By default assumes :py:attr:`.SpinHamiltonian.units`.  For the list of
            the  supported  units  see  :ref:`user-guide_usage_units_parameters`.  If
            given  ``units``  are different from  :py:attr:`.SpinHamiltonian.units`,  then
            the  parameter's  value  will be  converted  automatically from  ``units``  to
            :py:attr:`.SpinHamiltonian.units`.

        populate_equivalent : bool, default False
            Whether to automatically populate all equivalent parameters related by the
            symmetrization procedure. Ignored if ``convention.multiple_counting`` is
            ``False``.

        when_present : str, default "raise error"
            Action to take if an atom already has a parameter associated with it.
            Case-insensitive. Supported values are:

            - ``"raise error"`` (default): raises an error.
            - ``"replace"``: replace existing value of the parameter with the new one.
            - ``"sum"``: add the value of the parameter to the existing one.
            - ``"mean"``: replace the value of the parameter with the arithmetic mean of
              existing and new parameters.
            - ``"skip"``: Leave existing parameter unchanged and continue without raising
              an error.

        Notes
        -----

        If ``len(nus) == len(alphas) -1``, the correspondence between the ``alphas`` and
        ``nus`` is as follows

        * ``alphas[0]`` always located in the unit cell (0, 0, 0).
        * ``alphas[i]`` is located in the unit cell ``nus[i-1]`` for ``i >= 1``.

        If ``len(nus) == len(alphas)``, then the ``i``-th atom is located in the unit cell
        ``nus[i]`` for all ``i``. Note that the translational symmetry is always
        enforced, so the ``nus`` are updated as ``nus[i] = nus[i] - nus[0]`` for all
        ``i`` before the parameter is added to the Hamiltonian.

        """

        self._reset_internals()

        for alpha in alphas:
            _validate_atom_index(index=alpha, atoms=self.atoms)

        for nu in nus:
            _validate_unit_cell_index(ijk=nu)

        if not (len(alphas) - 1 == len(nus) or len(alphas) == len(nus)):
            raise ValueError(
                f"Expected number of unit cell indices to be equal to or one less than the number of atom indices, got {len(alphas)} atom indices and {len(nus)} unit cell indices."
            )

        if len(nus) == len(alphas) - 1:
            nus = tuple([(0, 0, 0)] + list(nus))

        parameter = np.array(parameter)

        if not len(parameter.shape) == len(alphas) or any(
            _ != 3 for _ in parameter.shape
        ):
            raise ValueError(
                f"Expected parameter to be a tensor with {len(alphas)} components of size 3, got {parameter.shape}."
            )

        if units is not None:
            units = _validated_units(units=units, supported_units=_PARAMETER_UNITS)
            parameter = (
                parameter * _PARAMETER_UNITS[units] / _PARAMETER_UNITS[self._units]
            )

        specs = _get_specs(nus=nus, alphas=alphas)

        if self.convention.multiple_counting:
            if populate_equivalent:
                equivalent_parameters = get_equivalent(
                    n=specs[0],
                    p_n=specs[1],
                    nus=specs[2],
                    alphas=specs[3],
                    parameter=parameter,
                )

                for nus, alphas, parameter in equivalent_parameters:
                    self._parameters.add(
                        specs=(specs[0], specs[1], nus, alphas),
                        parameter=parameter,
                        when_present=when_present,
                    )
            else:
                self._parameters.add(
                    specs=specs, parameter=parameter, when_present=when_present
                )
        else:
            equivalent_parameters = get_equivalent(
                n=specs[0],
                p_n=specs[1],
                nus=specs[2],
                alphas=specs[3],
                parameter=parameter,
            )
            nus, alphas, parameter = equivalent_parameters[0]

            self._parameters.add(
                specs=(specs[0], specs[1], nus, alphas),
                parameter=parameter,
                when_present=when_present,
            )

    # TODO: check that the implementation is reasonable
    def remove(self, nus, alphas, remove_equivalent=False):
        r"""
        Removes any parameter with at most four components of spin operator from the
        Hamiltonian.

        .. versionadded:: 0.5.0

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for the definition of the
        Hamiltonian.

        Parameters
        ----------
        nus : (n, 3) or (n-1, 3) list/tuple of tuple of int
            List of unit cell indices associated with the parameter. Each unit cell index
            is a tuple of three integers (i, j, k) corresponding to the translation by
            :math:`i\boldsymbol{a}_1 + j\boldsymbol{a}_2 + k\boldsymbol{a}_3`.

        alphas : (n,) list/tuple of int
            List of indices of atoms associated with the parameter. Based on the order in
            :py:attr:`.SpinHamiltonian.atoms`.

        remove_equivalent : bool, default False
            Whether to automatically remove all equivalent parameters related by the
            symmetrization procedure. Ignored if ``convention.multiple_counting`` is
            ``False``.


        Notes
        -----

        See notes of :py:meth:`.SpinHamiltonian.add` for the details on ``nus`` and
        ``alphas``.

        """

        for alpha in alphas:
            _validate_atom_index(index=alpha, atoms=self.atoms)

        for nu in nus:
            _validate_unit_cell_index(ijk=nu)

        if not (len(alphas) - 1 == len(nus) or len(alphas) == len(nus)):
            raise ValueError(
                f"Expected number of unit cell indices to be equal to or one less than the number of atom indices, got {len(alphas)} atom indices and {len(nus)} unit cell indices."
            )

        if len(nus) == len(alphas) - 1:
            nus = tuple([(0, 0, 0)] + list(nus))

        specs = _get_specs(nus=nus, alphas=alphas)

        if self.convention.multiple_counting:
            if remove_equivalent:
                equivalent_parameters = get_equivalent(
                    n=specs[0],
                    p_n=specs[1],
                    nus=specs[2],
                    alphas=specs[3],
                    parameter=None,
                )

                for nus, alphas, _ in equivalent_parameters:
                    self._parameters.remove(specs=(specs[0], specs[1], nus, alphas))
            else:
                self._parameters.remove(specs=specs)
        else:
            equivalent_parameters = get_equivalent(
                n=specs[0], p_n=specs[1], nus=specs[2], alphas=specs[3]
            )
            nus, alphas, _ = equivalent_parameters[0]

            self._parameters.remove(specs=(specs[0], specs[1], nus, alphas))

    def parameters(self, n=None, p_n=None):
        r"""
        Returns an iterator over parameters of the Hamiltonian.

        .. versionadded:: 0.5.0

        Parameters
        ----------
        n : int, optional
            Number of spins of the respective spin Hamiltonian term.
            Expected to be between 1 and 4. If not given, then all parameters are returned
            and ``p_n`` is ignored.
        p_n : int, optional
            Index of integer partition of ``n``. Expected to be between 1 and maximal
            number of integer partitions for the given ``n``. If not given, then
            parameters of all respective terms of the spin Hamiltonian with ``n`` spins
            are returned. Ignored if ``n`` is not given.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. Each element of the iterator is
            a tuple ``(nus, alphas, parameter)`` where ``nus`` is a
            tuple of unit cell indices, ``alphas`` is a tuple of atom indices, and
            ``parameter`` is a tensor of the parameter's value.

            - ``len(alphas) = n``
            - ``len(nus) == len(alphas) - 1``
            - ``len(parameter.shape) == len(alphas)``
            - ``parameter.shape[i] == 3`` for all ``0 <= i < len(alphas)``
            - ``alphas[0]`` is always located in the unit cell (0, 0, 0)
            - ``alphas[i]`` is located in the unit cell ``nus[i-1]`` for
              ``1 <= i < len(alphas)``

        See Also
        --------
        add
        remove
        p1
        p21
        p22
        p31
        p32
        p33
        p41
        p42
        p43
        p44
        p45
        """

        return _InteractionParametersIterator(parameters=self._parameters, n=n, p_n=p_n)

    def symmetrize(self):
        r"""
        Symmetrize interaction parameters as specified in the SI note 3 of |paper-2026|_.
        """

        if self.convention.multiple_counting:
            new_parameters = _InteractionParameters()
            for (n, p_n, nus, alphas), parameter in self._parameters._container:
                equivalent_parameters = get_equivalent(
                    n=n, p_n=p_n, nus=nus, alphas=alphas, parameter=parameter
                )

                degeneracy = len(equivalent_parameters)

                for nus, alphas, parameter in equivalent_parameters:
                    new_parameters.add(
                        specs=(n, p_n, nus, alphas),
                        parameter=parameter / degeneracy,
                        when_present="sum",
                    )

            self._parameters = new_parameters

    ############################################################################
    #                          One spin & one site (1)                         #
    ############################################################################
    @property
    def p1(self):
        r"""
        Parameters of one spin & one site term of the Hamiltonian (:ref:`ug_tb_sh_1-1`).

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for more details.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. See notes of
            :py:meth:`.SpinHamiltonian.parameters` for more details.

        See Also
        --------
        add
        remove
        parameters
        """

        return self.parameters(n=1, p_n=1)

    ############################################################################
    #                       Two spins & one site (2 + 0)                       #
    ############################################################################

    @property
    def p21(self):
        r"""
        Parameters of two spins & one site term of the Hamiltonian (:ref:`ug_tb_sh_2-1`).

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for more details.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. See notes of
            :py:meth:`.SpinHamiltonian.parameters` for more details.

        See Also
        --------
        add
        remove
        parameters
        """

        return self.parameters(n=2, p_n=1)

    ############################################################################
    #                        Two spins & two sites (1+1)                       #
    ############################################################################

    @property
    def p22(self):
        r"""
        Parameters of two spins & two sites term of the Hamiltonian (:ref:`ug_tb_sh_2-2`).

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for more details.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. See notes of
            :py:meth:`.SpinHamiltonian.parameters` for more details.

        See Also
        --------
        add
        remove
        parameters
        """

        return self.parameters(n=2, p_n=2)

    ############################################################################
    #                      Three spins & one site (3+0+0)                      #
    ############################################################################

    @property
    def p31(self):
        r"""
        Parameters of three spins & one site term of the Hamiltonian
        (:ref:`ug_tb_sh_3-1`).

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for more details.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. See notes of
            :py:meth:`.SpinHamiltonian.parameters` for more details.

        See Also
        --------
        add
        remove
        parameters
        """

        return self.parameters(n=3, p_n=1)

    ############################################################################
    #                      Three spins & two sites (2+1+0)                     #
    ############################################################################
    @property
    def p32(self):
        r"""
        Parameters of three spins & two sites term of the Hamiltonian
        (:ref:`ug_tb_sh_3-2`).

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for more details.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. See notes of
            :py:meth:`.SpinHamiltonian.parameters` for more details.

        See Also
        --------
        add
        remove
        parameters
        """

        return self.parameters(n=3, p_n=2)

    ############################################################################
    #                     Three spins & three sites (1+1+1)                    #
    ############################################################################
    @property
    def p33(self):
        r"""
        Parameters of three spins & three sites term of the Hamiltonian
        (:ref:`ug_tb_sh_3-3`).

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for more details.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. See notes of
            :py:meth:`.SpinHamiltonian.parameters` for more details.

        See Also
        --------
        add
        remove
        parameters
        """

        return self.parameters(n=3, p_n=3)

    ############################################################################
    #                     Four spins & one site (4+0+0+0)                      #
    ############################################################################
    @property
    def p41(self):
        r"""
        Parameters of four spins & one site term of the Hamiltonian (:ref:`ug_tb_sh_4-1`).

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for more details.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. See notes of
            :py:meth:`.SpinHamiltonian.parameters` for more details.

        See Also
        --------
        add
        remove
        parameters
        """

        return self.parameters(n=4, p_n=1)

    ############################################################################
    #                     Four spins & two sites (3+1+0+0)                     #
    ############################################################################
    @property
    def p42(self):
        r"""
        Parameters of four spins & two sites term of the Hamiltonian
        (:ref:`ug_tb_sh_4-2`).

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for more details.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. See notes of
            :py:meth:`.SpinHamiltonian.parameters` for more details.

        See Also
        --------
        add
        remove
        parameters
        """

        return self.parameters(n=4, p_n=2)

    ############################################################################
    #                     Four spins & two sites (2+2+0+0)                     #
    ############################################################################
    @property
    def p43(self):
        r"""
        Parameters of four spins & two sites term of the Hamiltonian
        (:ref:`ug_tb_sh_4-3`).

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for more details.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. See notes of
            :py:meth:`.SpinHamiltonian.parameters` for more details.

        See Also
        --------
        add
        remove
        parameters
        """

        return self.parameters(n=4, p_n=3)

    ############################################################################
    #                    Four spins & three sites (2+1+1+0)                    #
    ############################################################################
    @property
    def p44(self):
        r"""
        Parameters of four spins & three sites term of the Hamiltonian
        (:ref:`ug_tb_sh_4-4`).

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for more details.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. See notes of
            :py:meth:`.SpinHamiltonian.parameters` for more details.

        See Also
        --------
        add
        remove
        parameters
        """

        return self.parameters(n=4, p_n=4)

    ############################################################################
    #                    Four spins & four sites (1+1+1+1)                     #
    ############################################################################
    @property
    def p45(self):
        r"""
        Parameters of four spins & four sites term of the Hamiltonian
        (:ref:`ug_tb_sh_4-5`).

        See :ref:`user-guide_theory-behind_spin-hamiltonian` for more details.

        Returns
        -------
        parameters : iterator
            Iterator over parameters of the Hamiltonian. See notes of
            :py:meth:`.SpinHamiltonian.parameters` for more details.

        See Also
        --------
        add
        remove
        parameters
        """

        return self.parameters(n=4, p_n=5)

    ############################################################################
    #                              Legacy methods                              #
    ############################################################################

    add_1 = _add_1
    remove_1 = _remove_1

    add_21 = _add_21
    remove_21 = _remove_21

    add_22 = _add_22
    remove_22 = _remove_22

    add_31 = _add_31
    remove_31 = _remove_31

    add_41 = _add_41
    remove_41 = _remove_41


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir

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

from magnopy._parameters._p22 import from_dmi, from_iso
from magnopy._spinham._convention import Convention
from magnopy._spinham._hamiltonian import SpinHamiltonian

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def ivuzjo(N=10, J=10):
    r"""
    Prepares a Hamiltonian from the paper by Ivanov, Uzdin and Jónsson.

    See [1]_ for details. The Hamiltonian is defined as

    .. math::

        \mathcal{H}
        =
        -\dfrac{1}{2}
        \sum_{\mu, \nu}
        J
        \left(
            \boldsymbol{S}_{\mu}
            \cdot
            \boldsymbol{S}_{\mu+\nu}
        \right)
        -
        \dfrac{1}{2}
        \sum_{\mu, \nu}
        \dfrac{J}{2}
        \boldsymbol{r}_{\nu}
        \cdot
        \left(
            \boldsymbol{S}_{\mu}
            \times
            \boldsymbol{S}_{\mu+\nu}
        \right)
        +
        \sum_{\mu}
        J
        \left(
            \boldsymbol{\hat{z}}
            \cdot
            \boldsymbol{S}_{\mu}
        \right)

    Parameters
    ----------

    N : int, default 10
        Size of the supercell (N x N).

    J : float, default 10
        Value of the isotropic exchange in energy units (meV), sign is *not* ignored.

    Returns
    -------

    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian (with magnetic field)

    References
    ----------

    .. [1] Ivanov, A.V., Uzdin, V.M. and Jónsson, H., 2021.
        Fast and robust algorithm for energy minimization of spin systems applied
        in an analysis of high temperature spin configurations in terms of skyrmion
        density.
        Computer Physics Communications, 260, p.107749.

    Examples
    --------

    To create an example Hamiltonian use

    .. doctest::

        >>> import magnopy
        >>> spinham = magnopy.examples.ivuzjo()

    .. doctest::

        >>> spinham.cell
        array([[10.,  0.,  0.],
               [ 0., 10.,  0.],
               [ 0.,  0.,  1.]])

    .. doctest::

        >>> len(spinham.atoms.names)
        100

    """

    D = J / 2

    BOHR_MAGNETON = 0.057883818060  # meV / Tesla

    cell = np.diag([N, N, 1.0])

    atoms = dict(names=[], positions=[], g_factors=[], spins=[])
    names_to_index = {}
    atom_index = 0
    for i in range(0, N):
        for j in range(0, N):
            atoms["names"].append(f"Fe_{i + 1}_{j + 1}")
            atoms["positions"].append([i + 0.5, j + 0.5, 0])
            atoms["spins"].append(1)
            atoms["g_factors"].append(2)
            names_to_index[f"Fe_{i + 1}_{j + 1}"] = atom_index
            atom_index += 1

    convention = Convention(
        multiple_counting=True, spin_normalized=False, c21=-1, c22=-0.5
    )

    spinham = SpinHamiltonian(cell=cell, atoms=atoms, convention=convention)

    # For each atom add bonds
    for i in range(0, N):
        for j in range(0, N):
            alpha = names_to_index[f"Fe_{i + 1}_{j + 1}"]

            # 1 0 0
            if i == N - 1:
                nu = (1, 0, 0)
                beta = names_to_index[f"Fe_1_{j + 1}"]
            else:
                nu = (0, 0, 0)
                beta = names_to_index[f"Fe_{i + 2}_{j + 1}"]

            parameter = from_iso(iso=J) + from_dmi(dmi=[D, 0, 0])
            spinham.add(nus=[nu], alphas=[alpha, beta], parameter=parameter)

            # 0 1 0
            if j == N - 1:
                nu = (0, 1, 0)
                beta = names_to_index[f"Fe_{i + 1}_1"]
            else:
                nu = (0, 0, 0)
                beta = names_to_index[f"Fe_{i + 1}_{j + 2}"]
            parameter = from_iso(iso=J) + from_dmi(dmi=[0, D, 0])
            spinham.add(nus=[nu], alphas=[alpha, beta], parameter=parameter)

    spinham.add_magnetic_field(B=[0, 0, J / 5 / BOHR_MAGNETON / 2])

    return spinham


def full_ham(M=4):
    r"""
    Prepares a Hamiltonian with ``M`` atoms on a cubic lattice and all possible types of
    interaction parameters populated.

    Parameters
    ----------
    M : int, default 4
        Number of magnetic atoms in the unit cell. Must be greater than or equal to 4.

    Returns
    -------

    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian with ``M`` atoms and all possible types of interaction
        parameters populated.

    Notes
    -----

    This Hamiltonian is not meant to represent any physical system. Its purpose is to be
    used in the examples of the code, when the creation of the Hamiltonian is not the main
    point of the example.

    Examples
    --------

    To get an instance of the Hamiltonian use

    .. doctest::

        >>> import magnopy
        >>> spinham = magnopy.examples.full_ham()

    .. doctest::

        >>> spinham.cell
        array([[1., 0., 0.],
               [0., 1., 0.],
               [0., 0., 1.]])
        >>> spinham.atoms.names
        ['Fe1', 'Fe2', 'Fe3', 'Fe4']
        >>> spinham.convention
        magnopy.Convention(
            multiple_counting = True,
            spin_normalized = False,
            c1 = 1.0,
            c21 = 1.0,
            c22 = 1.0,
            c31 = 1.0,
            c32 = 1.0,
            c33 = 1.0,
            c41 = 1.0,
            c42 = 1.0,
            c43 = 1.0,
            c44 = 1.0,
            c45 = 1.0,
            name = "full_ham(m=4)"
        )

    .. doctest::

        >>> len(spinham.parameters())
        1660
        >>> len(spinham.p1)
        4
        >>> len(spinham.p21)
        4
        >>> len(spinham.p22)
        20
        >>> len(spinham.p31)
        4
        >>> len(spinham.p32)
        84
        >>> len(spinham.p33)
        24
        >>> len(spinham.p41)
        4
        >>> len(spinham.p42)
        64
        >>> len(spinham.p43)
        60
        >>> len(spinham.p44)
        624
        >>> len(spinham.p45)
        768

    Note how the amount of parameters changes when we change convention to
    non-multiple counting:

    .. doctest::

        >>> spinham.convention = spinham.convention.get_modified(
        ...     multiple_counting=False
        ... )

        >>> len(spinham.parameters())
        168
        >>> len(spinham.p1)
        4
        >>> len(spinham.p21)
        4
        >>> len(spinham.p22)
        10
        >>> len(spinham.p31)
        4
        >>> len(spinham.p32)
        28
        >>> len(spinham.p33)
        4
        >>> len(spinham.p41)
        4
        >>> len(spinham.p42)
        16
        >>> len(spinham.p43)
        10
        >>> len(spinham.p44)
        52
        >>> len(spinham.p45)
        32

    """

    cell = np.eye(3, dtype=float)

    if M < 4:
        raise ValueError("M must be an integer greater than or equal to 4.")

    atoms = dict(
        names=[f"Fe{_ + 1}" for _ in range(M)],
        positions=np.linspace([0, 0, 0], [1, 1, 1], M + 1)[:-1],
        spins=[5 / 2] * M,
        g_factors=[2] * M,
        spglib_types=list(range(M)),
    )
    convention = Convention(
        spin_normalized=False,
        multiple_counting=True,
        c1=1,
        c21=1,
        c22=1,
        c31=1,
        c32=1,
        c33=1,
        c41=1,
        c42=1,
        c43=1,
        c44=1,
        c45=1,
        name=f"full_ham(M={M})",
    )

    spinham = SpinHamiltonian(cell=cell, atoms=atoms, convention=convention)

    ############################################################################
    #                                 One site                                 #
    ############################################################################
    for alpha_1 in range(0, M):
        # (1) terms
        spinham.add(nus=[], alphas=[alpha_1], parameter=[-1, 0, 2])

        # (2, 1) terms
        parameter = np.ones((3, 3))
        parameter[0, 0] = -1
        spinham.add(nus=[(0, 0, 0)], alphas=[alpha_1, alpha_1], parameter=parameter)

        # (3, 1) terms
        parameter = np.ones((3, 3, 3))
        parameter[0, 0, 0] = 2
        spinham.add(
            nus=[(0, 0, 0), (0, 0, 0)],
            alphas=[alpha_1, alpha_1, alpha_1],
            parameter=parameter,
        )

        # (4, 1) terms
        parameter = np.ones((3, 3, 3, 3))
        parameter[0, 0, 0, 0] = -1
        spinham.add(
            nus=[(0, 0, 0), (0, 0, 0), (0, 0, 0)],
            alphas=[alpha_1, alpha_1, alpha_1, alpha_1],
            parameter=parameter,
        )

    ############################################################################
    #                                Two sites                                 #
    ############################################################################

    for alpha_1 in range(0, M):
        for alpha_2 in range(0, M):
            if alpha_1 != alpha_2:
                nu_2 = (0, 0, 0)
            else:
                nu_2 = (1, 0, 0)
            # (2, 2) terms
            spinham.add(
                nus=[nu_2],
                alphas=[alpha_1, alpha_2],
                parameter=-np.eye(3),
                populate_equivalent=True,
                when_present="skip",
            )

            # (3, 2) terms
            parameter = np.ones((3, 3, 3))
            parameter[0, 0, 1] = -1
            spinham.add(
                nus=[(0, 0, 0), nu_2],
                alphas=[alpha_1, alpha_1, alpha_2],
                parameter=parameter,
                populate_equivalent=True,
                when_present="skip",
            )

            # (4, 2) terms
            parameter = np.ones((3, 3, 3, 3))
            parameter[0, 0, 0, 1] = -1
            spinham.add(
                nus=[(0, 0, 0), (0, 0, 0), nu_2],
                alphas=[alpha_1, alpha_1, alpha_1, alpha_2],
                parameter=parameter,
                populate_equivalent=True,
                when_present="skip",
            )

            # (4, 3) terms
            parameter = np.ones((3, 3, 3, 3))
            parameter[0, 1, 0, 1] = -1
            spinham.add(
                nus=[(0, 0, 0), nu_2, nu_2],
                alphas=[alpha_1, alpha_1, alpha_2, alpha_2],
                parameter=parameter,
                populate_equivalent=True,
                when_present="skip",
            )

    ############################################################################
    #                                Three sites                               #
    ############################################################################

    for alpha_1 in range(0, M):
        for alpha_2 in range(0, M):
            for alpha_3 in range(0, M):
                if alpha_1 == alpha_2:
                    nu_2 = (1, 0, 0)
                else:
                    nu_2 = (0, 0, 0)

                if alpha_1 != alpha_3 and alpha_2 != alpha_3:
                    nu_3 = (0, 0, 0)
                else:
                    nu_3 = (0, 1, 0)

                # (3, 3) terms
                parameter = np.ones((3, 3, 3))
                parameter[0, 1, 1] = -1
                spinham.add(
                    nus=[nu_2, nu_3],
                    alphas=[alpha_1, alpha_1, alpha_2],
                    parameter=parameter,
                    populate_equivalent=True,
                    when_present="skip",
                )

                # (4, 4) terms
                parameter = np.ones((3, 3, 3, 3))
                parameter[0, 1, 1, 1] = -1
                spinham.add(
                    nus=[(0, 0, 0), nu_2, nu_3],
                    alphas=[alpha_1, alpha_1, alpha_2, alpha_3],
                    parameter=parameter,
                    populate_equivalent=True,
                    when_present="skip",
                )

    ############################################################################
    #                                Four sites                                #
    ############################################################################

    for alpha_1 in range(0, M):
        for alpha_2 in range(0, M):
            for alpha_3 in range(0, M):
                for alpha_4 in range(0, M):
                    if alpha_1 == alpha_2:
                        nu_2 = (1, 0, 0)
                    else:
                        nu_2 = (0, 0, 0)

                    if alpha_1 != alpha_3 and alpha_2 != alpha_3:
                        nu_3 = (0, 0, 0)
                    else:
                        nu_3 = (0, 1, 0)

                    if alpha_1 != alpha_4 and alpha_2 != alpha_4 and alpha_3 != alpha_4:
                        nu_4 = (0, 0, 0)
                    else:
                        nu_4 = (0, 0, 1)

                # (4, 5) terms
                parameter = np.ones((3, 3, 3, 3))
                parameter[1, 1, 1, 1] = -1
                spinham.add(
                    nus=[(0, 0, 0), nu_2, nu_3, nu_4],
                    alphas=[alpha_1, alpha_2, alpha_3, alpha_4],
                    parameter=parameter,
                    populate_equivalent=True,
                    when_present="skip",
                )

    return spinham


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir

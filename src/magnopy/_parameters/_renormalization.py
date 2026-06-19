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

from magnopy._parameters._interaction_parameters import (
    _InteractionParameters,
    _get_specs,
)
from magnopy._spinham._convention import Convention


def _minus(nu):
    return tuple([-_ for _ in nu])


def _diff(nu1, nu2):
    return tuple([nu1[_] - nu2[_] for _ in range(3)])


def _get_corrections_1(nus, alphas, parameter, C1):
    return [[((0, 0, 0),), alphas, parameter * C1]]


def _get_corrections_2(nus, alphas, parameter, C2, spins):
    nu_2 = nus[0]
    alpha_1, alpha_2 = alphas
    return [
        # One spin
        [((0, 0, 0),), (alpha_1,), C2 * (parameter @ spins[alpha_2])],
        # One spin
        [((0, 0, 0),), (alpha_2,), C2 * (spins[alpha_1] @ parameter)],
        # Two spins
        [((0, 0, 0), nu_2), (alpha_1, alpha_2), C2 * parameter],
    ]


def _get_corrections_3(nus, alphas, parameter, C3, spins):
    nu_2 = nus[0]
    nu_3 = nus[1]
    alpha_1, alpha_2, alpha_3 = alphas
    return [
        # One spin
        [
            ((0, 0, 0),),
            (alpha_1,),
            C3 * np.einsum("ijk,j,k->i", parameter, spins[alpha_2], spins[alpha_3]),
        ],
        [
            ((0, 0, 0),),
            (alpha_2,),
            C3 * np.einsum("jik,j,k->i", parameter, spins[alpha_1], spins[alpha_3]),
        ],
        [
            ((0, 0, 0),),
            (alpha_3,),
            C3 * np.einsum("kji,j,k->i", parameter, spins[alpha_2], spins[alpha_1]),
        ],
        # Two spins
        [
            ((0, 0, 0), nu_2),
            (alpha_1, alpha_2),
            C3 * np.einsum("ijk,k->ij", parameter, spins[alpha_3]),
        ],
        [
            ((0, 0, 0), nu_3),
            (alpha_1, alpha_3),
            C3 * np.einsum("ikj,k->ij", parameter, spins[alpha_2]),
        ],
        [
            ((0, 0, 0), _diff(nu_3, nu_2)),
            (alpha_2, alpha_3),
            C3 * np.einsum("kij,k->ij", parameter, spins[alpha_1]),
        ],
        # Three spins
        [((0, 0, 0), nu_2, nu_3), (alpha_1, alpha_2, alpha_3), C3 * parameter],
    ]


def _get_corrections_4(nus, alphas, parameter, C4, spins):
    nu_2 = nus[0]
    nu_3 = nus[1]
    nu_4 = nus[2]
    alpha_1, alpha_2, alpha_3, alpha_4 = alphas
    return [
        # One spin
        [
            ((0, 0, 0),),
            (alpha_1,),
            C4
            * np.einsum(
                "ijkl,j,k,l->i",
                parameter,
                spins[alpha_2],
                spins[alpha_3],
                spins[alpha_4],
            ),
        ],
        [
            ((0, 0, 0),),
            (alpha_2,),
            C4
            * np.einsum(
                "jikl,j,k,l->i",
                parameter,
                spins[alpha_1],
                spins[alpha_3],
                spins[alpha_4],
            ),
        ],
        [
            ((0, 0, 0),),
            (alpha_3,),
            C4
            * np.einsum(
                "kjil,j,k,l->i",
                parameter,
                spins[alpha_2],
                spins[alpha_1],
                spins[alpha_4],
            ),
        ],
        [
            ((0, 0, 0),),
            (alpha_4,),
            C4
            * np.einsum(
                "ljki,j,k,l->i",
                parameter,
                spins[alpha_2],
                spins[alpha_3],
                spins[alpha_1],
            ),
        ],
        # Two spins
        [
            ((0, 0, 0), nu_2),
            (alpha_1, alpha_2),
            C4 * np.einsum("ijkl,k,l->ij", parameter, spins[alpha_3], spins[alpha_4]),
        ],
        [
            ((0, 0, 0), nu_3),
            (alpha_1, alpha_3),
            C4 * np.einsum("ikjl,k,l->ij", parameter, spins[alpha_2], spins[alpha_4]),
        ],
        [
            ((0, 0, 0), nu_4),
            (alpha_1, alpha_4),
            C4 * np.einsum("ilkj,k,l->ij", parameter, spins[alpha_3], spins[alpha_2]),
        ],
        [
            ((0, 0, 0), _diff(nu_3, nu_2)),
            (alpha_2, alpha_3),
            C4 * np.einsum("kijl,k,l->ij", parameter, spins[alpha_1], spins[alpha_4]),
        ],
        [
            ((0, 0, 0), _diff(nu_4, nu_2)),
            (alpha_2, alpha_4),
            C4 * np.einsum("likj,k,l->ij", parameter, spins[alpha_3], spins[alpha_1]),
        ],
        [
            ((0, 0, 0), _diff(nu_4, nu_3)),
            (alpha_3, alpha_4),
            C4 * np.einsum("klij,k,l->ij", parameter, spins[alpha_1], spins[alpha_2]),
        ],
        # Three spins
        [
            ((0, 0, 0), nu_2, nu_3),
            (alpha_1, alpha_2, alpha_3),
            C4 * np.einsum("ijkl,l->ijk", parameter, spins[alpha_4]),
        ],
        [
            ((0, 0, 0), nu_2, nu_4),
            (alpha_1, alpha_2, alpha_4),
            C4 * np.einsum("ijlk,l->ijk", parameter, spins[alpha_3]),
        ],
        [
            ((0, 0, 0), nu_4, nu_3),
            (alpha_1, alpha_4, alpha_3),
            C4 * np.einsum("ilkj,l->ijk", parameter, spins[alpha_2]),
        ],
        [
            ((0, 0, 0), _diff(nu_2, nu_4), _diff(nu_3, nu_4)),
            (alpha_4, alpha_2, alpha_3),
            C4 * np.einsum("ljki,l->ijk", parameter, spins[alpha_1]),
        ],
        # Four spins
        [
            ((0, 0, 0), nu_2, nu_3, nu_4),
            (alpha_1, alpha_2, alpha_3, alpha_4),
            C4 * parameter,
        ],
    ]


def _renormalized_parameters(
    parameters: _InteractionParameters,
    convention: Convention,
    spin_directions,
    spin_values,
) -> _InteractionParameters:
    """
    Renormalizes the interaction parameters as described in supplementary note 6 of
    |paper-2026|_.

    Parameters
    ----------
    parameters : _InteractionParameters
        The interaction parameters to be renormalized.

    convention : Convention
        The convention of the parameters. It is the user's responsibility to ensure that
        ``convention`` corresponds to ``parameters``.

    spin_directions : (M, 3) |array-like|_
        Directions of spin vectors. Only directions of vectors are used, modulus is
        ignored. The indices of the spin_directions shall be compatible with ``alphas``
        of the ``parameters``.

    spin_values : (M, ) |array-like|_
        Spin quantum numbers. The indices of the spin_values shall be compatible with
        ``alphas`` of the ``parameters``.

    Returns
    -------
    _InteractionParameters
        The renormalized interaction parameters.
    """

    spin_directions = np.array(spin_directions, dtype=float)

    spin_directions = (
        spin_directions / np.linalg.norm(spin_directions, axis=1)[:, np.newaxis]
    )

    spin_values = np.array(spin_values, dtype=float)

    spins = spin_values[:, np.newaxis] * spin_directions

    renormalized_parameters = _InteractionParameters()

    for (n, p_n, nus, alphas), parameter in parameters._container:
        if n == 1:
            corrections = _get_corrections_1(
                nus=nus, alphas=alphas, parameter=parameter, C1=convention.c1
            )

        elif n == 2:
            # Get C2
            if p_n == 1:
                C2 = convention.c21
            elif p_n == 2:
                C2 = convention.c22
            else:
                raise ValueError(f"Invalid p_n={p_n} for n=2. Expected p_n=1 or p_n=2.")

            corrections = _get_corrections_2(
                nus=nus, alphas=alphas, parameter=parameter, C2=C2, spins=spins
            )

        elif n == 3:
            if p_n == 1:
                C3 = convention.c31
            elif p_n == 2:
                C3 = convention.c32
            elif p_n == 3:
                C3 = convention.c33
            else:
                raise ValueError(
                    f"Invalid p_n={p_n} for n=3. Expected p_n=1, p_n=2 or p_n=3."
                )

            corrections = _get_corrections_3(
                nus=nus, alphas=alphas, parameter=parameter, C3=C3, spins=spins
            )

        elif n == 4:
            if p_n == 1:
                C4 = convention.c41
            elif p_n == 2:
                C4 = convention.c42
            elif p_n == 3:
                C4 = convention.c43
            elif p_n == 4:
                C4 = convention.c44
            elif p_n == 5:
                C4 = convention.c45
            else:
                raise ValueError(
                    f"Invalid p_n={p_n} for n=4. Expected p_n=1, p_n=2, p_n=3, p_n=4 or p_n=5."
                )

            corrections = _get_corrections_4(
                nus=nus, alphas=alphas, parameter=parameter, C4=C4, spins=spins
            )
        else:
            raise ValueError(f"Invalid n={n}. Expected n=1, n=2, n=3 or n=4.")

        for nus, alphas, parameter in corrections:
            specs = _get_specs(nus=nus, alphas=alphas)
            renormalized_parameters.add(
                specs=specs, parameter=parameter, when_present="sum"
            )

    return renormalized_parameters

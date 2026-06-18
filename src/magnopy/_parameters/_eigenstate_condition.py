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

from magnopy._parameters._interaction_parameters import _InteractionParametersIterator
from magnopy._parameters._renormalization import _renormalized_parameters
from magnopy._local_rf import span_local_rfs
from magnopy._spinham._convention import Convention

__all__ = ["is_eigenstate"]


def is_eigenstate(spinham, spin_directions, energy_tolerance=1e-8):
    r"""
    Checks all eigenstate conditions as described in the supplementary note 4 of
    |paper-2026|_ (eqs. S.40-S.50).

    Parameters
    ----------
    spinham : :py:class:`magnopy.SpinHamiltonian`
        Spin Hamiltonian

    spin_directions : (M, 3) |array-like|_
        Directional vectors. M is an amount of atoms in ``spinham.magnetic_atoms``.

    energy_tolerance : float, default 1e-8
        Numerical accuracy for comparing energy values to zero. Given in the same units as
        ``spinham.units``.

    Returns
    -------
    result : bool
        ``True`` if ``spin_directions`` describe an eigenstate of ``spinham``. ``False``
        otherwise.
    """

    spin_values = np.array(spinham.magnetic_atoms.spins, dtype=float)

    x, y, z = span_local_rfs(directional_vectors=spin_directions, hybridize=False)
    p = x + 1j * y

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
    )

    initial_convention = spinham.convention
    spinham.convention = convention
    parameters = spinham._parameters.copy()
    spinham.convention = initial_convention

    for i, ((n, p_n, nus, alphas), _) in enumerate(parameters._container):
        alphas = tuple(spinham.map_to_magnetic[alpha] for alpha in alphas)
        parameters._container[i][0] = (n, p_n, nus, alphas)

    renormalized_parameters = _renormalized_parameters(
        parameters=parameters,
        convention=convention,
        spin_directions=spin_directions,
        spin_values=spin_values,
    )

    checks = [
        _check_S_40,
        _check_S_41,
        _check_S_42,
        _check_S_43,
        _check_S_44,
        _check_S_45,
        _check_S_46,
        _check_S_47,
        _check_S_48,
        _check_S_49,
        _check_S_50,
    ]

    for check in checks:
        if not check(
            renormalized_parameters=renormalized_parameters,
            p=p,
            z=z,
            spin_values=spin_values,
            energy_tolerance=energy_tolerance,
        ):
            return False

    return True


def _check_S_50(
    renormalized_parameters, p, z, spin_values, energy_tolerance=1e-8
) -> bool:
    r"""

    Check eigenstate condition from eq. S.50 of the supplementary material of |paper-2026|_.

    Parameters
    ----------
    renormalized_parameters
        Renormalized interaction parameters.
    p : (M, 3) :numpy`ndarray`
        Complex spin components of the local reference frame.
    z : (M, 3) :numpy`ndarray`
        Directional vectors of the local reference frame.
    spin_values : (M, 3) :numpy`ndarray`
        Spin values.
    energy_tolerance : float, default 1e-8
        Tolerance for energy differences.
    """

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=5
    ):
        alpha_1, alpha_2, alpha_3, alpha_4 = alphas
        u_11 = np.einsum(
            "ijkl,i,j,k,l",
            parameter,
            p[alpha_1],
            p[alpha_2],
            p[alpha_3],
            p[alpha_4],
        )

        if abs(u_11) > energy_tolerance:
            return False

    return True


def _check_S_49(
    renormalized_parameters, p, z, spin_values, energy_tolerance=1e-8
) -> bool:
    r"""

    Check eigenstate condition from eq. S.49 of the supplementary material of |paper-2026|_.

    Parameters
    ----------
    renormalized_parameters
        Renormalized interaction parameters.
    p : (M, 3) :numpy`ndarray`
        Complex spin components of the local reference frame.
    z : (M, 3) :numpy`ndarray`
        Directional vectors of the local reference frame.
    spin_values : (M, 3) :numpy`ndarray`
        Spin values.
    energy_tolerance : float, default 1e-8
        Tolerance for energy differences.
    """

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=4
    ):
        if ((0, 0, 0), alphas[0]) == (nus[0], alphas[1]):
            alpha_1, alpha_2, alpha_3 = alphas[1:]

            if round(2 * spin_values[alpha_1]) > 1:
                u_10 = np.einsum(
                    "ijkl,i,j,k,l",
                    parameter,
                    p[alpha_1],
                    p[alpha_1],
                    p[alpha_2],
                    p[alpha_3],
                )

                if abs(u_10) > energy_tolerance:
                    return False

    return True


def _check_S_48(
    renormalized_parameters, p, z, spin_values, energy_tolerance=1e-8
) -> bool:
    r"""

    Check eigenstate condition from eq. S.48 of the supplementary material of |paper-2026|_.

    Parameters
    ----------
    renormalized_parameters
        Renormalized interaction parameters.
    p : (M, 3) :numpy`ndarray`
        Complex spin components of the local reference frame.
    z : (M, 3) :numpy`ndarray`
        Directional vectors of the local reference frame.
    spin_values : (M, 3) :numpy`ndarray`
        Spin values.
    energy_tolerance : float, default 1e-8
        Tolerance for energy differences.
    """

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=3
    ):
        if ((0, 0, 0), alphas[0]) == (nus[0], alphas[1]):
            alpha_1 = alphas[0]
            alpha_2 = alphas[2]

            if (
                round(2 * spin_values[alpha_1]) > 1
                and round(2 * spin_values[alpha_2]) > 1
            ):
                u_9 = np.einsum(
                    "ijkl,i,j,k,l",
                    parameter,
                    p[alpha_1],
                    p[alpha_1],
                    p[alpha_2],
                    p[alpha_2],
                )

                if abs(u_9) > energy_tolerance:
                    return False

    return True


def _check_S_47(
    renormalized_parameters, p, z, spin_values, energy_tolerance=1e-8
) -> bool:
    r"""

    Check eigenstate condition from eq. S.47 of the supplementary material of |paper-2026|_.

    Parameters
    ----------
    renormalized_parameters
        Renormalized interaction parameters.
    p : (M, 3) :numpy`ndarray`
        Complex spin components of the local reference frame.
    z : (M, 3) :numpy`ndarray`
        Directional vectors of the local reference frame.
    spin_values : (M, 3) :numpy`ndarray`
        Spin values.
    energy_tolerance : float, default 1e-8
        Tolerance for energy differences.
    """

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=2
    ):
        if ((0, 0, 0), alphas[0]) == (nus[0], alphas[1]) and ((0, 0, 0), alphas[0]) == (
            nus[1],
            alphas[2],
        ):
            alpha_1 = alphas[0]
            alpha_2 = alphas[3]

            if round(2 * spin_values[alpha_1]) > 2:
                u_8 = np.einsum(
                    "ijkl,i,j,k,l",
                    parameter,
                    p[alpha_1],
                    p[alpha_1],
                    p[alpha_1],
                    p[alpha_2],
                )

                if abs(u_8) > energy_tolerance:
                    return False

    return True


def _check_S_46(
    renormalized_parameters, p, z, spin_values, energy_tolerance=1e-8
) -> bool:
    r"""

    Check eigenstate condition from eq. S.46 of the supplementary material of |paper-2026|_.

    Parameters
    ----------
    renormalized_parameters
        Renormalized interaction parameters.
    p : (M, 3) :numpy`ndarray`
        Complex spin components of the local reference frame.
    z : (M, 3) :numpy`ndarray`
        Directional vectors of the local reference frame.
    spin_values : (M, 3) :numpy`ndarray`
        Spin values.
    energy_tolerance : float, default 1e-8
        Tolerance for energy differences.
    """

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=1
    ):
        alpha_1 = alphas[0]

        if round(2 * spin_values[alpha_1]) > 3:
            u_7 = np.einsum(
                "ijkl,i,j,k,l",
                parameter,
                p[alpha_1],
                p[alpha_1],
                p[alpha_1],
                p[alpha_1],
            )

            if abs(u_7) > energy_tolerance:
                return False

    return True


def _check_S_45(
    renormalized_parameters, p, z, spin_values, energy_tolerance=1e-8
) -> bool:
    r"""

    Check eigenstate condition from eq. S.45 of the supplementary material of |paper-2026|_.

    Parameters
    ----------
    renormalized_parameters
        Renormalized interaction parameters.
    p : (M, 3) :numpy`ndarray`
        Complex spin components of the local reference frame.
    z : (M, 3) :numpy`ndarray`
        Directional vectors of the local reference frame.
    spin_values : (M, 3) :numpy`ndarray`
        Spin values.
    energy_tolerance : float, default 1e-8
        Tolerance for energy differences.
    """

    u_6 = {}

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=3, p_n=3
    ):
        nu_2, nu_3 = nus
        alpha_1, alpha_2, alpha_3 = alphas
        key = (nu_2, nu_3, alpha_1, alpha_2, alpha_3)
        if key not in u_6:
            u_6[key] = 0

        u_6[key] += np.einsum(
            "ijk,i,j,k",
            parameter,
            p[alpha_1],
            p[alpha_2],
            p[alpha_3],
        )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=4
    ):
        if (nus[1], alphas[2]) == (nus[2], alphas[3]):
            nu_2 = nus[0]
            nu_3 = nus[1]
            alpha_1, alpha_2, alpha_3 = alphas[:3]
            key = (nu_2, nu_3, alpha_1, alpha_2, alpha_3)
            if key not in u_6:
                u_6[key] = 0

            u_6[key] -= 6 * np.einsum(
                "ijkl,i,j,k,l",
                parameter,
                p[alpha_1],
                p[alpha_2],
                z[alpha_3],
                p[alpha_3],
            )

    for key in u_6:
        if abs(u_6[key]) > energy_tolerance:
            return False

    return True


def _check_S_44(
    renormalized_parameters, p, z, spin_values, energy_tolerance=1e-8
) -> bool:
    r"""

    Check eigenstate condition from eq. S.44 of the supplementary material of |paper-2026|_.

    Parameters
    ----------
    renormalized_parameters
        Renormalized interaction parameters.
    p : (M, 3) :numpy`ndarray`
        Complex spin components of the local reference frame.
    z : (M, 3) :numpy`ndarray`
        Directional vectors of the local reference frame.
    spin_values : (M, 3) :numpy`ndarray`
        Spin values.
    energy_tolerance : float, default 1e-8
        Tolerance for energy differences.
    """

    u_5 = {}

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=3, p_n=2
    ):
        if ((0, 0, 0), alphas[0]) == (nus[0], alphas[1]):
            nu_2 = nus[1]
            alpha_1 = alphas[0]
            alpha_2 = alphas[2]

            if round(2 * spin_values[alpha_1]) > 1:
                key = (nu_2, alpha_1, alpha_2)
                if key not in u_5:
                    u_5[key] = 0

                u_5[key] += np.einsum(
                    "ijk,i,j,k",
                    parameter,
                    p[alpha_1],
                    p[alpha_1],
                    p[alpha_2],
                )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=2
    ):
        if ((0, 0, 0), alphas[0]) == (nus[0], alphas[1]) and ((0, 0, 0), alphas[0]) == (
            nus[1],
            alphas[2],
        ):
            nu_2 = nus[2]
            alpha_1 = alphas[0]
            alpha_2 = alphas[3]

            if round(2 * spin_values[alpha_1]) > 1:
                key = (nu_2, alpha_1, alpha_2)
                if key not in u_5:
                    u_5[key] = 0

                medium_matrix = 2 * np.einsum("i,j->ij", z[alpha_1], p[alpha_1])
                medium_matrix += np.einsum("i,j->ij", p[alpha_1], z[alpha_1])

                u_5[key] -= 4 * np.einsum(
                    "ijkl,ij,k,l",
                    parameter,
                    medium_matrix,
                    p[alpha_1],
                    p[alpha_2],
                )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=3
    ):
        if ((0, 0, 0), alphas[0]) == (nus[0], alphas[1]):
            nu_2 = nus[1]
            alpha_1 = alphas[0]
            alpha_2 = alphas[2]

            if round(2 * spin_values[alpha_1]) > 1:
                key = (nu_2, alpha_1, alpha_2)
                if key not in u_5:
                    u_5[key] = 0

                u_5[key] -= 6 * np.einsum(
                    "ijkl,i,j,k,l",
                    parameter,
                    p[alpha_1],
                    p[alpha_1],
                    z[alpha_2],
                    p[alpha_2],
                )

    for key in u_5:
        if abs(u_5[key]) > energy_tolerance:
            return False

    return True


def _check_S_43(
    renormalized_parameters, p, z, spin_values, energy_tolerance=1e-8
) -> bool:
    r"""

    Check eigenstate condition from eq. S.43 of the supplementary material of |paper-2026|_.

    Parameters
    ----------
    renormalized_parameters
        Renormalized interaction parameters.
    p : (M, 3) :numpy`ndarray`
        Complex spin components of the local reference frame.
    z : (M, 3) :numpy`ndarray`
        Directional vectors of the local reference frame.
    spin_values : (M, 3) :numpy`ndarray`
        Spin values.
    energy_tolerance : float, default 1e-8
        Tolerance for energy differences.
    """

    u_4 = {}

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=3, p_n=1
    ):
        alpha_1 = alphas[0]

        if round(2 * spin_values[alpha_1]) > 2:
            key = alpha_1
            if key not in u_4:
                u_4[key] = 0

            u_4[key] += np.einsum(
                "ijk,i,j,k",
                parameter,
                p[alpha_1],
                p[alpha_1],
                p[alpha_1],
            )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=1
    ):
        alpha_1 = alphas[0]

        if round(2 * spin_values[alpha_1]) > 2:
            key = alpha_1
            if key not in u_4:
                u_4[key] = 0

            medium_matrix = 3 * np.einsum(
                "i,j,k->ijk", z[alpha_1], p[alpha_1], p[alpha_1]
            )
            medium_matrix += 2 * np.einsum(
                "i,j,k->ijk", p[alpha_1], z[alpha_1], p[alpha_1]
            )
            medium_matrix += np.einsum("i,j,k->ijk", p[alpha_1], p[alpha_1], z[alpha_1])

            u_4[key] -= np.einsum("ijkl,ijk,l", parameter, medium_matrix, p[alpha_1])

    for key in u_4:
        if abs(u_4[key]) > energy_tolerance:
            return False

    return True


def _check_S_42(
    renormalized_parameters, p, z, spin_values, energy_tolerance=1e-8
) -> bool:
    r"""

    Check eigenstate condition from eq. S.42 of the supplementary material of |paper-2026|_.

    Parameters
    ----------
    renormalized_parameters
        Renormalized interaction parameters.
    p : (M, 3) :numpy`ndarray`
        Complex spin components of the local reference frame.
    z : (M, 3) :numpy`ndarray`
        Directional vectors of the local reference frame.
    spin_values : (M, 3) :numpy`ndarray`
        Spin values.
    energy_tolerance : float, default 1e-8
        Tolerance for energy differences.
    """

    u_3 = {}
    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=2, p_n=2
    ):
        nu_2 = nus[0]
        alpha_1, alpha_2 = alphas
        key = (nu_2, alpha_1, alpha_2)
        if key not in u_3:
            u_3[key] = 0

        u_3[key] += np.einsum(
            "ij,i,j",
            parameter,
            p[alpha_1],
            p[alpha_2],
        )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=3, p_n=2
    ):
        if (nus[0], alphas[1]) == (nus[1], alphas[2]):
            nu_2 = nus[0]
            alpha_1, alpha_2 = alphas[:2]
            key = (nu_2, alpha_1, alpha_2)
            if key not in u_3:
                u_3[key] = 0

            u_3[key] -= 3 * np.einsum(
                "ijk,i,j,k",
                parameter,
                p[alpha_1],
                z[alpha_2],
                p[alpha_2],
            )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=2
    ):
        if ((0, 0, 0), alphas[0]) == (nus[0], alphas[1]) and ((0, 0, 0), alphas[0]) == (
            nus[1],
            alphas[2],
        ):
            nu_2 = nus[2]
            alpha_1, alpha_2 = alphas[0], alphas[3]
            key = (nu_2, alpha_1, alpha_2)
            if key not in u_3:
                u_3[key] = 0

            medium_matrix = np.einsum("i,j->ij", z[alpha_1], z[alpha_1])

            if round(2 * spin_values[alpha_1]) > 1:
                medium_matrix += (spin_values[alpha_1] - 0.5) * np.einsum(
                    "i,j->ij", np.conjugate(p[alpha_1]), p[alpha_1]
                )

            medium_matrix += (
                0.5
                * spin_values[alpha_1]
                * np.einsum("i,j->ij", p[alpha_1], np.conjugate(p[alpha_1]))
            )

            u_3[key] += 4 * np.einsum(
                "ijkl,ij,k,l",
                parameter,
                medium_matrix,
                p[alpha_1],
                p[alpha_2],
            )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=3
    ):
        if ((0, 0, 0), alphas[0]) == (nus[0], alphas[1]):
            nu_2 = nus[1]
            alpha_1, alpha_2 = alphas[0], alphas[2]
            key = (nu_2, alpha_1, alpha_2)
            if key not in u_3:
                u_3[key] = 0

            u_3[key] += 3 * np.einsum(
                "ijkl,i,j,k,l",
                parameter,
                z[alpha_1],
                p[alpha_1],
                z[alpha_2],
                p[alpha_2],
            )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=4
    ):
        if (nus[1], alphas[2]) == (nus[2], alphas[3]):
            nu_2 = nus[0]
            alpha_1, alpha_2, alpha_3 = alphas[:3]

            key = (nu_2, alpha_1, alpha_2)
            if key not in u_3:
                u_3[key] = 0

            u_3[key] += (
                3
                * spin_values[alpha_3]
                * np.einsum(
                    "ijkl,i,j,k,l",
                    parameter,
                    p[alpha_1],
                    p[alpha_2],
                    np.conjugate(p[alpha_3]),
                    p[alpha_3],
                )
            )

    for key in u_3:
        if abs(u_3[key]) > energy_tolerance:
            return False

    return True


def _check_S_41(
    renormalized_parameters, p, z, spin_values, energy_tolerance=1e-8
) -> bool:
    r"""

    Check eigenstate condition from eq. S.41 of the supplementary material of |paper-2026|_.

    Parameters
    ----------
    renormalized_parameters
        Renormalized interaction parameters.
    p : (M, 3) :numpy`ndarray`
        Complex spin components of the local reference frame.
    z : (M, 3) :numpy`ndarray`
        Directional vectors of the local reference frame.
    spin_values : (M, 3) :numpy`ndarray`
        Spin values.
    energy_tolerance : float, default 1e-8
        Tolerance for energy differences.
    """

    u_2 = {}

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=2, p_n=1
    ):
        alpha_1 = alphas[0]

        if round(2 * spin_values[alpha_1]) > 1:
            key = alpha_1
            if key not in u_2:
                u_2[key] = 0

            u_2[key] += p[alpha_1] @ parameter @ p[alpha_1]

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=3, p_n=1
    ):
        alpha_1 = alphas[0]

        if round(2 * spin_values[alpha_1]) > 1:
            key = alpha_1
            if key not in u_2:
                u_2[key] = 0

            medium_matrix = 2 * np.einsum("i,j->ij", z[alpha_1], p[alpha_1])
            medium_matrix += np.einsum("i,j->ij", p[alpha_1], z[alpha_1])

            u_2[key] -= np.einsum(
                "ijk,ij,k",
                parameter,
                medium_matrix,
                p[alpha_1],
            )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=1
    ):
        alpha_1 = alphas[0]

        if round(2 * spin_values[alpha_1]) > 1:
            key = alpha_1
            if key not in u_2:
                u_2[key] = 0

            medium_matrix = 4 * np.einsum(
                "i,j,k->ijk", z[alpha_1], z[alpha_1], p[alpha_1]
            )
            medium_matrix += 2 * np.einsum(
                "i,j,k->ijk", z[alpha_1], p[alpha_1], z[alpha_1]
            )
            medium_matrix += np.einsum("i,j,k->ijk", p[alpha_1], z[alpha_1], z[alpha_1])
            medium_matrix += (
                0.5
                * spin_values[alpha_1]
                * np.einsum(
                    "i,j,k->ijk", p[alpha_1], p[alpha_1], np.conjugate(p[alpha_1])
                )
            )
            medium_matrix += (spin_values[alpha_1] - 0.5) * np.einsum(
                "i,j,k->ijk", p[alpha_1], np.conjugate(p[alpha_1]), p[alpha_1]
            )
            medium_matrix += (
                1.5
                * (spin_values[alpha_1] - 1)
                * np.einsum(
                    "i,j,k->ijk", np.conjugate(p[alpha_1]), p[alpha_1], p[alpha_1]
                )
            )

            u_2[key] += np.einsum(
                "ijkl,ijk,l",
                parameter,
                medium_matrix,
                p[alpha_1],
            )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=3
    ):
        if ((0, 0, 0), alphas[0]) == (nus[0], alphas[1]):
            alpha_1 = alphas[0]
            alpha_2 = alphas[2]

            if round(2 * spin_values[alpha_1]) > 1:
                key = alpha_1
                if key not in u_2:
                    u_2[key] = 0

                u_2[key] += (
                    3
                    * spin_values[alpha_2]
                    * np.einsum(
                        "ijkl,i,j,k,l",
                        parameter,
                        p[alpha_1],
                        p[alpha_1],
                        np.conjugate(p[alpha_2]),
                        p[alpha_2],
                    )
                )

    for key in u_2:
        if abs(u_2[key]) > energy_tolerance:
            return False

    return True


def _check_S_40(
    renormalized_parameters, p, z, spin_values, energy_tolerance=1e-8
) -> bool:
    r"""

    Check eigenstate condition from eq. S.40 of the supplementary material of |paper-2026|_.

    Parameters
    ----------
    renormalized_parameters
        Renormalized interaction parameters.
    p : (M, 3) :numpy`ndarray`
        Complex spin components of the local reference frame.
    z : (M, 3) :numpy`ndarray`
        Directional vectors of the local reference frame.
    spin_values : (M, 3) :numpy`ndarray`
        Spin values.
    energy_tolerance : float, default 1e-8
        Tolerance for energy differences.
    """

    u_1 = {}

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=1, p_n=1
    ):
        alpha_1 = alphas[0]

        key = alpha_1
        if key not in u_1:
            u_1[key] = 0

        u_1[key] += parameter @ p[alpha_1]

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=2, p_n=1
    ):
        alpha_1 = alphas[0]

        key = alpha_1
        if key not in u_1:
            u_1[key] = 0

        u_1[key] -= z[alpha_1] @ parameter @ p[alpha_1]

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=3, p_n=1
    ):
        alpha_1 = alphas[0]

        key = alpha_1
        if key not in u_1:
            u_1[key] = 0

        medium_matrix = np.einsum("i,j->ij", z[alpha_1], z[alpha_1])
        medium_matrix += (
            0.5
            * spin_values[alpha_1]
            * np.einsum("i,j->ij", p[alpha_1], np.conjugate(p[alpha_1]))
        )
        if round(2 * spin_values[alpha_1]) > 1:
            medium_matrix += (spin_values[alpha_1] - 0.5) * np.einsum(
                "i,j->ij", np.conjugate(p[alpha_1]), p[alpha_1]
            )

        u_1[key] += np.einsum(
            "ijk,ij,k",
            parameter,
            medium_matrix,
            p[alpha_1],
        )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=3, p_n=2
    ):
        if (nus[0], alphas[1]) == (nus[1], alphas[2]):
            alpha_1 = alphas[0]
            alpha_2 = alphas[1]

            key = alpha_1
            if key not in u_1:
                u_1[key] = 0

            u_1[key] += (
                1.5
                * spin_values[alpha_2]
                * np.einsum(
                    "ijk,i,j,k",
                    parameter,
                    p[alpha_1],
                    np.conjugate(p[alpha_2]),
                    p[alpha_2],
                )
            )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=1
    ):
        alpha_1 = alphas[0]

        key = alpha_1
        if key not in u_1:
            u_1[key] = 0

        medium_matrix = np.einsum("i,j,k->ijk", z[alpha_1], z[alpha_1], z[alpha_1])
        medium_matrix += (
            0.5
            * spin_values[alpha_1]
            * (
                np.einsum("i,j,k->ijk", p[alpha_1], p[alpha_1], z[alpha_1])
                + np.einsum("i,j,k->ijk", z[alpha_1], p[alpha_1], p[alpha_1])
            )
        )

        if round(2 * spin_values[alpha_1]) > 1:
            medium_matrix += (spin_values[alpha_1] - 0.5) * (
                2
                * np.einsum(
                    "i,j,k->ijk", np.conjugate(p[alpha_1]), z[alpha_1], p[alpha_1]
                )
                + np.einsum(
                    "i,j,k->ijk", z[alpha_1], np.conjugate(p[alpha_1]), p[alpha_1]
                )
                + np.einsum(
                    "i,j,k->ijk", np.conjugate(p[alpha_1]), p[alpha_1], z[alpha_1]
                )
            )

        u_1[key] -= np.einsum(
            "ijkl,ijk,l",
            parameter,
            medium_matrix,
            p[alpha_1],
        )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=2
    ):
        if (nus[0], alphas[1]) == (nus[1], alphas[2]) and (nus[0], alphas[1]) == (
            nus[2],
            alphas[3],
        ):
            alpha_1 = alphas[0]
            alpha_2 = alphas[1]

            key = alpha_1
            if key not in u_1:
                u_1[key] = 0

            u_1[key] += (
                2
                * spin_values[alpha_2]
                * np.einsum(
                    "ijkl,i,j,k,l",
                    parameter,
                    p[alpha_1],
                    np.conjugate(p[alpha_2]),
                    z[alpha_2],
                    p[alpha_2],
                )
            )

    for nus, alphas, parameter in _InteractionParametersIterator(
        parameters=renormalized_parameters, n=4, p_n=3
    ):
        if ((0, 0, 0), alphas[0]) == (nus[0], alphas[1]):
            alpha_1 = alphas[0]
            alpha_2 = alphas[2]

            key = alpha_1
            if key not in u_1:
                u_1[key] = 0

            u_1[key] += (
                3
                * spin_values[alpha_2]
                * np.einsum(
                    "ijkl,i,j,k,l",
                    parameter,
                    z[alpha_1],
                    p[alpha_1],
                    np.conjugate(p[alpha_2]),
                    p[alpha_2],
                )
            )

    for key in u_1:
        if abs(u_1[key]) > energy_tolerance:
            return False

    return True

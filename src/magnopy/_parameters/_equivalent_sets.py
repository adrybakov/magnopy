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

from magnopy._parameters._interaction_parameters import _get_specs
from magnopy._parameters._interaction_parameters import _InteractionParameters

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _minus(nu):
    return tuple([-_ for _ in nu])


def _diff(nu1, nu2):
    return tuple([nu1[_] - nu2[_] for _ in range(3)])


def _get_equivalent_2_2(nus, alphas, parameter=None):
    """
    See S.21 of SI of paper-2026
    """
    nu_2 = nus[0]
    alpha_1 = alphas[0]
    alpha_2 = alphas[1]

    if ((0, 0, 0), alpha_1) == (nu_2, alpha_2):
        raise ValueError("Invalid indices for (1+1) case.")

    versions_nus = [
        (nu_2,),
        (_minus(nu_2),),
    ]

    versions_alphas = [
        (alpha_1, alpha_2),
        (alpha_2, alpha_1),
    ]

    if parameter is None:
        versions_parameter = [None] * 2
    else:
        versions_parameter = [
            parameter.copy(),
            np.transpose(parameter.copy()),
        ]

    parameters = list(zip(versions_nus, versions_alphas, versions_parameter))
    parameters.sort(key=lambda x: x[:-1], reverse=True)

    return parameters


def _get_equivalent_3_2(nus, alphas, parameter=None):
    """
    See S.22 of SI of paper-2026
    """
    r1 = ((0, 0, 0), alphas[0])
    r2 = (nus[0], alphas[1])
    r3 = (nus[1], alphas[2])
    if r1 == r2 and r1 != r3:
        nu_2 = nus[1]
        alpha_1 = alphas[0]
        alpha_2 = alphas[2]
    elif r1 == r3 and r1 != r2:
        nu_2 = nus[0]
        alpha_1 = alphas[0]
        alpha_2 = alphas[1]
        if parameter is not None:
            parameter = np.transpose(parameter, (0, 2, 1))
    elif r2 == r3 and r2 != r1:
        nu_2 = _minus(nus[0])
        alpha_1 = alphas[1]
        alpha_2 = alphas[0]
        if parameter is not None:
            parameter = np.transpose(parameter, (1, 2, 0))
    else:
        raise ValueError("Invalid indices for (2+1) case.")

    versions_nus = [
        ((0, 0, 0), nu_2),
        (nu_2, (0, 0, 0)),
        (_minus(nu_2), _minus(nu_2)),
    ]

    versions_alphas = [
        (alpha_1, alpha_1, alpha_2),
        (alpha_1, alpha_2, alpha_1),
        (alpha_2, alpha_1, alpha_1),
    ]

    if parameter is None:
        versions_parameter = [None] * 3
    else:
        versions_parameter = [
            parameter.copy(),
            np.transpose(parameter.copy(), (0, 2, 1)),
            np.transpose(parameter.copy(), (2, 0, 1)),
        ]

    parameters = list(zip(versions_nus, versions_alphas, versions_parameter))
    parameters.sort(key=lambda x: x[:-1], reverse=True)

    return parameters


def _get_equivalent_3_3(nus, alphas, parameter=None):
    """
    See S.23 of SI of paper-2026
    """

    nu_2 = nus[0]
    nu_3 = nus[1]
    alpha_1 = alphas[0]
    alpha_2 = alphas[1]
    alpha_3 = alphas[2]

    r1 = ((0, 0, 0), alpha_1)
    r2 = (nu_2, alpha_2)
    r3 = (nu_3, alpha_3)
    if r1 == r2 or r1 == r3 or r2 == r3:
        raise ValueError("Invalid indices for (1+1+1) case.")

    versions_nus = [
        (nu_2, nu_3),
        (nu_3, nu_2),
        (_minus(nu_2), _diff(nu_3, nu_2)),
        (_diff(nu_3, nu_2), _minus(nu_2)),
        (_minus(nu_3), _diff(nu_2, nu_3)),
        (_diff(nu_2, nu_3), _minus(nu_3)),
    ]

    versions_alphas = [
        (alpha_1, alpha_2, alpha_3),
        (alpha_1, alpha_3, alpha_2),
        (alpha_2, alpha_1, alpha_3),
        (alpha_2, alpha_3, alpha_1),
        (alpha_3, alpha_1, alpha_2),
        (alpha_3, alpha_2, alpha_1),
    ]

    if parameter is None:
        versions_parameter = [None] * 6
    else:
        versions_parameter = [
            parameter.copy(),
            np.transpose(parameter.copy(), (0, 2, 1)),
            np.transpose(parameter.copy(), (1, 0, 2)),
            np.transpose(parameter.copy(), (1, 2, 0)),
            np.transpose(parameter.copy(), (2, 0, 1)),
            np.transpose(parameter.copy(), (2, 1, 0)),
        ]

    parameters = list(zip(versions_nus, versions_alphas, versions_parameter))
    parameters.sort(key=lambda x: x[:-1], reverse=True)

    return parameters


def _get_equivalent_4_2(nus, alphas, parameter=None):
    """
    See S.24 of SI of paper-2026
    """
    r1 = ((0, 0, 0), alphas[0])
    r2 = (nus[0], alphas[1])
    r3 = (nus[1], alphas[2])
    r4 = (nus[2], alphas[3])
    if r1 == r2 and r1 == r3 and r1 != r4:
        nu_2 = r4[0]
        alpha_1 = r1[1]
        alpha_2 = r4[1]
    elif r1 == r2 and r1 == r4 and r1 != r3:
        nu_2 = r3[0]
        alpha_1 = r1[1]
        alpha_2 = r3[1]
        if parameter is not None:
            parameter = np.transpose(parameter, (0, 1, 3, 2))
    elif r1 == r3 and r1 == r4 and r1 != r2:
        nu_2 = r2[0]
        alpha_1 = r1[1]
        alpha_2 = r2[1]
        if parameter is not None:
            parameter = np.transpose(parameter, (0, 2, 3, 1))
    elif r2 == r3 and r2 == r4 and r1 != r2:
        nu_2 = _minus(r2[0])
        alpha_1 = r2[1]
        alpha_2 = r1[1]
        if parameter is not None:
            parameter = np.transpose(parameter, (1, 2, 3, 0))
    else:
        raise ValueError("Invalid indices for (3+1+0+0) case.")

    versions_nus = [
        ((0, 0, 0), (0, 0, 0), nu_2),
        ((0, 0, 0), nu_2, (0, 0, 0)),
        (nu_2, (0, 0, 0), (0, 0, 0)),
        (_minus(nu_2), _minus(nu_2), _minus(nu_2)),
    ]

    versions_alphas = [
        (alpha_1, alpha_1, alpha_1, alpha_2),
        (alpha_1, alpha_1, alpha_2, alpha_1),
        (alpha_1, alpha_2, alpha_1, alpha_1),
        (alpha_2, alpha_1, alpha_1, alpha_1),
    ]

    if parameter is None:
        versions_parameter = [None] * 4
    else:
        versions_parameter = [
            parameter.copy(),
            np.transpose(parameter.copy(), (0, 1, 3, 2)),
            np.transpose(parameter.copy(), (0, 3, 1, 2)),
            np.transpose(parameter.copy(), (3, 0, 1, 2)),
        ]

    parameters = list(zip(versions_nus, versions_alphas, versions_parameter))
    parameters.sort(key=lambda x: x[:-1], reverse=True)

    return parameters


def _get_equivalent_4_3(nus, alphas, parameter=None):
    """
    See S.25 of SI of paper-2026
    """
    r1 = ((0, 0, 0), alphas[0])
    r2 = (nus[0], alphas[1])
    r3 = (nus[1], alphas[2])
    r4 = (nus[2], alphas[3])
    if r1 == r2 and r3 == r4 and r2 != r3:
        nu_2 = r3[0]
        alpha_1 = r1[1]
        alpha_2 = r3[1]
    elif r1 == r3 and r2 == r4 and r1 != r2:
        nu_2 = r2[0]
        alpha_1 = r1[1]
        alpha_2 = r2[1]
        if parameter is not None:
            parameter = np.transpose(parameter, (0, 2, 1, 3))
    elif r1 == r4 and r2 == r3 and r1 != r2:
        nu_2 = r2[0]
        alpha_1 = r1[1]
        alpha_2 = r2[1]
        if parameter is not None:
            parameter = np.transpose(parameter, (0, 3, 1, 2))
    else:
        raise ValueError("Invalid indices for (2+2+0+0) case.")

    versions_nus = [
        ((0, 0, 0), nu_2, nu_2),
        (nu_2, (0, 0, 0), nu_2),
        (nu_2, nu_2, (0, 0, 0)),
        (_minus(nu_2), _minus(nu_2), (0, 0, 0)),
        (_minus(nu_2), (0, 0, 0), _minus(nu_2)),
        ((0, 0, 0), _minus(nu_2), _minus(nu_2)),
    ]

    versions_alphas = [
        (alpha_1, alpha_1, alpha_2, alpha_2),
        (alpha_1, alpha_2, alpha_1, alpha_2),
        (alpha_1, alpha_2, alpha_2, alpha_1),
        (alpha_2, alpha_1, alpha_1, alpha_2),
        (alpha_2, alpha_1, alpha_2, alpha_1),
        (alpha_2, alpha_2, alpha_1, alpha_1),
    ]

    if parameter is None:
        versions_parameter = [None] * 6
    else:
        versions_parameter = [
            parameter.copy(),
            np.transpose(parameter.copy(), (0, 2, 1, 3)),
            np.transpose(parameter.copy(), (0, 2, 3, 1)),
            np.transpose(parameter.copy(), (2, 0, 1, 3)),
            np.transpose(parameter.copy(), (2, 0, 3, 1)),
            np.transpose(parameter.copy(), (2, 3, 0, 1)),
        ]

    parameters = list(zip(versions_nus, versions_alphas, versions_parameter))
    parameters.sort(key=lambda x: x[:-1], reverse=True)

    return parameters


def _get_equivalent_4_4(nus, alphas, parameter=None):
    """
    See S.26 of SI of paper-2026
    """
    r1 = ((0, 0, 0), alphas[0])
    r2 = (nus[0], alphas[1])
    r3 = (nus[1], alphas[2])
    r4 = (nus[2], alphas[3])
    if r1 == r2 and r1 != r3 and r1 != r4 and r3 != r4:
        nu_2 = r3[0]
        nu_3 = r4[0]
        alpha_1 = r1[1]
        alpha_2 = r3[1]
        alpha_3 = r4[1]
    elif r1 == r3 and r1 != r2 and r1 != r4 and r2 != r4:
        nu_2 = r2[0]
        nu_3 = r4[0]
        alpha_1 = r1[1]
        alpha_2 = r2[1]
        alpha_3 = r4[1]
        if parameter is not None:
            parameter = np.transpose(parameter, (0, 2, 1, 3))
    elif r1 == r4 and r1 != r2 and r1 != r3 and r2 != r3:
        nu_2 = r2[0]
        nu_3 = r3[0]
        alpha_1 = r1[1]
        alpha_2 = r2[1]
        alpha_3 = r3[1]
        if parameter is not None:
            parameter = np.transpose(parameter, (0, 3, 1, 2))
    elif r2 == r3 and r2 != r1 and r2 != r4 and r1 != r4:
        nu_2 = _minus(r2[0])
        nu_3 = _diff(r4[0], r2[0])
        alpha_1 = r2[1]
        alpha_2 = r1[1]
        alpha_3 = r4[1]
        if parameter is not None:
            parameter = np.transpose(parameter, (1, 2, 0, 3))
    elif r2 == r4 and r2 != r1 and r2 != r3 and r1 != r3:
        nu_2 = _minus(r2[0])
        nu_3 = _diff(r3[0], r2[0])
        alpha_1 = r2[1]
        alpha_2 = r1[1]
        alpha_3 = r3[1]
        if parameter is not None:
            parameter = np.transpose(parameter, (1, 3, 0, 2))
    elif r3 == r4 and r3 != r1 and r3 != r2 and r1 != r2:
        nu_2 = _minus(r3[0])
        nu_3 = _diff(r2[0], r3[0])
        alpha_1 = r3[1]
        alpha_2 = r1[1]
        alpha_3 = r2[1]
        if parameter is not None:
            parameter = np.transpose(parameter, (2, 3, 0, 1))
    else:
        raise ValueError("Invalid indices for (2+1+1+0) case.")

    versions_nus = [
        ((0, 0, 0), nu_2, nu_3),
        ((0, 0, 0), nu_3, nu_2),
        (nu_2, (0, 0, 0), nu_3),
        (nu_3, (0, 0, 0), nu_2),
        (nu_2, nu_3, (0, 0, 0)),
        (nu_3, nu_2, (0, 0, 0)),
        (_minus(nu_2), _minus(nu_2), _diff(nu_3, nu_2)),
        (_minus(nu_3), _minus(nu_3), _diff(nu_2, nu_3)),
        (_minus(nu_2), _diff(nu_3, nu_2), _minus(nu_2)),
        (_minus(nu_3), _diff(nu_2, nu_3), _minus(nu_3)),
        (_diff(nu_3, nu_2), _minus(nu_2), _minus(nu_2)),
        (_diff(nu_2, nu_3), _minus(nu_3), _minus(nu_3)),
    ]

    versions_alphas = [
        (alpha_1, alpha_1, alpha_2, alpha_3),
        (alpha_1, alpha_1, alpha_3, alpha_2),
        (alpha_1, alpha_2, alpha_1, alpha_3),
        (alpha_1, alpha_3, alpha_1, alpha_2),
        (alpha_1, alpha_2, alpha_3, alpha_1),
        (alpha_1, alpha_3, alpha_2, alpha_1),
        (alpha_2, alpha_1, alpha_1, alpha_3),
        (alpha_3, alpha_1, alpha_1, alpha_2),
        (alpha_2, alpha_1, alpha_3, alpha_1),
        (alpha_3, alpha_1, alpha_2, alpha_1),
        (alpha_2, alpha_3, alpha_1, alpha_1),
        (alpha_3, alpha_2, alpha_1, alpha_1),
    ]

    if parameter is None:
        versions_parameter = [None] * 12
    else:
        versions_parameter = [
            parameter.copy(),
            np.transpose(parameter.copy(), (0, 1, 3, 2)),
            np.transpose(parameter.copy(), (0, 2, 1, 3)),
            np.transpose(parameter.copy(), (0, 3, 1, 2)),
            np.transpose(parameter.copy(), (0, 2, 3, 1)),
            np.transpose(parameter.copy(), (0, 3, 2, 1)),
            np.transpose(parameter.copy(), (2, 0, 1, 3)),
            np.transpose(parameter.copy(), (3, 0, 1, 2)),
            np.transpose(parameter.copy(), (2, 0, 3, 1)),
            np.transpose(parameter.copy(), (3, 0, 2, 1)),
            np.transpose(parameter.copy(), (2, 3, 0, 1)),
            np.transpose(parameter.copy(), (3, 2, 0, 1)),
        ]

    parameters = list(zip(versions_nus, versions_alphas, versions_parameter))
    parameters.sort(key=lambda x: x[:-1], reverse=True)

    return parameters


def _get_equivalent_4_5(nus, alphas, parameter=None):
    """
    See S.27 of SI of paper-2026
    """
    nu_2 = nus[0]
    nu_3 = nus[1]
    nu_4 = nus[2]
    alpha_1 = alphas[0]
    alpha_2 = alphas[1]
    alpha_3 = alphas[2]
    alpha_4 = alphas[3]

    r1 = ((0, 0, 0), alpha_1)
    r2 = (nu_2, alpha_2)
    r3 = (nu_3, alpha_3)
    r4 = (nu_4, alpha_4)
    if r1 == r2 or r1 == r3 or r1 == r4 or r2 == r3 or r2 == r4 or r3 == r4:
        raise ValueError("Invalid indices for (1+1+1+1) case.")

    versions_nus = [
        (nu_2, nu_3, nu_4),
        (nu_2, nu_4, nu_3),
        (nu_3, nu_2, nu_4),
        (nu_3, nu_4, nu_2),
        (nu_4, nu_2, nu_3),
        (nu_4, nu_3, nu_2),
        (_minus(nu_2), _diff(nu_3, nu_2), _diff(nu_4, nu_2)),
        (_minus(nu_2), _diff(nu_4, nu_2), _diff(nu_3, nu_2)),
        (_diff(nu_3, nu_2), _minus(nu_2), _diff(nu_4, nu_2)),
        (_diff(nu_3, nu_2), _diff(nu_4, nu_2), _minus(nu_2)),
        (_diff(nu_4, nu_2), _minus(nu_2), _diff(nu_3, nu_2)),
        (_diff(nu_4, nu_2), _diff(nu_3, nu_2), _minus(nu_2)),
        (_minus(nu_3), _diff(nu_2, nu_3), _diff(nu_4, nu_3)),
        (_minus(nu_3), _diff(nu_4, nu_3), _diff(nu_2, nu_3)),
        (_diff(nu_2, nu_3), _minus(nu_3), _diff(nu_4, nu_3)),
        (_diff(nu_2, nu_3), _diff(nu_4, nu_3), _minus(nu_3)),
        (_diff(nu_4, nu_3), _minus(nu_3), _diff(nu_2, nu_3)),
        (_diff(nu_4, nu_3), _diff(nu_2, nu_3), _minus(nu_3)),
        (_minus(nu_4), _diff(nu_2, nu_4), _diff(nu_3, nu_4)),
        (_minus(nu_4), _diff(nu_3, nu_4), _diff(nu_2, nu_4)),
        (_diff(nu_2, nu_4), _minus(nu_4), _diff(nu_3, nu_4)),
        (_diff(nu_2, nu_4), _diff(nu_3, nu_4), _minus(nu_4)),
        (_diff(nu_3, nu_4), _minus(nu_4), _diff(nu_2, nu_4)),
        (_diff(nu_3, nu_4), _diff(nu_2, nu_4), _minus(nu_4)),
    ]

    versions_alphas = [
        (alpha_1, alpha_2, alpha_3, alpha_4),
        (alpha_1, alpha_2, alpha_4, alpha_3),
        (alpha_1, alpha_3, alpha_2, alpha_4),
        (alpha_1, alpha_3, alpha_4, alpha_2),
        (alpha_1, alpha_4, alpha_2, alpha_3),
        (alpha_1, alpha_4, alpha_3, alpha_2),
        (alpha_2, alpha_1, alpha_3, alpha_4),
        (alpha_2, alpha_1, alpha_4, alpha_3),
        (alpha_2, alpha_3, alpha_1, alpha_4),
        (alpha_2, alpha_3, alpha_4, alpha_1),
        (alpha_2, alpha_4, alpha_1, alpha_3),
        (alpha_2, alpha_4, alpha_3, alpha_1),
        (alpha_3, alpha_1, alpha_2, alpha_4),
        (alpha_3, alpha_1, alpha_4, alpha_2),
        (alpha_3, alpha_2, alpha_1, alpha_4),
        (alpha_3, alpha_2, alpha_4, alpha_1),
        (alpha_3, alpha_4, alpha_1, alpha_2),
        (alpha_3, alpha_4, alpha_2, alpha_1),
        (alpha_4, alpha_1, alpha_2, alpha_3),
        (alpha_4, alpha_1, alpha_3, alpha_2),
        (alpha_4, alpha_2, alpha_1, alpha_3),
        (alpha_4, alpha_2, alpha_3, alpha_1),
        (alpha_4, alpha_3, alpha_1, alpha_2),
        (alpha_4, alpha_3, alpha_2, alpha_1),
    ]

    if parameter is None:
        versions_parameter = [None] * 24
    else:
        versions_parameter = [
            parameter.copy(),
            np.transpose(parameter.copy(), (0, 1, 3, 2)),
            np.transpose(parameter.copy(), (0, 2, 1, 3)),
            np.transpose(parameter.copy(), (0, 2, 3, 1)),
            np.transpose(parameter.copy(), (0, 3, 1, 2)),
            np.transpose(parameter.copy(), (0, 3, 2, 1)),
            np.transpose(parameter.copy(), (1, 0, 2, 3)),
            np.transpose(parameter.copy(), (1, 0, 3, 2)),
            np.transpose(parameter.copy(), (1, 2, 0, 3)),
            np.transpose(parameter.copy(), (1, 2, 3, 0)),
            np.transpose(parameter.copy(), (1, 3, 0, 2)),
            np.transpose(parameter.copy(), (1, 3, 2, 0)),
            np.transpose(parameter.copy(), (2, 0, 1, 3)),
            np.transpose(parameter.copy(), (2, 0, 3, 1)),
            np.transpose(parameter.copy(), (2, 1, 0, 3)),
            np.transpose(parameter.copy(), (2, 1, 3, 0)),
            np.transpose(parameter.copy(), (2, 3, 0, 1)),
            np.transpose(parameter.copy(), (2, 3, 1, 0)),
            np.transpose(parameter.copy(), (3, 0, 1, 2)),
            np.transpose(parameter.copy(), (3, 0, 2, 1)),
            np.transpose(parameter.copy(), (3, 1, 0, 2)),
            np.transpose(parameter.copy(), (3, 1, 2, 0)),
            np.transpose(parameter.copy(), (3, 2, 0, 1)),
            np.transpose(parameter.copy(), (3, 2, 1, 0)),
        ]

    parameters = list(zip(versions_nus, versions_alphas, versions_parameter))
    parameters.sort(key=lambda x: x[:-1], reverse=True)

    return parameters


def _get_equivalent(n, p_n, nus, alphas, parameter=None):

    if n == 2 and p_n == 2:
        return _get_equivalent_2_2(nus, alphas, parameter)
    elif n == 3 and p_n == 2:
        return _get_equivalent_3_2(nus, alphas, parameter)
    elif n == 3 and p_n == 3:
        return _get_equivalent_3_3(nus, alphas, parameter)
    elif n == 4 and p_n == 2:
        return _get_equivalent_4_2(nus, alphas, parameter)
    elif n == 4 and p_n == 3:
        return _get_equivalent_4_3(nus, alphas, parameter)
    elif n == 4 and p_n == 4:
        return _get_equivalent_4_4(nus, alphas, parameter)
    elif n == 4 and p_n == 5:
        return _get_equivalent_4_5(nus, alphas, parameter)
    elif p_n == 1 and 1 <= n <= 4:
        return [(nus, alphas, parameter)]
    else:
        raise ValueError("Invalid n and p_n values.")


def get_equivalent_parameters(nus, alphas, parameter=None):
    """
    Computes equivalent parameters as described in supplementary information of
    |paper-2026|_ (eqs. S.21-S.27).

    The returned list of parameters is sorted in descending order by the indices (nus and
    alphas).

    Parameters
    ----------
    nus : list of tuples
        List of ``n-1`` unit cell indices associated with the parameter. Each unit cell
        index is a tuple of three integers.
    alphas : list of tuples
        List of ``n`` atom indices associated with the parameter. Each atom index is an
        integer.
    parameter : (3, ..., 3) |array-like|_, optional
        Value of the parameter. The shape of the array should be (3, ..., 3) with ``n``
        dimensions. If not provided, then the returned parameters will have ``None`` as
        the value.

    Returns
    -------
    parameters : list of tuples
        List of equivalent parameters. Each parameter is a tuple of the form
        ``(nus, alphas, parameter)`` where ``nus`` and ``alphas`` are the unit cell and
        atom indices of the parameter, respectively, and ``parameter`` is the value of
        the parameter (or ``None`` if not provided).

    Notes
    -----
    See :ref:`user-guide_theory-behind_equivalent-parameters` for more details.

    Examples
    --------

    .. doctest::

        >>> import magnopy
        >>> eq_params = magnopy.get_equivalent_parameters(
        ...     nus=[(1, 0, 0)],
        ...     alphas=[(0,), (1,)],
        ...     parameter=[[0, -1, 0], [0.5, 0.3, 0], [0, 0, 0]],
        ... )
        >>> for nus, alphas, parameter in eq_params:
        ...     print(nus, alphas)
        ...     print(parameter)
        ((1, 0, 0),) ((0,), (1,))
        [[ 0.  -1.   0. ]
         [ 0.5  0.3  0. ]
         [ 0.   0.   0. ]]
        ((-1, 0, 0),) ((1,), (0,))
        [[ 0.   0.5  0. ]
         [-1.   0.3  0. ]
         [ 0.   0.   0. ]]

    .. doctest::

        >>> import magnopy
        >>> eq_params = magnopy.get_equivalent_parameters(
        ...     nus=[(1, 0, 0), (0, 1, 0)], alphas=[(0,), (1,), (2,)], parameter=None
        ... )
        >>> for nus, alphas, parameter in eq_params:
        ...     print(nus, alphas)
        ((1, 0, 0), (0, 1, 0)) ((0,), (1,), (2,))
        ((1, -1, 0), (0, -1, 0)) ((2,), (1,), (0,))
        ((0, 1, 0), (1, 0, 0)) ((0,), (2,), (1,))
        ((0, -1, 0), (1, -1, 0)) ((2,), (0,), (1,))
        ((-1, 1, 0), (-1, 0, 0)) ((1,), (2,), (0,))
        ((-1, 0, 0), (-1, 1, 0)) ((1,), (0,), (2,))
    """

    nus_for_specs = [(0, 0, 0)] + list(nus)

    n, p_n = _get_specs(nus=nus_for_specs, alphas=alphas)[:2]

    if parameter is not None:
        parameter = np.array(parameter)

    return _get_equivalent(n=n, p_n=p_n, nus=nus, alphas=alphas, parameter=parameter)


def _get_missing_parameters(parameters, strategy="mean"):
    r"""
    Computes missing parameters of the equivalent sets.

    Parameters
    ----------
    parameters : _InteractionParameters
    strategy : str, default="mean"

    Returns
    -------
    missing_parameters : _InteractionParameters
    """

    strategy = strategy.lower()
    counter = {}
    missing_parameters = _InteractionParameters()

    for (n, p_n, nus, alphas), parameter in parameters._container:
        equivalent_set = _get_equivalent(
            n=n, p_n=p_n, nus=nus, alphas=alphas, parameter=parameter
        )

        for eq_nus, eq_alphas, eq_parameter in equivalent_set:
            eq_specs = (n, p_n, eq_nus, eq_alphas)

            if eq_specs not in parameters:
                if strategy == "zeros":
                    missing_parameters.add(
                        specs=eq_specs,
                        parameter=np.zeros_like(parameter, dtype=float),
                        when_present="skip",
                    )
                elif strategy == "mean":
                    if (eq_nus, eq_alphas) not in counter:
                        counter[(eq_nus, eq_alphas)] = 0
                    missing_parameters.add(
                        specs=eq_specs,
                        parameter=parameter,
                        when_present="weighted average",
                        weights=(counter[(eq_nus, eq_alphas)], 1),
                    )
                    counter[(eq_nus, eq_alphas)] += 1
                else:
                    raise ValueError(
                        f'Expected strategy to be either "zeros" or "mean", got {strategy}.'
                    )
    return missing_parameters


def _set_distribution(parameters, strategy="symmetrize"):
    r"""
    Changes distribution within equivalent sets.

    Parameters
    ----------
    parameters : _InteractionParameters

    Returns
    -------
    new_parameters : _InteractionParameters
    """

    strategy = strategy.lower()
    new_parameters = _InteractionParameters()

    if strategy == "symmetrize":
        for (n, p_n, nus, alphas), parameter in parameters._container:
            equivalent_parameters = _get_equivalent(
                n=n, p_n=p_n, nus=nus, alphas=alphas, parameter=parameter
            )

            degeneracy = len(equivalent_parameters)

            for eq_nus, eq_alphas, eq_parameter in equivalent_parameters:
                new_parameters.add(
                    specs=(n, p_n, eq_nus, eq_alphas),
                    parameter=eq_parameter / degeneracy,
                    when_present="sum",
                )
    elif strategy == "representative":
        for (n, p_n, nus, alphas), parameter in parameters._container:
            equivalent_parameters = _get_equivalent(
                n=n, p_n=p_n, nus=nus, alphas=alphas, parameter=parameter
            )

            for index, (eq_nus, eq_alphas, eq_parameter) in enumerate(
                equivalent_parameters
            ):
                if index == 0:
                    new_parameters.add(
                        specs=(n, p_n, eq_nus, eq_alphas),
                        parameter=eq_parameter,
                        when_present="sum",
                    )
                else:
                    new_parameters.add(
                        specs=(n, p_n, eq_nus, eq_alphas),
                        parameter=np.zeros_like(eq_parameter, dtype=float),
                        when_present="skip",
                    )
    else:
        raise ValueError(
            f'Expected strategy to be either "symmetrize" or "representative" got {strategy}.'
        )

    return new_parameters


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir

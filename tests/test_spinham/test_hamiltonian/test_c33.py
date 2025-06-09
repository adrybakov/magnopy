# MAGNOPY - Python package for magnons.
# Copyright (C) 2023-2025 Magnopy Team
#
# e-mail: anry@uv.es, web: magnopy.com
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


import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as harrays

from magnopy import Convention, SpinHamiltonian
from magnopy._spinham._c33 import _get_primary_p33

MAX_MODULUS = 1e8
ARRAY_3x3x3 = harrays(
    np.float64,
    (3, 3, 3),
    elements=st.floats(min_value=-MAX_MODULUS, max_value=MAX_MODULUS),
)
RANDOM_UC = harrays(int, (4, 3), elements=st.integers(min_value=-1000, max_value=1000))


@given(
    st.integers(),
    st.integers(),
    st.integers(),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.tuples(st.integers(), st.integers(), st.integers()),
    ARRAY_3x3x3,
)
def test_add_33(alpha, beta, gamma, nu, _lambda, parameter):
    atoms = {"names": ["Cr" for _ in range(9)], "spins": [1 for _ in range(9)]}

    spinham = SpinHamiltonian(cell=np.eye(3), atoms=atoms, convention=Convention())

    if (
        0 <= alpha < len(spinham.atoms.names)
        and 0 <= beta < len(spinham.atoms.names)
        and 0 <= gamma < len(spinham.atoms.names)
    ):
        spinham.add_33(alpha, beta, gamma, nu, _lambda, parameter)
    else:
        with pytest.raises(ValueError):
            spinham.add_33(alpha, beta, gamma, nu, _lambda, parameter)


@given(
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.tuples(st.integers(), st.integers(), st.integers()),
    ARRAY_3x3x3,
)
def test_add_33_sorting(
    alpha1,
    beta1,
    gamma1,
    nu1,
    _lambda1,
    alpha2,
    beta2,
    gamma2,
    nu2,
    _lambda2,
    alpha3,
    beta3,
    gamma3,
    nu3,
    _lambda3,
    alpha4,
    beta4,
    gamma4,
    nu4,
    _lambda4,
    parameter,
):
    atoms = {"names": ["Cr" for _ in range(9)], "spins": [1 for _ in range(9)]}

    spinham = SpinHamiltonian(cell=np.eye(3), atoms=atoms, convention=Convention())

    spinham.add_33(alpha1, beta1, gamma1, nu1, _lambda1, parameter)

    if [alpha1, beta1, gamma1, nu1, _lambda1] == [alpha2, beta2, gamma2, nu2, _lambda2]:
        with pytest.raises(ValueError):
            spinham.add_33(alpha2, beta2, gamma2, nu2, _lambda2, parameter)
    else:
        spinham.add_33(alpha2, beta2, gamma2, nu2, _lambda2, parameter)

    spinham.add_33(alpha3, beta3, gamma3, nu3, _lambda3, parameter, replace=True)
    spinham.add_33(alpha4, beta4, gamma4, nu4, _lambda4, parameter, replace=True)

    for i in range(len(spinham._33) - 1):
        assert spinham._33[i][:-1] <= spinham._33[i + 1][:-1]


@given(
    st.integers(min_value=0, max_value=2),
    st.integers(min_value=0, max_value=2),
    st.integers(min_value=0, max_value=2),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.tuples(st.integers(), st.integers(), st.integers()),
    RANDOM_UC,
    RANDOM_UC,
)
def test_remove_33(r_alpha, r_beta, r_gamma, r_nu, r_lambda, nus, lambdas):
    atoms = {"names": ["Cr" for _ in range(4)], "spins": [1 for _ in range(4)]}

    spinham = SpinHamiltonian(cell=np.eye(3), atoms=atoms, convention=Convention())

    for alpha in range(len(spinham.atoms.names)):
        for beta in range(alpha, len(spinham.atoms.names)):
            for gamma in range(beta, len(spinham.atoms.names)):
                for nu in nus:
                    for _lambda in lambdas:
                        nu = (int(nu[0]), int(nu[1]), int(nu[2]))
                        _lambda = (int(_lambda[0]), int(_lambda[1]), int(_lambda[2]))
                        spinham.add_33(
                            alpha,
                            beta,
                            gamma,
                            nu,
                            _lambda,
                            np.ones((3, 3, 3)),
                            replace=True,
                        )

    bond = [r_alpha, r_beta, r_gamma, r_nu, r_lambda]
    if (
        0 <= r_alpha < len(spinham.atoms.names)
        and 0 <= r_beta < len(spinham.atoms.names)
        and 0 <= r_gamma < len(spinham.atoms.names)
    ):
        original_bonds = [tmp[:-1] for tmp in spinham._33]
        original_length = len(spinham._33)

        spinham.remove_33(*bond)

        primary_bond = list(_get_primary_p33(*bond))
        if primary_bond in original_bonds:
            updated_bonds = [tmp[:-1] for tmp in spinham._33]

            assert len(spinham._33) == original_length - 1
            assert bond not in updated_bonds
            assert primary_bond not in updated_bonds
        else:
            assert len(spinham._33) == original_length

    else:
        with pytest.raises(ValueError):
            spinham.remove_33(*bond)


@given(ARRAY_3x3x3, st.floats(min_value=0.1, max_value=1e4))
def test_mul(parameter, number):
    atoms = {"names": ["Cr" for _ in range(9)], "spins": [1 for _ in range(9)]}

    spinham = SpinHamiltonian(
        cell=np.eye(3),
        atoms=atoms,
        convention=Convention(multiple_counting=True, spin_normalized=False),
    )

    spinham.add_33(
        alpha=0, beta=1, gamma=4, nu=(0, 3, -4), _lambda=(1, 3, 6), parameter=parameter
    )
    spinham.add_33(
        alpha=4,
        beta=2,
        gamma=3,
        nu=(1, 0, 0),
        _lambda=(0, 0, 5),
        parameter=parameter * 1.33,
    )
    spinham.add_33(
        alpha=7,
        beta=5,
        gamma=2,
        nu=(0, 0, 0),
        _lambda=(-1, 2, 3),
        parameter=parameter / 3,
    )

    m_spinham = spinham * number

    assert spinham.M == m_spinham.M

    assert len(spinham.p33) == len(m_spinham.p33)

    params = list(spinham.p33)
    m_params = list(m_spinham.p33)
    for i in range(len(params)):
        assert params[i][0] == m_params[i][0]
        assert params[i][1] == m_params[i][1]
        assert params[i][2] == m_params[i][2]
        assert params[i][3] == m_params[i][3]
        assert params[i][4] == m_params[i][4]

        assert np.allclose(number * params[i][5], m_params[i][5])


@given(ARRAY_3x3x3, st.floats(min_value=0.1, max_value=1e4))
def test_rmul(parameter, number):
    atoms = {"names": ["Cr" for _ in range(9)], "spins": [1 for _ in range(9)]}

    spinham = SpinHamiltonian(
        cell=np.eye(3),
        atoms=atoms,
        convention=Convention(multiple_counting=True, spin_normalized=False),
    )

    spinham.add_33(
        alpha=0, beta=1, gamma=4, nu=(0, 3, -4), _lambda=(1, 3, 6), parameter=parameter
    )
    spinham.add_33(
        alpha=4,
        beta=2,
        gamma=3,
        nu=(1, 0, 0),
        _lambda=(0, 0, 5),
        parameter=parameter * 1.33,
    )
    spinham.add_33(
        alpha=7,
        beta=5,
        gamma=2,
        nu=(0, 0, 0),
        _lambda=(-1, 2, 3),
        parameter=parameter / 3,
    )

    m_spinham = number * spinham

    assert spinham.M == m_spinham.M

    assert len(spinham.p33) == len(m_spinham.p33)

    params = list(spinham.p33)
    m_params = list(m_spinham.p33)
    for i in range(len(params)):
        assert params[i][0] == m_params[i][0]
        assert params[i][1] == m_params[i][1]
        assert params[i][2] == m_params[i][2]
        assert params[i][3] == m_params[i][3]
        assert params[i][4] == m_params[i][4]

        assert np.allclose(number * params[i][5], m_params[i][5])


@given(ARRAY_3x3x3, ARRAY_3x3x3)
def test_add(parameter1, parameter2):
    atoms = dict(
        names=["Cr" for _ in range(9)],
        spins=[1 for _ in range(9)],
        positions=[[0.1 * i, 0, 0] for i in range(9)],
        g_factors=[2 for _ in range(9)],
    )

    spinham1 = SpinHamiltonian(
        cell=np.eye(3), atoms=atoms, convention=Convention(multiple_counting=True)
    )
    spinham2 = SpinHamiltonian(
        cell=np.eye(3), atoms=atoms, convention=Convention(multiple_counting=True)
    )

    spinham1.add_33(
        alpha=0, beta=1, gamma=4, nu=(0, 3, -4), _lambda=(1, 3, 6), parameter=parameter1
    )
    spinham1.add_33(
        alpha=4,
        beta=2,
        gamma=3,
        nu=(1, 0, 0),
        _lambda=(0, 0, 5),
        parameter=parameter1 * 1.33,
    )
    spinham1.add_33(
        alpha=7,
        beta=5,
        gamma=2,
        nu=(0, 0, 0),
        _lambda=(1, 2, 3),
        parameter=parameter1 / 3,
    )

    spinham2.add_33(
        alpha=0, beta=1, gamma=4, nu=(0, 3, -4), _lambda=(1, 3, 6), parameter=parameter2
    )
    spinham2.add_33(
        alpha=4,
        beta=2,
        gamma=3,
        nu=(1, 0, 0),
        _lambda=(0, 0, 5),
        parameter=parameter2 * 1.33,
    )
    spinham2.add_33(
        alpha=8,
        beta=5,
        gamma=2,
        nu=(0, 0, 0),
        _lambda=(1, 2, 3),
        parameter=parameter2 / 3,
    )

    m_spinham = spinham1 + spinham2

    assert m_spinham.M == 8

    assert len(m_spinham.p33) == 24

    for i in range(2):
        assert np.allclose(
            m_spinham._33[i][-1], spinham1._33[i][-1] + spinham2._33[i][-1]
        )

    assert np.allclose(m_spinham._33[2][-1], spinham1._33[2][-1])
    assert np.allclose(m_spinham._33[3][-1], spinham2._33[2][-1])

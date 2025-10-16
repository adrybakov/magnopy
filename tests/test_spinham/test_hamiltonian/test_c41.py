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
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as harrays

from magnopy import Convention, SpinHamiltonian, make_supercell

MAX_MODULUS = 1e8
ARRAY = harrays(
    np.float64,
    (3, 3, 3, 3),
    elements=st.floats(min_value=-MAX_MODULUS, max_value=MAX_MODULUS),
)


def get_spinham(for_supercell=False) -> SpinHamiltonian:
    if for_supercell:
        atoms = dict(
            names=["Cr1", "Cr2"],
            spins=[1, 2],
            positions=[[0, 0, 0], [0.5, 0.5, 0.5]],
            g_factors=[2, 2],
        )
    else:
        atoms = dict(
            names=["Cr" for _ in range(9)],
            spins=[1 for _ in range(9)],
            positions=[[0.1 * i, 0, 0] for i in range(9)],
            g_factors=[2 for _ in range(9)],
        )

    return SpinHamiltonian(
        cell=np.eye(3),
        atoms=atoms,
        convention=Convention(
            spin_normalized=False,
            multiple_counting=True,
            c1=1,
            c21=1,
            c22=1,
            c31=1,
            c32=1,
            c33=1,
            c41=1,
            c421=1,
            c422=1,
            c43=1,
            c44=1,
        ),
    )


@given(st.integers(), ARRAY)
def test_add_41(alpha, parameter):
    spinham = get_spinham()

    if 0 <= alpha < len(spinham.atoms.names):
        spinham.add_41(alpha, parameter)
    else:
        with pytest.raises(ValueError):
            spinham.add_41(alpha, parameter)


@pytest.mark.parametrize(
    "when_present, parameter",
    [("skip", 1.0), ("replace", 2.0), ("add", 3.0), ("mean", 1.5)],
)
def test_add_41_when_present(when_present, parameter):
    spinham = get_spinham()

    spinham.add_41(0, np.ones((3, 3, 3, 3)))

    with pytest.raises(ValueError):
        spinham.add_41(0, np.ones((3, 3, 3, 3)))

    spinham.add_41(0, 2.0 * np.ones((3, 3, 3, 3)), when_present=when_present)
    assert np.allclose(spinham._41[0][1], parameter * np.ones((3, 3, 3, 3)))


@given(
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    ARRAY,
)
def test_add_41_sorting(alpha1, alpha2, alpha3, alpha4, parameter):
    spinham = get_spinham()

    spinham.add_41(alpha1, parameter)

    if alpha2 == alpha1:
        with pytest.raises(ValueError):
            spinham.add_41(alpha2, parameter)
    else:
        spinham.add_41(alpha2, parameter)

    spinham.add_41(alpha3, parameter, when_present="replace")
    spinham.add_41(alpha4, parameter, when_present="replace")

    for i in range(len(spinham._41) - 1):
        assert spinham._41[i][:-1] <= spinham._41[i + 1][:-1]


@given(st.integers())
def test_remove_41(r_alpha):
    spinham = get_spinham()

    for alpha in range(len(spinham.atoms.names)):
        spinham.add_41(alpha, np.ones((3, 3, 3, 3)))

    bond = [r_alpha]
    if 0 <= r_alpha < len(spinham.atoms.names):
        original_bonds = [tmp[:-1] for tmp in spinham._41]
        original_length = len(spinham._41)

        spinham.remove_41(*bond)

        if bond in original_bonds:
            updated_bonds = [tmp[:-1] for tmp in spinham._41]

            assert len(spinham._41) == original_length - 1
            assert bond not in updated_bonds
        else:
            assert len(spinham._41) == original_length
    else:
        with pytest.raises(ValueError):
            spinham.remove_41(*bond)


@given(ARRAY, st.floats(min_value=0.1, max_value=1e4))
def test_mul(parameter, number):
    spinham = get_spinham()

    spinham.add_41(alpha=0, parameter=parameter)
    spinham.add_41(alpha=4, parameter=parameter * 1.32)
    spinham.add_41(alpha=7, parameter=parameter / 3)

    m_spinham = spinham * number

    assert spinham.M == m_spinham.M

    assert len(spinham.p41) == len(m_spinham.p41)

    params = list(spinham.p41)
    m_params = list(m_spinham.p41)
    for i in range(len(params)):
        assert params[i][0] == m_params[i][0]

        assert np.allclose(number * params[i][1], m_params[i][1])


@given(ARRAY, st.floats(min_value=0.1, max_value=1e4))
def test_rmul(parameter, number):
    spinham = get_spinham()

    spinham.add_41(alpha=0, parameter=parameter)
    spinham.add_41(alpha=4, parameter=parameter * 1.32)
    spinham.add_41(alpha=7, parameter=parameter / 3)

    m_spinham = number * spinham

    assert spinham.M == m_spinham.M

    assert len(spinham.p41) == len(m_spinham.p41)

    params = list(spinham.p41)
    m_params = list(m_spinham.p41)
    for i in range(len(params)):
        assert params[i][0] == m_params[i][0]

        assert np.allclose(number * params[i][1], m_params[i][1])


@given(ARRAY, ARRAY)
def test_add(parameter1, parameter2):
    spinham1 = get_spinham()
    spinham2 = get_spinham()

    spinham1.add_41(alpha=0, parameter=parameter1)
    spinham1.add_41(alpha=4, parameter=parameter1 * 1.32)
    spinham1.add_41(alpha=7, parameter=parameter1 / 3)

    spinham2.add_41(alpha=0, parameter=parameter2)
    spinham2.add_41(alpha=4, parameter=parameter2 * 1.32)
    spinham2.add_41(alpha=8, parameter=parameter2 / 3)

    m_spinham = spinham1 + spinham2

    assert m_spinham.M == 4

    assert len(m_spinham.p41) == 4

    for i in range(2):
        assert np.allclose(m_spinham._41[i][1], spinham1._41[i][1] + spinham2._41[i][1])

    assert np.allclose(m_spinham._41[2][1], spinham1._41[2][1])
    assert np.allclose(m_spinham._41[3][1], spinham2._41[2][1])


@given(
    ARRAY,
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1, max_value=5),
)
def test_make_supercell(parameter1, i, j, k):
    spinham = get_spinham(for_supercell=True)

    spinham.add_41(alpha=0, parameter=parameter1)
    spinham.add_41(alpha=1, parameter=parameter1 * 1.42)

    new_spinham = make_supercell(spinham=spinham, supercell=(i, j, k))

    assert len(new_spinham.p41) == i * j * k * 2

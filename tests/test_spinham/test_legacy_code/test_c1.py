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
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as harrays

from magnopy import Convention, SpinHamiltonian, make_supercell

MAX_MODULUS = 1e8
ARRAY = harrays(
    np.float64,
    (3,),
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
            c42=1,
            c43=1,
            c44=1,
            c45=1,
        ),
    )


@given(st.integers(), ARRAY)
def test_add_1(alpha, parameter):
    spinham = get_spinham()

    if 0 <= alpha < len(spinham.atoms.names):
        spinham.add_1(alpha, parameter)
    else:
        with pytest.raises(ValueError):
            spinham.add_1(alpha, parameter)


@pytest.mark.parametrize(
    "when_present, parameter",
    [("skip", 1.0), ("replace", 2.0), ("sum", 3.0), ("mean", 1.5)],
)
def test_add_1_when_present(when_present, parameter):
    spinham = get_spinham()

    spinham.add_1(0, np.ones(3))

    with pytest.raises(ValueError):
        spinham.add_1(0, np.ones(3))

    spinham.add_1(0, 2.0 * np.ones(3), when_present=when_present)
    assert np.allclose(spinham.p1[0][-1], parameter * np.ones(3))


@given(
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    ARRAY,
)
def test_add_1_sorting(alpha1, alpha2, alpha3, alpha4, parameter):
    spinham = get_spinham()

    spinham.add_1(alpha1, parameter)

    if alpha2 == alpha1:
        with pytest.raises(ValueError):
            spinham.add_1(alpha2, parameter)
    else:
        spinham.add_1(alpha2, parameter)

    spinham.add_1(alpha3, parameter, when_present="replace")
    spinham.add_1(alpha4, parameter, when_present="replace")

    parameters = list(spinham.p1)
    for i in range(len(parameters) - 1):
        assert parameters[i][:2] <= parameters[i + 1][:2]


@given(st.integers())
def test_remove_1(r_alpha):
    spinham = get_spinham()
    r_specs = ((), (r_alpha,))

    for alpha in range(len(spinham.atoms.names)):
        spinham.add_1(alpha, np.ones(3))

    if 0 <= r_alpha < len(spinham.atoms.names):
        specs_before = [_[:-1] for _ in spinham.p1]
        spinham.remove_1(alpha=r_alpha)
        updated_specs = [_[:-1] for _ in spinham.p1]

        if r_specs in specs_before:
            assert len(updated_specs) == len(specs_before) - 1
            assert r_specs not in updated_specs
        else:
            assert len(updated_specs) == len(specs_before)
    else:
        with pytest.raises(ValueError):
            spinham.remove_1(alpha=r_alpha)


@given(ARRAY, st.floats(min_value=0.1, max_value=1e4))
def test_mul(parameter, number):
    spinham = get_spinham()

    spinham.add_1(alpha=0, parameter=parameter)
    spinham.add_1(alpha=4, parameter=parameter * 1.32)
    spinham.add_1(alpha=7, parameter=parameter / 3)

    m_spinham = spinham * number

    assert spinham.M == m_spinham.M

    assert len(spinham.p1) == len(m_spinham.p1)

    for i in range(len(spinham.p1)):
        assert spinham.p1[i][0] == m_spinham.p1[i][0]
        assert spinham.p1[i][1] == m_spinham.p1[i][1]

        assert np.allclose(number * spinham.p1[i][2], m_spinham.p1[i][2])


@given(ARRAY, st.floats(min_value=0.1, max_value=1e4))
def test_rmul(parameter, number):
    spinham = get_spinham()

    spinham.add_1(alpha=0, parameter=parameter)
    spinham.add_1(alpha=4, parameter=parameter * 1.32)
    spinham.add_1(alpha=7, parameter=parameter / 3)

    m_spinham = number * spinham

    assert spinham.M == m_spinham.M

    assert len(spinham.p1) == len(m_spinham.p1)

    for i in range(len(spinham.p1)):
        assert spinham.p1[i][0] == m_spinham.p1[i][0]
        assert spinham.p1[i][1] == m_spinham.p1[i][1]

        assert np.allclose(number * spinham.p1[i][2], m_spinham.p1[i][2])


@given(ARRAY, ARRAY)
def test_add(parameter1, parameter2):
    spinham1 = get_spinham()
    spinham2 = get_spinham()

    spinham1.add_1(alpha=0, parameter=parameter1)
    spinham1.add_1(alpha=4, parameter=parameter1 * 1.32)
    spinham1.add_1(alpha=7, parameter=parameter1 / 3)

    spinham2.add_1(alpha=0, parameter=parameter2)
    spinham2.add_1(alpha=4, parameter=parameter2 * 1.32)
    spinham2.add_1(alpha=8, parameter=parameter2 / 3)

    m_spinham = spinham1 + spinham2

    assert m_spinham.M == 4

    assert len(m_spinham.p1) == 4

    for i in range(2):
        assert np.allclose(m_spinham.p1[i][2], spinham1.p1[i][2] + spinham2.p1[i][2])

    assert np.allclose(m_spinham.p1[2][2], spinham1.p1[2][2])
    assert np.allclose(m_spinham.p1[3][2], spinham2.p1[2][2])


@given(
    ARRAY,
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1, max_value=5),
)
def test_make_supercell(parameter1, i, j, k):
    spinham = get_spinham(for_supercell=True)

    spinham.add_1(alpha=0, parameter=parameter1)
    spinham.add_1(alpha=1, parameter=parameter1 * 1.42)

    assert len(spinham.p1) == 2

    new_spinham = make_supercell(spinham=spinham, supercell=(i, j, k))

    assert len(new_spinham.p1) == i * j * k * 2

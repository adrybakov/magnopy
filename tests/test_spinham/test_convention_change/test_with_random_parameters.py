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
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as harrays

from magnopy import Convention, Energy, SpinHamiltonian

MAX_MODULUS = 1e4
ARRAY_3 = harrays(
    np.float64,
    (3),
    elements=st.floats(min_value=-MAX_MODULUS, max_value=MAX_MODULUS),
)
ARRAY_3x3 = harrays(
    np.float64,
    (3, 3),
    elements=st.floats(min_value=-MAX_MODULUS, max_value=MAX_MODULUS),
)
ARRAY_3x3x3 = harrays(
    np.float64,
    (3, 3, 3),
    elements=st.floats(min_value=-MAX_MODULUS, max_value=MAX_MODULUS),
)
ARRAY_3x3x3x3 = harrays(
    np.float64,
    (3, 3, 3, 3),
    elements=st.floats(min_value=-MAX_MODULUS, max_value=MAX_MODULUS),
)


def _get_spinham(p1, p2, p3, p4):
    basic_convention = Convention(
        spin_normalized=False,
        multiple_counting=False,
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

    cell = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    atoms = dict(
        names=["Fe1", "Fe2"],
        spins=[5 / 2, 3 / 2],
        positions=[[0, 0, 0], [0.5, 0.5, 0.5]],
    )

    spin_directions = [[0, 0, 1], [0, 0, 1]]

    spinham = SpinHamiltonian(cell=cell, atoms=atoms, convention=basic_convention)

    # (1)
    spinham.add(nus=(), alphas=(0,), parameter=p1)
    spinham.add(nus=(), alphas=(1,), parameter=p1)

    # (2+0)
    spinham.add(nus=((0, 0, 0),), alphas=(0, 0), parameter=p2)
    spinham.add(nus=((0, 0, 0),), alphas=(1, 1), parameter=p2)

    # (1+1)
    spinham.add(nus=((1, 0, 0),), alphas=(0, 0), parameter=p2)
    spinham.add(nus=((0, 1, 0),), alphas=(0, 0), parameter=p2)
    spinham.add(nus=((0, 0, 1),), alphas=(0, 0), parameter=p2)

    spinham.add(nus=((0, 0, 0),), alphas=(0, 1), parameter=p2)
    spinham.add(nus=((-1, 0, 0),), alphas=(0, 1), parameter=p2)
    spinham.add(nus=((-1, -1, 0),), alphas=(0, 1), parameter=p2)
    spinham.add(nus=((0, -1, 0),), alphas=(0, 1), parameter=p2)

    # (3+0+0)
    spinham.add(nus=((0, 0, 0), (0, 0, 0)), alphas=(0, 0, 0), parameter=p3)
    spinham.add(nus=((0, 0, 0), (0, 0, 0)), alphas=(1, 1, 1), parameter=p3)

    # (2+1+0)
    spinham.add(nus=((0, 0, 0), (1, 0, 0)), alphas=(0, 0, 0), parameter=p3)
    spinham.add(nus=((0, 0, 0), (0, 1, 0)), alphas=(0, 0, 0), parameter=p3)
    spinham.add(nus=((0, 0, 0), (0, 0, 1)), alphas=(0, 0, 0), parameter=p3)

    spinham.add(nus=((0, 0, 0), (0, 0, 0)), alphas=(0, 0, 1), parameter=p3)
    spinham.add(nus=((0, 0, 0), (-1, 0, 0)), alphas=(0, 0, 1), parameter=p3)
    spinham.add(nus=((0, 0, 0), (-1, -1, 0)), alphas=(0, 0, 1), parameter=p3)
    spinham.add(nus=((0, 0, 0), (0, -1, 0)), alphas=(0, 0, 1), parameter=p3)

    # (1+1+1)
    spinham.add(nus=((1, 0, 0), (0, 1, 0)), alphas=(0, 0, 0), parameter=p3)
    spinham.add(nus=((1, 0, 0), (0, 1, 0)), alphas=(1, 1, 1), parameter=p3)
    spinham.add(nus=((0, 0, 0), (-1, 0, 0)), alphas=(0, 1, 1), parameter=p3)

    # (4+0+0+0)
    spinham.add(
        alphas=(0, 0, 0, 0), nus=((0, 0, 0), (0, 0, 0), (0, 0, 0)), parameter=p4
    )
    spinham.add(
        alphas=(1, 1, 1, 1), nus=((0, 0, 0), (0, 0, 0), (0, 0, 0)), parameter=p4
    )

    # (3+1+0+0)
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (1, 0, 0)), alphas=(0, 0, 0, 0), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (0, 1, 0)), alphas=(0, 0, 0, 0), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (0, 0, 1)), alphas=(0, 0, 0, 0), parameter=p4
    )

    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (0, 0, 0)), alphas=(0, 0, 0, 1), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (-1, 0, 0)), alphas=(0, 0, 0, 1), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (-1, -1, 0)), alphas=(0, 0, 0, 1), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (0, -1, 0)), alphas=(0, 0, 0, 1), parameter=p4
    )

    # (2+2+0+0)
    spinham.add(
        nus=((0, 0, 0), (1, 0, 0), (1, 0, 0)), alphas=(0, 0, 0, 0), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (0, 1, 0), (0, 1, 0)), alphas=(0, 0, 0, 0), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 1), (0, 0, 1)), alphas=(0, 0, 0, 0), parameter=p4
    )

    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (0, 0, 0)), alphas=(0, 0, 1, 1), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (-1, 0, 0), (-1, 0, 0)), alphas=(0, 0, 1, 1), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (-1, -1, 0), (-1, -1, 0)), alphas=(0, 0, 1, 1), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (0, -1, 0), (0, -1, 0)), alphas=(0, 0, 1, 1), parameter=p4
    )

    # (2+1+1+0)
    spinham.add(
        nus=((0, 0, 0), (1, 0, 0), (0, 1, 0)), alphas=(0, 0, 0, 0), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (1, 0, 0), (0, 1, 0)), alphas=(1, 1, 1, 1), parameter=p4
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (-1, 0, 0)), alphas=(0, 0, 1, 1), parameter=p4
    )

    # (1+1+1+1)
    spinham.add(
        alphas=(0, 0, 0, 0), nus=((1, 0, 0), (0, 1, 0), (0, 0, 1)), parameter=p4
    )
    spinham.add(
        alphas=(1, 1, 1, 1), nus=((1, 0, 0), (0, 1, 0), (0, 0, 1)), parameter=p4
    )

    spinham.add(
        alphas=(0, 0, 1, 1), nus=((1, 0, 0), (0, 0, 0), (1, 0, 0)), parameter=p4
    )

    return spinham, basic_convention, spin_directions


@pytest.mark.parametrize("spin_normalized", (True, False))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_spin_normalized(spin_normalized, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)

    modified_convention = convention.get_modified(spin_normalized=spin_normalized)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("multiple_counting", (True, False))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_multiple_counting(multiple_counting, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)

    modified_convention = convention.get_modified(multiple_counting=multiple_counting)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c1", (-1, -0.5, 0.5, 1))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_c1(c1, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)
    assert len(spinham.p1) > 0

    modified_convention = convention.get_modified(c1=c1)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c21", (-1, -0.5, 0.5, 1))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_c21(c21, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)
    assert len(spinham.p21) > 0

    modified_convention = convention.get_modified(c21=c21)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c22", (-1, -0.5, 0.5, 1))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_c22(c22, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)
    assert len(spinham.p22) > 0

    modified_convention = convention.get_modified(c22=c22)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c31", (-1, -0.5, 0.5, 1))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_c31(c31, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)
    assert len(spinham.p31) > 0

    modified_convention = convention.get_modified(c31=c31)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c32", (-1, -0.5, 0.5, 1))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_c32(c32, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)
    assert len(spinham.p32) > 0

    modified_convention = convention.get_modified(c32=c32)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c33", (-1, -0.5, 0.5, 1))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_c33(c33, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)
    assert len(spinham.p33) > 0

    modified_convention = convention.get_modified(c33=c33)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c41", (-1, -0.5, 0.5, 1))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_c41(c41, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)
    assert len(spinham.p41) > 0

    modified_convention = convention.get_modified(c41=c41)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c42", (-1, -0.5, 0.5, 1))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_c42(c42, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)
    assert len(spinham.p42) > 0

    modified_convention = convention.get_modified(c42=c42)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c43", (-1, -0.5, 0.5, 1))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_c43(c43, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)
    assert len(spinham.p43) > 0

    modified_convention = convention.get_modified(c43=c43)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c44", (-1, -0.5, 0.5, 1))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_c44(c44, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)
    assert len(spinham.p44) > 0

    modified_convention = convention.get_modified(c44=c44)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c45", (-1, -0.5, 0.5, 1))
@given(p1=ARRAY_3, p2=ARRAY_3x3, p3=ARRAY_3x3x3, p4=ARRAY_3x3x3x3)
@settings(deadline=1000)
def test_c45(c45, p1, p2, p3, p4):
    spinham, convention, spin_directions = _get_spinham(p1=p1, p2=p2, p3=p3, p4=p4)
    assert len(spinham.p45) > 0

    modified_convention = convention.get_modified(c45=c45)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8

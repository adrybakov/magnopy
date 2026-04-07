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


import pytest

from magnopy import Convention, Energy, SpinHamiltonian


def _get_spinham():
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
    spinham.add(nus=(), alphas=(0,), parameter=[1, 1, 1])
    spinham.add(nus=(), alphas=(1,), parameter=[1, 1, 1])

    parameter = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    # (2+0)
    spinham.add(nus=((0, 0, 0),), alphas=(0, 0), parameter=parameter)
    spinham.add(nus=((0, 0, 0),), alphas=(1, 1), parameter=parameter)

    # (1+1)
    spinham.add(nus=((1, 0, 0),), alphas=(0, 0), parameter=parameter)
    spinham.add(nus=((0, 1, 0),), alphas=(0, 0), parameter=parameter)
    spinham.add(nus=((0, 0, 1),), alphas=(0, 0), parameter=parameter)

    spinham.add(nus=((0, 0, 0),), alphas=(0, 1), parameter=parameter)
    spinham.add(nus=((-1, 0, 0),), alphas=(0, 1), parameter=parameter)
    spinham.add(nus=((-1, -1, 0),), alphas=(0, 1), parameter=parameter)
    spinham.add(nus=((0, -1, 0),), alphas=(0, 1), parameter=parameter)

    parameter = [
        [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 1]],
    ]
    # (3+0+0)
    spinham.add(nus=((0, 0, 0), (0, 0, 0)), alphas=(0, 0, 0), parameter=parameter)
    spinham.add(nus=((0, 0, 0), (0, 0, 0)), alphas=(1, 1, 1), parameter=parameter)

    # (2+1+0)
    spinham.add(nus=((0, 0, 0), (1, 0, 0)), alphas=(0, 0, 0), parameter=parameter)
    spinham.add(nus=((0, 0, 0), (0, 1, 0)), alphas=(0, 0, 0), parameter=parameter)
    spinham.add(nus=((0, 0, 0), (0, 0, 1)), alphas=(0, 0, 0), parameter=parameter)

    spinham.add(nus=((0, 0, 0), (0, 0, 0)), alphas=(0, 0, 1), parameter=parameter)
    spinham.add(nus=((0, 0, 0), (-1, 0, 0)), alphas=(0, 0, 1), parameter=parameter)
    spinham.add(nus=((0, 0, 0), (-1, -1, 0)), alphas=(0, 0, 1), parameter=parameter)
    spinham.add(nus=((0, 0, 0), (0, -1, 0)), alphas=(0, 0, 1), parameter=parameter)

    # (1+1+1)
    spinham.add(nus=((1, 0, 0), (0, 1, 0)), alphas=(0, 0, 0), parameter=parameter)
    spinham.add(nus=((1, 0, 0), (0, 1, 0)), alphas=(1, 1, 1), parameter=parameter)
    spinham.add(nus=((0, 0, 0), (-1, 0, 0)), alphas=(0, 1, 1), parameter=parameter)

    parameter = [
        [
            [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ],
        [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ],
        [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 1]],
        ],
    ]
    # (4+0+0+0)
    spinham.add(
        alphas=(0, 0, 0, 0), nus=((0, 0, 0), (0, 0, 0), (0, 0, 0)), parameter=parameter
    )
    spinham.add(
        alphas=(1, 1, 1, 1), nus=((0, 0, 0), (0, 0, 0), (0, 0, 0)), parameter=parameter
    )

    # (3+1+0+0)
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (1, 0, 0)), alphas=(0, 0, 0, 0), parameter=parameter
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (0, 1, 0)), alphas=(0, 0, 0, 0), parameter=parameter
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (0, 0, 1)), alphas=(0, 0, 0, 0), parameter=parameter
    )

    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (0, 0, 0)), alphas=(0, 0, 0, 1), parameter=parameter
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (-1, 0, 0)), alphas=(0, 0, 0, 1), parameter=parameter
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (-1, -1, 0)),
        alphas=(0, 0, 0, 1),
        parameter=parameter,
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (0, -1, 0)), alphas=(0, 0, 0, 1), parameter=parameter
    )

    # (2+2+0+0)
    spinham.add(
        nus=((0, 0, 0), (1, 0, 0), (1, 0, 0)), alphas=(0, 0, 0, 0), parameter=parameter
    )
    spinham.add(
        nus=((0, 0, 0), (0, 1, 0), (0, 1, 0)), alphas=(0, 0, 0, 0), parameter=parameter
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 1), (0, 0, 1)), alphas=(0, 0, 0, 0), parameter=parameter
    )

    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (0, 0, 0)), alphas=(0, 0, 1, 1), parameter=parameter
    )
    spinham.add(
        nus=((0, 0, 0), (-1, 0, 0), (-1, 0, 0)),
        alphas=(0, 0, 1, 1),
        parameter=parameter,
    )
    spinham.add(
        nus=((0, 0, 0), (-1, -1, 0), (-1, -1, 0)),
        alphas=(0, 0, 1, 1),
        parameter=parameter,
    )
    spinham.add(
        nus=((0, 0, 0), (0, -1, 0), (0, -1, 0)),
        alphas=(0, 0, 1, 1),
        parameter=parameter,
    )

    # (2+1+1+0)
    spinham.add(
        nus=((0, 0, 0), (1, 0, 0), (0, 1, 0)), alphas=(0, 0, 0, 0), parameter=parameter
    )
    spinham.add(
        nus=((0, 0, 0), (1, 0, 0), (0, 1, 0)), alphas=(1, 1, 1, 1), parameter=parameter
    )
    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (-1, 0, 0)), alphas=(0, 0, 1, 1), parameter=parameter
    )

    # (1+1+1+1)
    spinham.add(
        alphas=(0, 0, 0, 0), nus=((1, 0, 0), (0, 1, 0), (0, 0, 1)), parameter=parameter
    )
    spinham.add(
        alphas=(1, 1, 1, 1), nus=((1, 0, 0), (0, 1, 0), (0, 0, 1)), parameter=parameter
    )

    spinham.add(
        alphas=(0, 0, 1, 1), nus=((1, 0, 0), (0, 0, 0), (1, 0, 0)), parameter=parameter
    )

    return spinham, basic_convention, spin_directions


@pytest.mark.parametrize("spin_normalized", (True, False))
def test_spin_normalized(spin_normalized):
    spinham, convention, spin_directions = _get_spinham()

    modified_convention = convention.get_modified(spin_normalized=spin_normalized)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("multiple_counting", (True, False))
def test_multiple_counting(multiple_counting):
    spinham, convention, spin_directions = _get_spinham()

    modified_convention = convention.get_modified(multiple_counting=multiple_counting)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c1", (-1, -0.5, 0.5, 1))
def test_c1(c1):
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p1) > 0

    modified_convention = convention.get_modified(c1=c1)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c21", (-1, -0.5, 0.5, 1))
def test_c21(c21):
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p21) > 0

    modified_convention = convention.get_modified(c21=c21)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c22", (-1, -0.5, 0.5, 1))
def test_c22(c22):
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p22) > 0

    modified_convention = convention.get_modified(c22=c22)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c31", (-1, -0.5, 0.5, 1))
def test_c31(c31):
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p31) > 0

    modified_convention = convention.get_modified(c31=c31)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c32", (-1, -0.5, 0.5, 1))
def test_c32(c32):
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p32) > 0

    modified_convention = convention.get_modified(c32=c32)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c33", (-1, -0.5, 0.5, 1))
def test_c33(c33):
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p33) > 0

    modified_convention = convention.get_modified(c33=c33)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c41", (-1, -0.5, 0.5, 1))
def test_c41(c41):
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p41) > 0

    modified_convention = convention.get_modified(c41=c41)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c42", (-1, -0.5, 0.5, 1))
def test_c42(c42):
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p42) > 0

    modified_convention = convention.get_modified(c42=c42)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c43", (-1, -0.5, 0.5, 1))
def test_c43(c43):
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p43) > 0

    modified_convention = convention.get_modified(c43=c43)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c44", (-1, -0.5, 0.5, 1))
def test_c44(c44):
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p44) > 0

    modified_convention = convention.get_modified(c44=c44)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


@pytest.mark.parametrize("c45", (-1, -0.5, 0.5, 1))
def test_c45(c45):
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p45) > 0

    modified_convention = convention.get_modified(c45=c45)

    target_energy = Energy(spinham)

    spinham.convention = modified_convention
    energy = Energy(spinham)

    assert abs(energy.E_0(spin_directions) - target_energy.E_0(spin_directions)) < 1e-8


def test_altogether():
    spinham, convention, spin_directions = _get_spinham()
    assert len(spinham.p1) > 0
    assert len(spinham.p21) > 0
    assert len(spinham.p22) > 0
    assert len(spinham.p31) > 0
    assert len(spinham.p32) > 0
    assert len(spinham.p33) > 0
    assert len(spinham.p41) > 0
    assert len(spinham.p42) > 0
    assert len(spinham.p43) > 0
    assert len(spinham.p44) > 0
    assert len(spinham.p45) > 0

    target_energy = Energy(spinham)

    for spin_normalized in [True, False]:
        for multiple_counting in [True, False]:
            for c1 in [-1, 0.5]:
                for c21 in [-1, 0.5]:
                    for c22 in [-1, 0.5]:
                        for c31 in [-1, 0.5]:
                            for c32 in [-1, 0.5]:
                                for c33 in [-1, 0.5]:
                                    for c41 in [-1, 0.5]:
                                        for c42 in [-1, 0.5]:
                                            for c43 in [-1, 0.5]:
                                                for c44 in [-1, 0.5]:
                                                    for c45 in [-1, 0.5]:
                                                        spinham.convention = Convention(
                                                            spin_normalized=spin_normalized,
                                                            multiple_counting=multiple_counting,
                                                            c1=c1,
                                                            c21=c21,
                                                            c22=c22,
                                                            c31=c31,
                                                            c32=c32,
                                                            c33=c33,
                                                            c41=c41,
                                                            c42=c42,
                                                            c43=c43,
                                                            c44=c44,
                                                            c45=c45,
                                                        )

                                                        energy = Energy(spinham)

                                                        assert (
                                                            abs(
                                                                energy.E_0(
                                                                    spin_directions
                                                                )
                                                                - target_energy.E_0(
                                                                    spin_directions
                                                                )
                                                            )
                                                            < 1e-8
                                                        )

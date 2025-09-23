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


import pytest

from magnopy import Convention, Energy, SpinHamiltonian
from magnopy._constants._units import _PARAMETER_UNITS


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
        c421=1,
        c422=1,
        c43=1,
        c44=1,
    )

    cell = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    atoms = dict(
        names=["Fe1", "Fe2"],
        spins=[5 / 2, 3 / 2],
        positions=[[0, 0, 0], [0.5, 0.5, 0.5]],
    )

    spin_directions = [[0, 0, 1], [0, 0, 1]]

    spinham = SpinHamiltonian(cell=cell, atoms=atoms, convention=basic_convention)

    spinham.add_1(alpha=0, parameter=[1, 1, 1])
    spinham.add_1(alpha=1, parameter=[1, 1, 1])

    parameter = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    spinham.add_21(alpha=0, parameter=parameter)
    spinham.add_21(alpha=1, parameter=parameter)

    spinham.add_22(alpha=0, beta=0, nu=(1, 0, 0), parameter=parameter)
    spinham.add_22(alpha=0, beta=0, nu=(0, 1, 0), parameter=parameter)
    spinham.add_22(alpha=0, beta=0, nu=(0, 0, 1), parameter=parameter)

    spinham.add_22(alpha=0, beta=1, nu=(0, 0, 0), parameter=parameter)
    spinham.add_22(alpha=0, beta=1, nu=(-1, 0, 0), parameter=parameter)
    spinham.add_22(alpha=0, beta=1, nu=(-1, -1, 0), parameter=parameter)
    spinham.add_22(alpha=0, beta=1, nu=(0, -1, 0), parameter=parameter)

    parameter = [
        [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 1]],
    ]
    spinham.add_31(alpha=0, parameter=parameter)
    spinham.add_31(alpha=1, parameter=parameter)

    spinham.add_32(alpha=0, beta=0, nu=(1, 0, 0), parameter=parameter)
    spinham.add_32(alpha=0, beta=0, nu=(0, 1, 0), parameter=parameter)
    spinham.add_32(alpha=0, beta=0, nu=(0, 0, 1), parameter=parameter)

    spinham.add_32(alpha=0, beta=1, nu=(0, 0, 0), parameter=parameter)
    spinham.add_32(alpha=0, beta=1, nu=(-1, 0, 0), parameter=parameter)
    spinham.add_32(alpha=0, beta=1, nu=(-1, -1, 0), parameter=parameter)
    spinham.add_32(alpha=0, beta=1, nu=(0, -1, 0), parameter=parameter)

    spinham.add_33(
        alpha=0, beta=0, gamma=0, nu=(1, 0, 0), _lambda=(0, 1, 0), parameter=parameter
    )
    spinham.add_33(
        alpha=1, beta=1, gamma=1, nu=(1, 0, 0), _lambda=(0, 1, 0), parameter=parameter
    )
    spinham.add_33(
        alpha=0, beta=1, gamma=1, nu=(0, 0, 0), _lambda=(-1, 0, 0), parameter=parameter
    )

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
    spinham.add_41(alpha=0, parameter=parameter)
    spinham.add_41(alpha=1, parameter=parameter)

    spinham.add_421(alpha=0, beta=0, nu=(1, 0, 0), parameter=parameter)
    spinham.add_421(alpha=0, beta=0, nu=(0, 1, 0), parameter=parameter)
    spinham.add_421(alpha=0, beta=0, nu=(0, 0, 1), parameter=parameter)

    spinham.add_421(alpha=0, beta=1, nu=(0, 0, 0), parameter=parameter)
    spinham.add_421(alpha=0, beta=1, nu=(-1, 0, 0), parameter=parameter)
    spinham.add_421(alpha=0, beta=1, nu=(-1, -1, 0), parameter=parameter)
    spinham.add_421(alpha=0, beta=1, nu=(0, -1, 0), parameter=parameter)

    spinham.add_422(alpha=0, beta=0, nu=(1, 0, 0), parameter=parameter)
    spinham.add_422(alpha=0, beta=0, nu=(0, 1, 0), parameter=parameter)
    spinham.add_422(alpha=0, beta=0, nu=(0, 0, 1), parameter=parameter)

    spinham.add_422(alpha=0, beta=1, nu=(0, 0, 0), parameter=parameter)
    spinham.add_422(alpha=0, beta=1, nu=(-1, 0, 0), parameter=parameter)
    spinham.add_422(alpha=0, beta=1, nu=(-1, -1, 0), parameter=parameter)
    spinham.add_422(alpha=0, beta=1, nu=(0, -1, 0), parameter=parameter)

    spinham.add_43(
        alpha=0, beta=0, gamma=0, nu=(1, 0, 0), _lambda=(0, 1, 0), parameter=parameter
    )
    spinham.add_43(
        alpha=1, beta=1, gamma=1, nu=(1, 0, 0), _lambda=(0, 1, 0), parameter=parameter
    )
    spinham.add_43(
        alpha=0, beta=1, gamma=1, nu=(0, 0, 0), _lambda=(-1, 0, 0), parameter=parameter
    )

    spinham.add_44(
        alpha=0,
        beta=0,
        gamma=0,
        epsilon=0,
        nu=(1, 0, 0),
        _lambda=(0, 1, 0),
        rho=(0, 0, 1),
        parameter=parameter,
    )
    spinham.add_44(
        alpha=1,
        beta=1,
        gamma=1,
        epsilon=1,
        nu=(1, 0, 0),
        _lambda=(0, 1, 0),
        rho=(0, 0, 1),
        parameter=parameter,
    )

    spinham.add_44(
        alpha=0,
        beta=0,
        gamma=1,
        epsilon=1,
        nu=(1, 0, 0),
        _lambda=(0, 0, 0),
        rho=(1, 0, 0),
        parameter=parameter,
    )

    return spinham, spin_directions


@pytest.mark.parametrize("units", list(_PARAMETER_UNITS))
def test_c44(units):
    spinham, spin_directions = _get_spinham()

    target_energy = Energy(spinham).E_0(spin_directions)

    spinham.units = units

    energy = Energy(spinham).E_0(spin_directions)

    assert abs(energy - target_energy) <= 1e-8 * abs(target_energy)

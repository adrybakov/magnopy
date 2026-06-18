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
import pytest
from magnopy import SpinHamiltonian, Convention, Energy


@pytest.mark.parametrize(
    "on_site,sd",
    [[[-0.5, 0, 0], [1, 0, 0]], [[0, -0.5, 0], [0, 1, 0]], [[0, 0, -0.5], [0, 0, 1]]],
)
def test_fm(on_site, sd):
    convention = Convention(
        multiple_counting=True, spin_normalized=False, c1=1, c21=1, c22=1
    )
    cell = np.eye(3)
    atoms = dict(
        names=["Fe"],
        spins=[2.5],
        g_factors=[2],
        positions=[[0, 0, 0]],
        spglib_types=[1],
    )

    spinham = SpinHamiltonian(cell=cell, atoms=atoms, convention=convention)

    spinham.add(
        nus=[(1, 0, 0)], alphas=[0, 0], parameter=-np.eye(3), populate_equivalent=True
    )
    spinham.add(
        nus=[(0, 1, 0)], alphas=[0, 0], parameter=-np.eye(3), populate_equivalent=True
    )
    spinham.add(
        nus=[(0, 0, 1)], alphas=[0, 0], parameter=-np.eye(3), populate_equivalent=True
    )

    spinham.add(nus=[(0, 0, 0)], alphas=[0, 0], parameter=np.diag(on_site))

    energy = Energy(spinham=spinham)

    sd_opt = energy.optimize(quiet=True)

    assert np.allclose(sd_opt, sd, atol=1e-4) or np.allclose(
        sd_opt, -np.array(sd), atol=1e-4
    )


@pytest.mark.parametrize(
    "on_site,sd",
    [[[-0.5, 0, 0], [1, 0, 0]], [[0, -0.5, 0], [0, 1, 0]], [[0, 0, -0.5], [0, 0, 1]]],
)
def test_afm(on_site, sd):
    convention = Convention(
        multiple_counting=True, spin_normalized=False, c1=1, c21=1, c22=1
    )
    cell = np.eye(3)
    atoms = dict(
        names=["Fe1", "Fe2"],
        spins=[2.5, 2.5],
        g_factors=[2, 2],
        positions=[[0, 0, 0], [0.5, 0.5, 0.5]],
        spglib_types=[1, 1],
    )

    spinham = SpinHamiltonian(cell=cell, atoms=atoms, convention=convention)

    spinham.add(
        nus=[(0, 0, 0)], alphas=[0, 1], parameter=np.eye(3), populate_equivalent=True
    )
    spinham.add(
        nus=[(-1, 0, 0)], alphas=[0, 1], parameter=np.eye(3), populate_equivalent=True
    )
    spinham.add(
        nus=[(0, -1, 0)], alphas=[0, 1], parameter=np.eye(3), populate_equivalent=True
    )
    spinham.add(
        nus=[(-1, -1, 0)], alphas=[0, 1], parameter=np.eye(3), populate_equivalent=True
    )

    spinham.add(
        nus=[(0, 0, -1)], alphas=[0, 1], parameter=np.eye(3), populate_equivalent=True
    )
    spinham.add(
        nus=[(-1, 0, -1)], alphas=[0, 1], parameter=np.eye(3), populate_equivalent=True
    )
    spinham.add(
        nus=[(0, -1, -1)], alphas=[0, 1], parameter=np.eye(3), populate_equivalent=True
    )
    spinham.add(
        nus=[(-1, -1, -1)], alphas=[0, 1], parameter=np.eye(3), populate_equivalent=True
    )

    spinham.add(nus=[(0, 0, 0)], alphas=[0, 0], parameter=np.diag(on_site))

    energy = Energy(spinham=spinham)

    sd_opt = energy.optimize(quiet=True)

    assert (
        np.allclose(sd_opt[0], sd, atol=1e-4)
        and np.allclose(sd_opt[1], -np.array(sd), atol=1e-4)
    ) or (
        np.allclose(sd_opt[0], -np.array(sd), atol=1e-4)
        and np.allclose(sd_opt[1], sd, atol=1e-4)
    )

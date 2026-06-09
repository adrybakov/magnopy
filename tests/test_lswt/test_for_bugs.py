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
from math import sqrt
import numpy as np
from magnopy import SpinHamiltonian, Convention, LSWT


def test_issue_114():
    cell = [
        [6, 0, 0],
        [-3, 3 * sqrt(3), 0],
        [0, 0, 10],
    ]
    atoms = dict(
        names=[f"Mn{i}" for i in [1, 2, 3]],
        spins=[1] * 3,
        positions=np.array(
            [
                [1 / 2, 1 / 2, 0],
                [1 / 2, 0, 0],
                [0, 1 / 2, 0],
            ]
        ),
        g_factors=[2.0, 2.0, 2.0],
        spglib_types=[1, 1, 1],
    )

    convention = Convention.get_predefined("SpinW")
    spinham = SpinHamiltonian(cell=cell, atoms=atoms, convention=convention)

    for nu, alpha1, alpha2 in [
        [(-1, 0, 0), 2, 0],
        [(-1, 0, 0), 2, 1],
        [(0, -1, 0), 1, 0],
        [(0, -1, 0), 1, 2],
        [(0, 0, 0), 0, 1],
        [(0, 0, 0), 0, 2],
        [(0, 0, 0), 1, 0],
        [(0, 0, 0), 2, 0],
        [(0, 1, 0), 0, 1],
        [(0, 1, 0), 2, 1],
        [(1, 0, 0), 0, 2],
        [(1, 0, 0), 1, 2],
    ]:
        spinham.add(nus=[nu], alphas=[alpha1, alpha2], parameter=1.0 * np.eye(3))
    for nu, alpha_1, alpha_2 in [
        [(-1, -1, 0), 1, 0],
        [(-1, -1, 0), 2, 0],
        [(-1, 0, 0), 0, 1],
        [(-1, 1, 0), 2, 1],
        [(0, -1, 0), 0, 2],
        [(0, 0, 0), 1, 2],
        [(0, 0, 0), 2, 1],
        [(0, 1, 0), 2, 0],
        [(1, -1, 0), 1, 2],
        [(1, 0, 0), 1, 0],
        [(1, 1, 0), 0, 1],
        [(1, 1, 0), 0, 2],
    ]:
        spinham.add(nus=[nu], alphas=[alpha_1, alpha_2], parameter=0.11 * np.eye(3))

    for alpha in [0, 1, 2]:
        spinham.add(
            nus=[[0, 0, 0]], alphas=[alpha, alpha], parameter=np.diag([-0.5, -0.5, 0])
        )

    sds = np.array(
        [
            [0.866, -0.5, 0.0],
            [0.0, 1.0, 0.0],
            [-0.866, -0.5, 0.0],
        ]
    )

    lswt = LSWT(spinham=spinham, spin_directions=sds)

    omegas = lswt.omega(k=[0, 0, 0])

    assert np.all(np.isfinite(omegas))

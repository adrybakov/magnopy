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
import numpy as np
from magnopy import SpinHamiltonian, Convention, is_eigenstate, ConventionError


@pytest.mark.parametrize(
    "convention",
    [
        Convention(
            multiple_counting=False,
            spin_normalized=False,
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
        Convention(
            multiple_counting=False,
            spin_normalized=False,
            c1=1,
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
        Convention(
            multiple_counting=False,
            spin_normalized=False,
            c1=1,
            c21=1,
            c31=1,
            c32=1,
            c33=1,
            c41=1,
            c42=1,
            c43=1,
            c44=1,
            c45=1,
        ),
        Convention(
            multiple_counting=False,
            spin_normalized=False,
            c1=1,
            c21=1,
            c22=1,
            c32=1,
            c33=1,
            c41=1,
            c42=1,
            c43=1,
            c44=1,
            c45=1,
        ),
        Convention(
            multiple_counting=False,
            spin_normalized=False,
            c1=1,
            c21=1,
            c22=1,
            c31=1,
            c33=1,
            c41=1,
            c42=1,
            c43=1,
            c44=1,
            c45=1,
        ),
        Convention(
            multiple_counting=False,
            spin_normalized=False,
            c1=1,
            c21=1,
            c22=1,
            c31=1,
            c32=1,
            c41=1,
            c42=1,
            c43=1,
            c44=1,
            c45=1,
        ),
        Convention(
            multiple_counting=False,
            spin_normalized=False,
            c1=1,
            c21=1,
            c22=1,
            c31=1,
            c32=1,
            c33=1,
            c42=1,
            c43=1,
            c44=1,
            c45=1,
        ),
        Convention(
            multiple_counting=False,
            spin_normalized=False,
            c1=1,
            c21=1,
            c22=1,
            c31=1,
            c32=1,
            c33=1,
            c41=1,
            c43=1,
            c44=1,
            c45=1,
        ),
        Convention(
            multiple_counting=False,
            spin_normalized=False,
            c1=1,
            c21=1,
            c22=1,
            c31=1,
            c32=1,
            c33=1,
            c41=1,
            c42=1,
            c44=1,
            c45=1,
        ),
        Convention(
            multiple_counting=False,
            spin_normalized=False,
            c1=1,
            c21=1,
            c22=1,
            c31=1,
            c32=1,
            c33=1,
            c41=1,
            c42=1,
            c43=1,
            c45=1,
        ),
        Convention(
            multiple_counting=False,
            spin_normalized=False,
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
        ),
    ],
)
def test_issue_130(convention):
    cell = np.eye(1)
    atoms = dict(
        names=["Fe"],
        spins=[1],
        positions=np.array([[0, 0, 0]]),
        g_factors=[2.0],
        spglib_types=[1],
    )

    spinham = SpinHamiltonian(cell=cell, atoms=atoms, convention=convention)

    # C1
    spinham.add(nus=[], alphas=[0], parameter=np.array([0, 0, 1]))
    # C21
    spinham.add(nus=[(0, 0, 0)], alphas=[0, 0], parameter=np.eye(3))
    # C22
    spinham.add(nus=[(1, 0, 0)], alphas=[0, 0], parameter=np.eye(3))
    # C31
    spinham.add(
        nus=[(0, 0, 0), (0, 0, 0)], alphas=[0, 0, 0], parameter=np.ones((3, 3, 3))
    )
    # C32
    spinham.add(
        nus=[(1, 0, 0), (0, 0, 0)], alphas=[0, 0, 0], parameter=np.ones((3, 3, 3))
    )
    # C32
    spinham.add(
        nus=[(1, 0, 0), (0, 1, 0)], alphas=[0, 0, 0], parameter=np.ones((3, 3, 3))
    )
    # C41
    spinham.add(
        nus=[(0, 0, 0), (0, 0, 0), (0, 0, 0)],
        alphas=[0, 0, 0, 0],
        parameter=np.ones((3, 3, 3, 3)),
    )
    # C42
    spinham.add(
        nus=[(0, 0, 0), (0, 0, 0), (1, 0, 0)],
        alphas=[0, 0, 0, 0],
        parameter=np.ones((3, 3, 3, 3)),
    )
    # C43
    spinham.add(
        nus=[(0, 0, 0), (1, 0, 0), (1, 0, 0)],
        alphas=[0, 0, 0, 0],
        parameter=np.ones((3, 3, 3, 3)),
    )
    # C44
    spinham.add(
        nus=[(0, 0, 0), (1, 0, 0), (0, 1, 0)],
        alphas=[0, 0, 0, 0],
        parameter=np.ones((3, 3, 3, 3)),
    )
    # C45
    spinham.add(
        nus=[(1, 0, 0), (0, 1, 0), (0, 0, 1)],
        alphas=[0, 0, 0, 0],
        parameter=np.ones((3, 3, 3, 3)),
    )

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

    with pytest.raises(ConventionError):
        is_eigenstate(spinham=spinham, spin_directions=np.array([[0, 0, 1]]))

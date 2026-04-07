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
from hypothesis import given
from hypothesis import strategies as st
from copy import deepcopy

from magnopy._parameters._interaction_parameters import (
    _get_specs,
    _InteractionParameters,
)

ROLL = [
    ((), (1,)),
    (((0, 0, 0),), (1, 2)),
    (((0, 0, 0), (0, 0, 0)), (1, 2, 3)),
    (((0, 0, 0), (0, 0, 0), (0, 0, 0)), (1, 2, 3, 4)),
]


@pytest.mark.parametrize(
    "n, p_n, alphas, nus",
    [
        (1, 1, (0,), ((0, 0, 1),)),
        (2, 1, (0, 0), ((0, 1, 0), (0, 1, 0))),
        (2, 2, (0, 0), ((0, 0, 0), (0, 1, 0))),
        (2, 2, (0, 1), ((0, 0, 0), (0, 0, 0))),
        (3, 1, (0, 0, 0), ((0, 1, 0), (0, 1, 0), (0, 1, 0))),
        (3, 2, (0, 1, 0), ((0, 1, 0), (0, 1, 0), (0, 1, 0))),
        (3, 2, (0, 0, 0), ((0, 1, 0), (0, 2, 0), (0, 1, 0))),
        (3, 3, (0, 1, 2), ((0, 1, 0), (0, 1, 0), (0, 1, 0))),
        (3, 3, (0, 0, 1), ((0, 1, 1), (0, 1, 0), (0, 1, 0))),
        (4, 1, (0, 0, 0, 0), ((0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0))),
        (4, 2, (1, 0, 0, 0), ((0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0))),
        (4, 2, (0, 0, 0, 0), ((0, 1, 0), (0, 1, 1), (0, 1, 0), (0, 1, 0))),
        (4, 3, (1, 0, 1, 0), ((0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0))),
        (4, 3, (0, 0, 0, 0), ((1, 1, 0), (0, 1, 0), (1, 1, 0), (0, 1, 0))),
        (4, 4, (0, 1, 2, 0), ((0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0))),
        (4, 4, (0, 0, 0, 0), ((0, 2, 0), (1, 1, 0), (0, 1, 0), (0, 1, 0))),
        (4, 5, (2, 1, 0, 3), ((0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0))),
        (4, 5, (0, 1, 0, 1), ((0, 1, 0), (0, 1, 0), (1, 1, 0), (1, 1, 0))),
    ],
)
def test_get_specs(n, p_n, alphas, nus):
    specs = _get_specs(nus=nus, alphas=alphas)

    assert specs[0] == n
    assert specs[1] == p_n
    assert len(specs[2]) == len(nus) - 1
    assert specs[3] == alphas

    for i in range(len(nus) - 1):
        assert specs[2][i][0] == nus[i + 1][0] - nus[0][0]
        assert specs[2][i][1] == nus[i + 1][1] - nus[0][1]
        assert specs[2][i][2] == nus[i + 1][2] - nus[0][2]


def test_interaction_parameters_add():
    parameters = _InteractionParameters()
    parameters.add(specs=(2, 2, ((-1, 0, 2),), (0, 1)), parameter=np.zeros((3, 3)))

    assert len(parameters._container) == 1
    assert parameters._container[0][0] == (2, 2, ((-1, 0, 2),), (0, 1))
    assert np.allclose(parameters._container[0][1], np.zeros((3, 3)))


def test_interaction_parameters_remove():
    parameters = _InteractionParameters()
    parameters.add(specs=(2, 2, ((-1, 0, 2),), (0, 1)), parameter=np.zeros((3, 3)))

    parameters.remove(specs=(2, 2, ((0, 0, 2),), (1, 0)))
    assert len(parameters._container) == 1

    parameters.remove(specs=(2, 2, ((-1, 0, 2),), (0, 1)))
    assert len(parameters._container) == 0


def test_interaction_parameters_order():
    parameters = _InteractionParameters()
    parameters.add(specs=(1, 1, (), (0,)), parameter=np.zeros((3,)))
    parameters.add(specs=(2, 2, ((0, 0, 2),), (0, 1)), parameter=np.zeros((3, 3)))
    parameters.add(specs=(2, 2, ((-1, 0, 2),), (0, 0)), parameter=np.zeros((3, 3)))

    assert len(parameters._container) == 3
    assert parameters._container[0][0] == (1, 1, (), (0,))
    assert parameters._container[1][0] == (2, 2, ((-1, 0, 2),), (0, 0))
    assert parameters._container[2][0] == (2, 2, ((0, 0, 2),), (0, 1))


PARAMETERS_SINGLES = _InteractionParameters()


@pytest.mark.parametrize(
    "wtd,n, p_n, slices",
    [
        (
            "add",
            None,
            None,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 0],
                (2, 2): [0, 0],
                (3, 1): [0, 0],
                (3, 2): [0, 0],
                (3, 3): [0, 0],
                (4, 1): [0, 0],
                (4, 2): [0, 0],
                (4, 3): [0, 0],
                (4, 4): [0, 0],
                (4, 5): [0, 0],
            },
        ),
        (
            "add",
            3,
            2,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 0],
                (2, 2): [0, 0],
                (3, 1): [0, 0],
                (3, 2): [0, 1],
                (3, 3): [1, 0],
                (4, 1): [1, 0],
                (4, 2): [1, 0],
                (4, 3): [1, 0],
                (4, 4): [1, 0],
                (4, 5): [1, 0],
            },
        ),
        (
            "add",
            2,
            2,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 0],
                (2, 2): [0, 1],
                (3, 1): [1, 0],
                (3, 2): [1, 1],
                (3, 3): [2, 0],
                (4, 1): [2, 0],
                (4, 2): [2, 0],
                (4, 3): [2, 0],
                (4, 4): [2, 0],
                (4, 5): [2, 0],
            },
        ),
        (
            "add",
            4,
            4,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 0],
                (2, 2): [0, 1],
                (3, 1): [1, 0],
                (3, 2): [1, 1],
                (3, 3): [2, 0],
                (4, 1): [2, 0],
                (4, 2): [2, 0],
                (4, 3): [2, 0],
                (4, 4): [2, 1],
                (4, 5): [3, 0],
            },
        ),
        (
            "add",
            1,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 0],
                (2, 2): [1, 1],
                (3, 1): [2, 0],
                (3, 2): [2, 1],
                (3, 3): [3, 0],
                (4, 1): [3, 0],
                (4, 2): [3, 0],
                (4, 3): [3, 0],
                (4, 4): [3, 1],
                (4, 5): [4, 0],
            },
        ),
        (
            "add",
            4,
            2,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 0],
                (2, 2): [1, 1],
                (3, 1): [2, 0],
                (3, 2): [2, 1],
                (3, 3): [3, 0],
                (4, 1): [3, 0],
                (4, 2): [3, 1],
                (4, 3): [4, 0],
                (4, 4): [4, 1],
                (4, 5): [5, 0],
            },
        ),
        (
            "add",
            4,
            2,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 0],
                (2, 2): [1, 1],
                (3, 1): [2, 0],
                (3, 2): [2, 1],
                (3, 3): [3, 0],
                (4, 1): [3, 0],
                (4, 2): [3, 1],
                (4, 3): [4, 0],
                (4, 4): [4, 1],
                (4, 5): [5, 0],
            },
        ),
        (
            "remove",
            2,
            2,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 0],
                (2, 2): [1, 0],
                (3, 1): [1, 0],
                (3, 2): [1, 1],
                (3, 3): [2, 0],
                (4, 1): [2, 0],
                (4, 2): [2, 1],
                (4, 3): [3, 0],
                (4, 4): [3, 1],
                (4, 5): [4, 0],
            },
        ),
        (
            "add",
            2,
            2,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 0],
                (2, 2): [1, 1],
                (3, 1): [2, 0],
                (3, 2): [2, 1],
                (3, 3): [3, 0],
                (4, 1): [3, 0],
                (4, 2): [3, 1],
                (4, 3): [4, 0],
                (4, 4): [4, 1],
                (4, 5): [5, 0],
            },
        ),
        (
            "add",
            2,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 0],
                (3, 2): [3, 1],
                (3, 3): [4, 0],
                (4, 1): [4, 0],
                (4, 2): [4, 1],
                (4, 3): [5, 0],
                (4, 4): [5, 1],
                (4, 5): [6, 0],
            },
        ),
        (
            "add",
            4,
            5,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 0],
                (3, 2): [3, 1],
                (3, 3): [4, 0],
                (4, 1): [4, 0],
                (4, 2): [4, 1],
                (4, 3): [5, 0],
                (4, 4): [5, 1],
                (4, 5): [6, 1],
            },
        ),
        (
            "add",
            4,
            3,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 0],
                (3, 2): [3, 1],
                (3, 3): [4, 0],
                (4, 1): [4, 0],
                (4, 2): [4, 1],
                (4, 3): [5, 1],
                (4, 4): [6, 1],
                (4, 5): [7, 1],
            },
        ),
        (
            "add",
            3,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 1],
                (3, 2): [4, 1],
                (3, 3): [5, 0],
                (4, 1): [5, 0],
                (4, 2): [5, 1],
                (4, 3): [6, 1],
                (4, 4): [7, 1],
                (4, 5): [8, 1],
            },
        ),
        (
            "add",
            3,
            3,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 1],
                (3, 2): [4, 1],
                (3, 3): [5, 1],
                (4, 1): [6, 0],
                (4, 2): [6, 1],
                (4, 3): [7, 1],
                (4, 4): [8, 1],
                (4, 5): [9, 1],
            },
        ),
        (
            "add",
            4,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 1],
                (3, 2): [4, 1],
                (3, 3): [5, 1],
                (4, 1): [6, 1],
                (4, 2): [7, 1],
                (4, 3): [8, 1],
                (4, 4): [9, 1],
                (4, 5): [10, 1],
            },
        ),
        (
            "remove",
            4,
            5,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 1],
                (3, 2): [4, 1],
                (3, 3): [5, 1],
                (4, 1): [6, 1],
                (4, 2): [7, 1],
                (4, 3): [8, 1],
                (4, 4): [9, 1],
                (4, 5): [10, 0],
            },
        ),
        (
            "remove",
            3,
            3,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 1],
                (3, 2): [4, 1],
                (3, 3): [5, 0],
                (4, 1): [5, 1],
                (4, 2): [6, 1],
                (4, 3): [7, 1],
                (4, 4): [8, 1],
                (4, 5): [9, 0],
            },
        ),
        (
            "remove",
            4,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 1],
                (3, 2): [4, 1],
                (3, 3): [5, 0],
                (4, 1): [5, 0],
                (4, 2): [5, 1],
                (4, 3): [6, 1],
                (4, 4): [7, 1],
                (4, 5): [8, 0],
            },
        ),
        (
            "remove",
            3,
            2,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 1],
                (3, 2): [4, 0],
                (3, 3): [4, 0],
                (4, 1): [4, 0],
                (4, 2): [4, 1],
                (4, 3): [5, 1],
                (4, 4): [6, 1],
                (4, 5): [7, 0],
            },
        ),
        (
            "remove",
            4,
            3,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 1],
                (3, 2): [4, 0],
                (3, 3): [4, 0],
                (4, 1): [4, 0],
                (4, 2): [4, 1],
                (4, 3): [5, 0],
                (4, 4): [5, 1],
                (4, 5): [6, 0],
            },
        ),
        (
            "remove",
            4,
            2,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 1],
                (2, 2): [2, 1],
                (3, 1): [3, 1],
                (3, 2): [4, 0],
                (3, 3): [4, 0],
                (4, 1): [4, 0],
                (4, 2): [4, 0],
                (4, 3): [4, 0],
                (4, 4): [4, 1],
                (4, 5): [5, 0],
            },
        ),
        (
            "remove",
            1,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 1],
                (2, 2): [1, 1],
                (3, 1): [2, 1],
                (3, 2): [3, 0],
                (3, 3): [3, 0],
                (4, 1): [3, 0],
                (4, 2): [3, 0],
                (4, 3): [3, 0],
                (4, 4): [3, 1],
                (4, 5): [4, 0],
            },
        ),
        (
            "remove",
            4,
            4,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 1],
                (2, 2): [1, 1],
                (3, 1): [2, 1],
                (3, 2): [3, 0],
                (3, 3): [3, 0],
                (4, 1): [3, 0],
                (4, 2): [3, 0],
                (4, 3): [3, 0],
                (4, 4): [3, 0],
                (4, 5): [3, 0],
            },
        ),
        (
            "remove",
            2,
            2,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 1],
                (2, 2): [1, 0],
                (3, 1): [1, 1],
                (3, 2): [2, 0],
                (3, 3): [2, 0],
                (4, 1): [2, 0],
                (4, 2): [2, 0],
                (4, 3): [2, 0],
                (4, 4): [2, 0],
                (4, 5): [2, 0],
            },
        ),
        (
            "remove",
            3,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 1],
                (2, 2): [1, 0],
                (3, 1): [1, 0],
                (3, 2): [1, 0],
                (3, 3): [1, 0],
                (4, 1): [1, 0],
                (4, 2): [1, 0],
                (4, 3): [1, 0],
                (4, 4): [1, 0],
                (4, 5): [1, 0],
            },
        ),
        (
            "remove",
            2,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 0],
                (2, 2): [0, 0],
                (3, 1): [0, 0],
                (3, 2): [0, 0],
                (3, 3): [0, 0],
                (4, 1): [0, 0],
                (4, 2): [0, 0],
                (4, 3): [0, 0],
                (4, 4): [0, 0],
                (4, 5): [0, 0],
            },
        ),
        (
            "remove",
            2,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 0],
                (2, 2): [0, 0],
                (3, 1): [0, 0],
                (3, 2): [0, 0],
                (3, 3): [0, 0],
                (4, 1): [0, 0],
                (4, 2): [0, 0],
                (4, 3): [0, 0],
                (4, 4): [0, 0],
                (4, 5): [0, 0],
            },
        ),
    ],
)
def test_interaction_parameters_slices_singles(wtd, n, p_n, slices):
    if n is not None and p_n is not None:
        if wtd == "add":
            PARAMETERS_SINGLES.add(
                specs=(n, p_n, *ROLL[n - 1]),
                parameter=np.zeros((3,) * n),
                when_present="skip",
            )
        elif wtd == "remove":
            PARAMETERS_SINGLES.remove(specs=(n, p_n, *ROLL[n - 1]))

    for key in slices:
        assert PARAMETERS_SINGLES._slices[key] == slices[key]


PARAMETERS_MULTIPLES = _InteractionParameters()
MULTIPLES_MULTIPLES = {
    (1, 1): 1,
    (2, 1): 1,
    (2, 2): 1,
    (3, 1): 1,
    (3, 2): 1,
    (3, 3): 1,
    (4, 1): 1,
    (4, 2): 1,
    (4, 3): 1,
    (4, 4): 1,
    (4, 5): 1,
}


@pytest.mark.parametrize(
    "wtd, n, p_n, slices",
    [
        (
            "add",
            None,
            None,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 0],
                (2, 2): [0, 0],
                (3, 1): [0, 0],
                (3, 2): [0, 0],
                (3, 3): [0, 0],
                (4, 1): [0, 0],
                (4, 2): [0, 0],
                (4, 3): [0, 0],
                (4, 4): [0, 0],
                (4, 5): [0, 0],
            },
        ),
        (
            "add",
            2,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 1],
                (2, 2): [1, 0],
                (3, 1): [1, 0],
                (3, 2): [1, 0],
                (3, 3): [1, 0],
                (4, 1): [1, 0],
                (4, 2): [1, 0],
                (4, 3): [1, 0],
                (4, 4): [1, 0],
                (4, 5): [1, 0],
            },
        ),
        (
            "add",
            2,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 2],
                (2, 2): [2, 0],
                (3, 1): [2, 0],
                (3, 2): [2, 0],
                (3, 3): [2, 0],
                (4, 1): [2, 0],
                (4, 2): [2, 0],
                (4, 3): [2, 0],
                (4, 4): [2, 0],
                (4, 5): [2, 0],
            },
        ),
        (
            "add",
            2,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 3],
                (2, 2): [3, 0],
                (3, 1): [3, 0],
                (3, 2): [3, 0],
                (3, 3): [3, 0],
                (4, 1): [3, 0],
                (4, 2): [3, 0],
                (4, 3): [3, 0],
                (4, 4): [3, 0],
                (4, 5): [3, 0],
            },
        ),
        (
            "add",
            4,
            4,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 3],
                (2, 2): [3, 0],
                (3, 1): [3, 0],
                (3, 2): [3, 0],
                (3, 3): [3, 0],
                (4, 1): [3, 0],
                (4, 2): [3, 0],
                (4, 3): [3, 0],
                (4, 4): [3, 1],
                (4, 5): [4, 0],
            },
        ),
        (
            "add",
            4,
            4,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 3],
                (2, 2): [3, 0],
                (3, 1): [3, 0],
                (3, 2): [3, 0],
                (3, 3): [3, 0],
                (4, 1): [3, 0],
                (4, 2): [3, 0],
                (4, 3): [3, 0],
                (4, 4): [3, 2],
                (4, 5): [5, 0],
            },
        ),
        (
            "add",
            4,
            4,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 3],
                (2, 2): [3, 0],
                (3, 1): [3, 0],
                (3, 2): [3, 0],
                (3, 3): [3, 0],
                (4, 1): [3, 0],
                (4, 2): [3, 0],
                (4, 3): [3, 0],
                (4, 4): [3, 3],
                (4, 5): [6, 0],
            },
        ),
        (
            "add",
            3,
            2,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 0],
                (2, 1): [0, 3],
                (2, 2): [3, 0],
                (3, 1): [3, 0],
                (3, 2): [3, 1],
                (3, 3): [4, 0],
                (4, 1): [4, 0],
                (4, 2): [4, 0],
                (4, 3): [4, 0],
                (4, 4): [4, 3],
                (4, 5): [7, 0],
            },
        ),
        (
            "add",
            1,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 3],
                (2, 2): [4, 0],
                (3, 1): [4, 0],
                (3, 2): [4, 1],
                (3, 3): [5, 0],
                (4, 1): [5, 0],
                (4, 2): [5, 0],
                (4, 3): [5, 0],
                (4, 4): [5, 3],
                (4, 5): [8, 0],
            },
        ),
        (
            "add",
            2,
            1,
            {
                # (n, p_n): [start, length]
                (1, 1): [0, 1],
                (2, 1): [1, 4],
                (2, 2): [5, 0],
                (3, 1): [5, 0],
                (3, 2): [5, 1],
                (3, 3): [6, 0],
                (4, 1): [6, 0],
                (4, 2): [6, 0],
                (4, 3): [6, 0],
                (4, 4): [6, 3],
                (4, 5): [9, 0],
            },
        ),
    ],
)
def test_interaction_parameters_slices_multiples(wtd, n, p_n, slices):
    if n is not None and p_n is not None:
        if wtd == "add":
            alphas = tuple([MULTIPLES_MULTIPLES[(n, p_n)] * _ for _ in ROLL[n - 1][0]])

            nus = ROLL[n - 1][1]
            MULTIPLES_MULTIPLES[(n, p_n)] += 1
            PARAMETERS_MULTIPLES.add(
                specs=(n, p_n, alphas, nus), parameter=np.zeros((3,) * n)
            )
        elif wtd == "remove":
            alphas = tuple([MULTIPLES_MULTIPLES[(n, p_n)] * _ for _ in ROLL[n - 1][0]])
            nus = ROLL[n - 1][1]
            MULTIPLES_MULTIPLES[(n, p_n)] = max(1, MULTIPLES_MULTIPLES[(n, p_n)] - 1)
            PARAMETERS_MULTIPLES.remove(specs=(n, p_n, alphas, nus))

    for key in slices:
        assert PARAMETERS_MULTIPLES._slices[key] == slices[key]


@given(
    data=st.lists(
        elements=st.tuples(
            st.integers(min_value=0, max_value=1), st.integers(min_value=1, max_value=4)
        ),
        min_size=0,
        max_size=1000,
    ),
)
def test_interaction_parameters_slices_random(data):
    parameters = _InteractionParameters()

    factors = {1: 1, 2: 1, 3: 1, 4: 1}

    for wtd, n in data:
        prev_slices = deepcopy(parameters._slices)

        nus = tuple([(0, 0, 0)] * (n - 1))

        alphas = tuple([factors[n] * (_ + 1) for _ in range(n)])

        if wtd == 0:
            parameters.add(specs=(n, 1, alphas, nus), parameter=np.zeros((3,) * n))
            delta = 1
            factors[n] += 1
        elif wtd == 1:
            prev_len = len(parameters._container)
            parameters.remove(specs=(n, 1, alphas, nus))

            delta = len(parameters._container) - prev_len

            if delta == -1:
                factors[n] = max(1, factors[n] - 1)

        # Check that there is no empty space in the slices
        tmp = list(parameters._slices.values())
        for i in range(1, len(tmp)):
            assert tmp[i][0] == sum([_[1] for _ in tmp[:i]])

        new_slices = parameters._slices

        # Check that the slices before (n, 1) are unchanged
        for _ in range(1, n):
            assert new_slices[(_, 1)] == prev_slices[(_, 1)]

        # Check that the slices at (n, 1) are updated correctly (amount changes)
        assert new_slices[(n, 1)][0] == prev_slices[(n, 1)][0]  # Same position
        assert (
            new_slices[(n, 1)][1] == prev_slices[(n, 1)][1] + delta
        )  # Different length

        # Check that the slices after (n, 1) are updated correctly (position changes)
        for _ in range(n + 1, 5):
            assert (
                new_slices[(_, 1)][0] == prev_slices[(_, 1)][0] + delta
            )  # Same position
            assert new_slices[(_, 1)][1] == prev_slices[(_, 1)][1]  # Same length


def test_add():
    p1 = _InteractionParameters()
    p21 = _InteractionParameters()

    p1.add(specs=(1, 1, (), (1,)), parameter=np.zeros((3,)))
    p21.add(specs=(2, 1, ((0, 0, 0),), (0, 0)), parameter=np.zeros((3, 3)))

    p = p1 + p21

    assert p._slices == {
        (1, 1): [0, 1],
        (2, 1): [1, 1],
        (2, 2): [2, 0],
        (3, 1): [2, 0],
        (3, 2): [2, 0],
        (3, 3): [2, 0],
        (4, 1): [2, 0],
        (4, 2): [2, 0],
        (4, 3): [2, 0],
        (4, 4): [2, 0],
        (4, 5): [2, 0],
    }

    assert p._container[0][0] == (1, 1, (), (1,))
    assert p._container[1][0] == (2, 1, ((0, 0, 0),), (0, 0))

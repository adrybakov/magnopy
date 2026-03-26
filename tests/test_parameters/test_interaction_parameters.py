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
import pytest
import numpy as np

from magnopy._parameters._interaction_parameters import (
    _get_specs,
    _validate_parameter,
    _InteractionParameters,
)


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
    specs = _get_specs(alphas=alphas, nus=nus)

    assert specs[0] == n
    assert specs[1] == p_n
    assert specs[2] == alphas
    assert specs[3][0] == (0, 0, 0)


@pytest.mark.parametrize(
    "n, parameter",
    [
        (1, np.zeros((1,))),
        (2, np.zeros((3, 4))),
        (3, np.zeros((3, 2, 3))),
        (4, np.zeros((2, 3, 3, 3))),
        (1, np.zeros((3, 3))),
        (2, np.zeros((3))),
        (3, np.zeros((3, 3, 3, 3))),
        (4, np.zeros((3, 3, 3))),
        (1, [1, 2, 3]),
    ],
)
def test_validate_parameter_fails(n, parameter):
    with pytest.raises(ValueError):
        _validate_parameter(n=n, parameter=parameter)


@pytest.mark.parametrize(
    "n, parameter",
    [
        (1, np.zeros((3,))),
        (2, np.zeros((3, 3))),
        (3, np.zeros((3, 3, 3))),
        (4, np.zeros((3, 3, 3, 3))),
    ],
)
def test_validate_parameter_passes(n, parameter):
    _validate_parameter(n=n, parameter=parameter)


def test_interaction_parameters_add():
    parameters = _InteractionParameters()
    parameters.add(
        alphas=(0, 1), nus=((1, 0, 0), (0, 0, 2)), parameter=np.zeros((3, 3))
    )

    assert len(parameters._container) == 1
    assert parameters._container[0][0] == (2, 2, (0, 1), ((0, 0, 0), (-1, 0, 2)))
    assert np.allclose(parameters._container[0][1], np.zeros((3, 3)))


def test_interaction_parameters_remove():
    parameters = _InteractionParameters()
    parameters.add(
        alphas=(0, 1), nus=((1, 0, 0), (0, 0, 2)), parameter=np.zeros((3, 3))
    )

    parameters.remove(alphas=(1, 0), nus=((1, 0, 0), (0, 0, 2)))
    assert len(parameters._container) == 1

    parameters.remove(alphas=(0, 1), nus=((0, 0, 0), (-1, 0, 2)))
    assert len(parameters._container) == 0


def test_interaction_parameters_order():
    parameters = _InteractionParameters()
    parameters.add(alphas=(0,), nus=((3, 0, 1),), parameter=np.zeros((3,)))
    parameters.add(
        alphas=(0, 1), nus=((0, 0, 0), (0, 0, 2)), parameter=np.zeros((3, 3))
    )
    parameters.add(
        alphas=(0, 0), nus=((1, 0, 0), (0, 0, 2)), parameter=np.zeros((3, 3))
    )

    assert len(parameters._container) == 3
    assert parameters._container[0][0] == (1, 1, (0,), ((0, 0, 0),))
    assert parameters._container[1][0] == (2, 2, (0, 0), ((0, 0, 0), (-1, 0, 2)))
    assert parameters._container[2][0] == (2, 2, (0, 1), ((0, 0, 0), (0, 0, 2)))

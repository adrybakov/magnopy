# MAGNOPY - Python package for magnons.
# Copyright (C) 2023-2025 Magnopy Team
#
# e-mail: anry@uv.es, web: magnopy.com
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


import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as harrays

from magnopy import Convention, SpinHamiltonian
from magnopy._spinham._c421 import _get_primary_p421

MAX_MODULUS = 1e8
ARRAY_3x3x3x3 = harrays(
    np.float64,
    (3, 3, 3, 3),
    elements=st.floats(min_value=-MAX_MODULUS, max_value=MAX_MODULUS),
)
RANDOM_UC = harrays(int, (4, 3), elements=st.integers(min_value=-1000, max_value=1000))


@given(
    st.integers(),
    st.integers(),
    st.tuples(st.integers(), st.integers(), st.integers()),
    ARRAY_3x3x3x3,
)
def test_add_421(alpha, beta, nu, parameter):
    atoms = {"names": ["Cr" for _ in range(9)], "spins": [1 for _ in range(9)]}

    spinham = SpinHamiltonian(cell=np.eye(3), atoms=atoms, convention=Convention())

    if 0 <= alpha < len(spinham.atoms.names) and 0 <= beta < len(spinham.atoms.names):
        spinham.add_421(alpha, beta, nu, parameter)
    else:
        with pytest.raises(ValueError):
            spinham.add_421(alpha, beta, nu, parameter)


@given(
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.tuples(st.integers(), st.integers(), st.integers()),
    st.integers(min_value=0, max_value=8),
    st.integers(min_value=0, max_value=8),
    st.tuples(st.integers(), st.integers(), st.integers()),
    ARRAY_3x3x3x3,
)
def test_add_421_sorting(
    alpha1,
    beta1,
    nu1,
    alpha2,
    beta2,
    nu2,
    alpha3,
    beta3,
    nu3,
    alpha4,
    beta4,
    nu4,
    parameter,
):
    atoms = {"names": ["Cr" for _ in range(9)], "spins": [1 for _ in range(9)]}

    spinham = SpinHamiltonian(cell=np.eye(3), atoms=atoms, convention=Convention())

    spinham.add_421(alpha1, beta1, nu1, parameter)

    if [alpha1, beta1, nu1] == [alpha2, beta2, nu2]:
        with pytest.raises(ValueError):
            spinham.add_421(alpha2, beta2, nu2, parameter)
    else:
        spinham.add_421(alpha2, beta2, nu2, parameter)

    spinham.add_421(alpha3, beta3, nu3, parameter, replace=True)
    spinham.add_421(alpha4, beta4, nu4, parameter, replace=True)

    for i in range(len(spinham._421) - 1):
        assert spinham._421[i][:-1] <= spinham._421[i + 1][:-1]


@given(
    st.integers(min_value=0, max_value=2),
    st.integers(min_value=0, max_value=2),
    st.tuples(st.integers(), st.integers(), st.integers()),
    RANDOM_UC,
)
def test_remove_421(r_alpha, r_beta, r_nu, nus):
    atoms = {"names": ["Cr" for _ in range(4)], "spins": [1 for _ in range(4)]}

    spinham = SpinHamiltonian(cell=np.eye(3), atoms=atoms, convention=Convention())

    for alpha in range(len(spinham.atoms.names)):
        for beta in range(alpha, len(spinham.atoms.names)):
            for nu in nus:
                nu = (int(nu[0]), int(nu[1]), int(nu[2]))
                spinham.add_421(alpha, beta, nu, np.ones((3, 3, 3, 3)), replace=True)

    bond = [r_alpha, r_beta, r_nu]
    if 0 <= r_alpha < len(spinham.atoms.names) and 0 <= r_beta < len(
        spinham.atoms.names
    ):
        original_bonds = [tmp[:-1] for tmp in spinham._421]
        original_length = len(spinham._421)

        spinham.remove_421(*bond)

        primary_bond = list(_get_primary_p421(*bond))
        if primary_bond in original_bonds:
            updated_bonds = [tmp[:-1] for tmp in spinham._421]

            assert len(spinham._421) == original_length - 1
            assert bond not in updated_bonds
            assert primary_bond not in updated_bonds
        else:
            assert len(spinham._421) == original_length

    else:
        with pytest.raises(ValueError):
            spinham.remove_421(*bond)

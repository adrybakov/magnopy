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

from magnopy import Convention, SpinHamiltonian


MAX_MODULUS = 1e8

CASES = [
    (1, 1),
    (2, 1),
    (2, 2),
    (3, 1),
    (3, 2),
    (3, 3),
    (4, 1),
    (4, 2),
    (4, 3),
    (4, 4),
    (4, 5),
]


@st.composite
def strategy_11(draw, alpha_max):
    alpha_1 = draw(st.integers(min_value=0, max_value=alpha_max))

    return ((), (alpha_1,))


@st.composite
def strategy_21(draw, alpha_max):
    alpha_1 = draw(st.integers(min_value=0, max_value=alpha_max))

    return (((0, 0, 0),), (alpha_1, alpha_1))


@st.composite
def strategy_22(draw, alpha_max):
    nu_2 = draw(
        st.tuples(
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
        )
    )
    alpha_1 = draw(st.integers(min_value=0, max_value=alpha_max))
    alpha_2 = draw(
        st.integers(min_value=0, max_value=alpha_max).filter(
            # Ensure the second site to be different from the first one
            lambda alpha_2: (nu_2, alpha_2) != ((0, 0, 0), alpha_1)
        )
    )
    return ((nu_2,), (alpha_1, alpha_2))


@st.composite
def strategy_31(draw, alpha_max):
    alpha_1 = draw(st.integers(min_value=0, max_value=alpha_max))
    return (((0, 0, 0), (0, 0, 0)), (alpha_1, alpha_1, alpha_1))


@st.composite
def strategy_32(draw, alpha_max):
    nu_2 = draw(
        st.tuples(
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
        )
    )
    alpha_1 = draw(st.integers(min_value=0, max_value=alpha_max))
    alpha_2 = draw(
        st.integers(min_value=0, max_value=alpha_max).filter(
            # Ensure the second site to be different from the first one
            lambda alpha_2: (nu_2, alpha_2) != ((0, 0, 0), alpha_1)
        )
    )

    index = draw(st.integers(min_value=0, max_value=2))

    if index == 0:
        return ((nu_2, nu_2), (alpha_1, alpha_2, alpha_2))
    elif index == 1:
        return ((nu_2, (0, 0, 0)), (alpha_1, alpha_2, alpha_1))
    else:
        return (((0, 0, 0), nu_2), (alpha_1, alpha_1, alpha_2))


@st.composite
def strategy_33(draw, alpha_max):
    nu_2 = draw(
        st.tuples(
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
        )
    )
    nu_3 = draw(
        st.tuples(
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
        )
    )
    alpha_1 = draw(st.integers(min_value=0, max_value=alpha_max))
    alpha_2 = draw(
        st.integers(min_value=0, max_value=alpha_max).filter(
            # Ensure the second site to be different from the first one
            lambda alpha_2: (nu_2, alpha_2) != ((0, 0, 0), alpha_1)
        )
    )
    alpha_3 = draw(
        st.integers(min_value=0, max_value=alpha_max).filter(
            # Ensure the third site to be different from the first two ones
            lambda alpha_3: (
                (nu_3, alpha_3) != ((0, 0, 0), alpha_1)
                and (nu_3, alpha_3) != (nu_2, alpha_2)
            )
        )
    )

    return ((nu_2, nu_3), (alpha_1, alpha_2, alpha_3))


@st.composite
def strategy_41(draw, alpha_max):
    alpha_1 = draw(st.integers(min_value=0, max_value=alpha_max))
    return (((0, 0, 0), (0, 0, 0), (0, 0, 0)), (alpha_1, alpha_1, alpha_1, alpha_1))


@st.composite
def strategy_42(draw, alpha_max):
    nu_2 = draw(
        st.tuples(
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
        )
    )
    alpha_1 = draw(st.integers(min_value=0, max_value=alpha_max))
    alpha_2 = draw(
        st.integers(min_value=0, max_value=alpha_max).filter(
            # Ensure the second site to be different from the first one
            lambda alpha_2: (nu_2, alpha_2) != ((0, 0, 0), alpha_1)
        )
    )

    index = draw(st.integers(min_value=0, max_value=3))

    if index == 0:
        return ((nu_2, nu_2, nu_2), (alpha_1, alpha_2, alpha_2, alpha_2))
    elif index == 1:
        return ((nu_2, (0, 0, 0), (0, 0, 0)), (alpha_1, alpha_2, alpha_1, alpha_1))
    elif index == 2:
        return (((0, 0, 0), nu_2, (0, 0, 0)), (alpha_1, alpha_1, alpha_2, alpha_1))
    else:
        return (((0, 0, 0), (0, 0, 0), nu_2), (alpha_1, alpha_1, alpha_1, alpha_2))


@st.composite
def strategy_43(draw, alpha_max):
    nu_2 = draw(
        st.tuples(
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
        )
    )
    alpha_1 = draw(st.integers(min_value=0, max_value=alpha_max))
    alpha_2 = draw(
        st.integers(min_value=0, max_value=alpha_max).filter(
            # Ensure the second site to be different from the first one
            lambda alpha_2: (nu_2, alpha_2) != ((0, 0, 0), alpha_1)
        )
    )

    index = draw(st.integers(min_value=0, max_value=2))

    if index == 0:
        return (((0, 0, 0), nu_2, nu_2), (alpha_1, alpha_1, alpha_2, alpha_2))
    elif index == 1:
        return ((nu_2, (0, 0, 0), nu_2), (alpha_1, alpha_2, alpha_1, alpha_2))
    else:
        return ((nu_2, nu_2, (0, 0, 0)), (alpha_1, alpha_2, alpha_2, alpha_1))


@st.composite
def strategy_44(draw, alpha_max):
    nu_2 = draw(
        st.tuples(
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
        )
    )
    nu_3 = draw(
        st.tuples(
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
        )
    )
    alpha_1 = draw(st.integers(min_value=0, max_value=alpha_max))
    alpha_2 = draw(
        st.integers(min_value=0, max_value=alpha_max).filter(
            # Ensure the second site to be different from the first one
            lambda alpha_2: (nu_2, alpha_2) != ((0, 0, 0), alpha_1)
        )
    )
    alpha_3 = draw(
        st.integers(min_value=0, max_value=alpha_max).filter(
            # Ensure the third site to be different from the first two ones
            lambda alpha_3: (
                (nu_3, alpha_3) != ((0, 0, 0), alpha_1)
                and (nu_3, alpha_3) != (nu_2, alpha_2)
            )
        )
    )

    index = draw(st.integers(min_value=0, max_value=5))

    if index == 0:
        return (((0, 0, 0), nu_2, nu_3), (alpha_1, alpha_1, alpha_2, alpha_3))
    elif index == 1:
        return ((nu_2, (0, 0, 0), nu_3), (alpha_1, alpha_2, alpha_1, alpha_3))
    elif index == 2:
        return ((nu_2, nu_3, (0, 0, 0)), (alpha_1, alpha_2, alpha_3, alpha_1))
    elif index == 3:
        return ((nu_2, nu_2, nu_3), (alpha_1, alpha_2, alpha_2, alpha_3))
    elif index == 4:
        return ((nu_2, nu_3, nu_2), (alpha_1, alpha_2, alpha_3, alpha_2))
    else:
        return ((nu_2, nu_3, nu_3), (alpha_1, alpha_2, alpha_3, alpha_3))


@st.composite
def strategy_45(draw, alpha_max):
    nu_2 = draw(
        st.tuples(
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
        )
    )
    nu_3 = draw(
        st.tuples(
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
        )
    )
    nu_4 = draw(
        st.tuples(
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
            st.integers(min_value=-100, max_value=100),
        )
    )
    alpha_1 = draw(st.integers(min_value=0, max_value=alpha_max))
    alpha_2 = draw(
        st.integers(min_value=0, max_value=alpha_max).filter(
            # Ensure the second site to be different from the first one
            lambda alpha_2: (nu_2, alpha_2) != ((0, 0, 0), alpha_1)
        )
    )
    alpha_3 = draw(
        st.integers(min_value=0, max_value=alpha_max).filter(
            # Ensure the third site to be different from the first two ones
            lambda alpha_3: (
                (nu_3, alpha_3) != ((0, 0, 0), alpha_1)
                and (nu_3, alpha_3) != (nu_2, alpha_2)
            )
        )
    )
    alpha_4 = draw(
        st.integers(min_value=0, max_value=alpha_max).filter(
            # Ensure the fourth site to be different from the first three ones
            lambda alpha_4: (
                (nu_4, alpha_4) != ((0, 0, 0), alpha_1)
                and (nu_4, alpha_4) != (nu_2, alpha_2)
                and (nu_4, alpha_4) != (nu_3, alpha_3)
            )
        )
    )

    return ((nu_2, nu_3, nu_4), (alpha_1, alpha_2, alpha_3, alpha_4))


def position_strategy(n, p_n, alpha_max):
    r"""
    Returns
    -------
    (nus, alphas)
    """

    if n == 1 and p_n == 1:
        return strategy_11(alpha_max=alpha_max)
    elif n == 2 and p_n == 1:
        return strategy_21(alpha_max=alpha_max)
    elif n == 2 and p_n == 2:
        return strategy_22(alpha_max=alpha_max)
    elif n == 3 and p_n == 1:
        return strategy_31(alpha_max=alpha_max)
    elif n == 3 and p_n == 2:
        return strategy_32(alpha_max=alpha_max)
    elif n == 3 and p_n == 3:
        return strategy_33(alpha_max=alpha_max)
    elif n == 4 and p_n == 1:
        return strategy_41(alpha_max=alpha_max)
    elif n == 4 and p_n == 2:
        return strategy_42(alpha_max=alpha_max)
    elif n == 4 and p_n == 3:
        return strategy_43(alpha_max=alpha_max)
    elif n == 4 and p_n == 4:
        return strategy_44(alpha_max=alpha_max)
    elif n == 4 and p_n == 5:
        return strategy_45(alpha_max=alpha_max)
    else:
        raise NotImplementedError(
            f"position_strategy not implemented for n={n}, p_n={p_n}"
        )


def parameter_strategy(n):
    return harrays(
        dtype=np.float64,
        shape=tuple([3] * n),
        elements=st.floats(min_value=-MAX_MODULUS, max_value=MAX_MODULUS),
    )


def get_spinham(natoms=9):
    atoms = dict(
        names=[f"Cr{_ + 1}" for _ in range(natoms)],
        spins=[_ + 1 for _ in range(natoms)],
        positions=[[1 / natoms * i] * 3 for i in range(natoms)],
        g_factors=[2] * natoms,
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


@pytest.mark.parametrize("n, p_n", CASES)
@given(data=st.data())
def test_add(n, p_n, data):
    spinham = get_spinham()
    natoms = len(spinham.atoms.names)

    nus, alphas = data.draw(
        position_strategy(n=n, p_n=p_n, alpha_max=natoms * 2), label="nus, alphas"
    )

    parameter = data.draw(parameter_strategy(n=n), label="parameter")

    if all(0 <= alpha < natoms for alpha in alphas):
        spinham.add(nus=nus, alphas=alphas, parameter=parameter)
    else:
        with pytest.raises(ValueError):
            spinham.add(nus=nus, alphas=alphas, parameter=parameter)


@pytest.mark.parametrize("n, p_n", CASES)
@pytest.mark.parametrize(
    "when_present, factor",
    [("skip", 1.0), ("replace", 2.0), ("sum", 3.0), ("mean", 1.5)],
)
@given(data=st.data())
def test_add_when_present(n, p_n, when_present, factor, data):
    spinham = get_spinham()
    natoms = len(spinham.atoms.names)

    nus, alphas = data.draw(
        position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1), label="nus, alphas"
    )

    parameter = data.draw(parameter_strategy(n=n), label="parameter")

    spinham.add(nus=nus, alphas=alphas, parameter=parameter)

    with pytest.raises(ValueError):
        spinham.add(nus=nus, alphas=alphas, parameter=parameter)

    spinham.add(
        nus=nus, alphas=alphas, parameter=2 * parameter, when_present=when_present
    )

    assert np.allclose(spinham.parameters(n=n, p_n=p_n)[0][2], factor * parameter)


@pytest.mark.parametrize("n, p_n", CASES)
@given(data=st.data())
def test_add_sorting(n, p_n, data):
    spinham = get_spinham()
    natoms = len(spinham.atoms.names)

    v1_nus, v1_alphas = data.draw(
        position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1), label="nus, alphas"
    )
    v2_nus, v2_alphas = data.draw(
        position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1), label="nus, alphas"
    )
    v3_nus, v3_alphas = data.draw(
        position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1), label="nus, alphas"
    )
    v4_nus, v4_alphas = data.draw(
        position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1), label="nus, alphas"
    )

    v1_parameter = data.draw(parameter_strategy(n=n), label="parameter")
    v2_parameter = data.draw(parameter_strategy(n=n), label="parameter")
    v3_parameter = data.draw(parameter_strategy(n=n), label="parameter")
    v4_parameter = data.draw(parameter_strategy(n=n), label="parameter")

    spinham.add(nus=v1_nus, alphas=v1_alphas, parameter=v1_parameter)

    if v2_alphas == v1_alphas and v1_nus == v2_nus:
        with pytest.raises(ValueError):
            spinham.add(nus=v2_nus, alphas=v2_alphas, parameter=v2_parameter)
    else:
        spinham.add(nus=v2_nus, alphas=v2_alphas, parameter=v2_parameter)

    spinham.add(
        nus=v3_nus, alphas=v3_alphas, parameter=v3_parameter, when_present="replace"
    )
    spinham.add(
        nus=v4_nus, alphas=v4_alphas, parameter=v4_parameter, when_present="replace"
    )

    for i in range(len(spinham.parameters()) - 1):
        assert spinham.parameters()[i][:2] <= spinham.parameters()[i + 1][:2]


@pytest.mark.parametrize("n, p_n", CASES)
@given(data=st.data())
def test_remove(n, p_n, data):
    spinham = get_spinham()
    natoms = len(spinham.atoms.names)

    for i in range(natoms):
        nus, alphas = data.draw(
            position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1),
            label=f"(v{i}) nus, alphas",
        )
        spinham.add(
            nus=nus,
            alphas=alphas,
            parameter=np.ones(tuple([3] * n)),
            when_present="skip",
        )

    nus, alphas = data.draw(
        position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1), label="nus, alphas"
    )

    if all(0 <= alpha < natoms for alpha in alphas):
        pass
    else:
        with pytest.raises(ValueError):
            spinham.remove(nus=nus, alphas=alphas)


@pytest.mark.parametrize("n, p_n", CASES)
@given(
    data=st.data(),
    number=st.floats(min_value=0.1, max_value=1e4),
    index=st.integers(min_value=0, max_value=1),
)
def test_mul_rmul(n, p_n, data, number, index):
    spinham = get_spinham()
    natoms = len(spinham.atoms.names)

    v1_nus, v1_alphas = data.draw(
        position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1), label="nus, alphas"
    )
    v2_nus, v2_alphas = data.draw(
        position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1), label="nus, alphas"
    )
    v3_nus, v3_alphas = data.draw(
        position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1), label="nus, alphas"
    )

    parameter = data.draw(parameter_strategy(n=n), label="parameter")

    spinham.add(nus=v1_nus, alphas=v1_alphas, parameter=parameter)
    spinham.add(
        nus=v2_nus, alphas=v2_alphas, parameter=parameter * 1.42, when_present="sum"
    )
    spinham.add(
        nus=v3_nus, alphas=v3_alphas, parameter=parameter / 3, when_present="sum"
    )

    if index == 0:
        m_spinham = spinham * number
    else:
        m_spinham = number * spinham

    assert spinham.M == m_spinham.M

    assert len(spinham.parameters(n=n, p_n=p_n)) == len(
        m_spinham.parameters(n=n, p_n=p_n)
    )

    for i in range(len(spinham.parameters(n=n, p_n=p_n))):
        assert (
            spinham.parameters(n=n, p_n=p_n)[i][0]
            == m_spinham.parameters(n=n, p_n=p_n)[i][0]
        )
        assert (
            spinham.parameters(n=n, p_n=p_n)[i][1]
            == m_spinham.parameters(n=n, p_n=p_n)[i][1]
        )
        assert np.allclose(
            number * spinham.parameters(n=n, p_n=p_n)[i][2],
            m_spinham.parameters(n=n, p_n=p_n)[i][2],
        )


@pytest.mark.parametrize("n, p_n", CASES)
@given(data=st.data())
@settings(deadline=2000)
def test___add__(n, p_n, data):
    spinham1 = get_spinham()
    spinham2 = get_spinham()
    natoms = len(spinham1.atoms.names)

    v_nus_alphas = data.draw(
        st.lists(
            position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1),
            min_size=4,
            max_size=4,
            unique=True,
        ),
        label="positions",
    )

    v_nus_alphas.sort(key=lambda x: (x[0], x[1]))

    v1_nus, v1_alphas = v_nus_alphas[0]
    v2_nus, v2_alphas = v_nus_alphas[1]
    v3_nus, v3_alphas = v_nus_alphas[2]
    v4_nus, v4_alphas = v_nus_alphas[3]

    v1_parameter = data.draw(parameter_strategy(n=n), label="parameter")
    v2_parameter = data.draw(parameter_strategy(n=n), label="parameter")
    v3_parameter = data.draw(parameter_strategy(n=n), label="parameter")
    v4_parameter = data.draw(parameter_strategy(n=n), label="parameter")
    v5_parameter = data.draw(parameter_strategy(n=n), label="parameter")
    v6_parameter = data.draw(parameter_strategy(n=n), label="parameter")

    spinham1.add(nus=v1_nus, alphas=v1_alphas, parameter=v1_parameter)
    spinham1.add(nus=v2_nus, alphas=v2_alphas, parameter=v2_parameter)
    spinham1.add(nus=v3_nus, alphas=v3_alphas, parameter=v3_parameter)

    assert len(spinham1.parameters(n=n, p_n=p_n)) == 3

    spinham2.add(nus=v1_nus, alphas=v1_alphas, parameter=v4_parameter)
    spinham2.add(nus=v2_nus, alphas=v2_alphas, parameter=v5_parameter)
    spinham2.add(nus=v4_nus, alphas=v4_alphas, parameter=v6_parameter)

    assert len(spinham1.parameters(n=n, p_n=p_n)) == 3

    sum_spinham = spinham1 + spinham2

    assert len(sum_spinham.parameters(n=n, p_n=p_n)) == 4

    for i in range(2):
        assert np.allclose(
            sum_spinham.parameters(n=n, p_n=p_n)[i][2],
            spinham1.parameters(n=n, p_n=p_n)[i][2]
            + spinham2.parameters(n=n, p_n=p_n)[i][2],
        )

    assert np.allclose(
        sum_spinham.parameters(n=n, p_n=p_n)[2][2],
        spinham1.parameters(n=n, p_n=p_n)[2][2],
    )
    assert np.allclose(
        sum_spinham.parameters(n=n, p_n=p_n)[3][2],
        spinham2.parameters(n=n, p_n=p_n)[2][2],
    )


@pytest.mark.parametrize("n, p_n", CASES)
@given(data=st.data(), amount=st.integers(min_value=1, max_value=7))
def test_iterator(n, p_n, data, amount):
    spinham = get_spinham()
    natoms = len(spinham.atoms.names)

    for i in range(amount):
        nus, alphas = data.draw(
            position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1),
            label=f"(v{i}) nus, alphas",
        )
        parameter = data.draw(parameter_strategy(n=n), label="parameter")
        spinham.add(
            nus=nus,
            alphas=alphas,
            parameter=parameter,
            when_present="skip",
        )

    as_list = list(spinham.parameters(n=n, p_n=p_n))

    counter = 0
    for i, (nus, alphas, parameter) in enumerate(spinham.parameters(n=n, p_n=p_n)):
        counter += 1
        assert spinham.parameters(n=n, p_n=p_n)[i][:2] == (nus, alphas)
        assert np.allclose(spinham.parameters(n=n, p_n=p_n)[i][2], parameter)

        spinham.parameters(n=n, p_n=p_n)[i] = parameter.copy() * 2

        assert np.allclose(spinham.parameters(n=n, p_n=p_n)[i][2], 2 * parameter)

    assert counter == len(spinham.parameters(n=n, p_n=p_n))
    assert counter == len(as_list)


@pytest.mark.parametrize("n, p_n", CASES)
@given(data=st.data(), amount=st.integers(min_value=1, max_value=7))
def test_magnetic_atoms(n, p_n, data, amount):
    spinham = get_spinham()
    natoms = len(spinham.atoms.names)

    unique_alphas = set()
    for i in range(amount):
        nus, alphas = data.draw(
            position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1),
            label=f"(v{i}) nus, alphas",
        )
        spinham.add(
            nus=nus,
            alphas=alphas,
            parameter=np.ones(tuple([3] * n)),
            when_present="skip",
        )

        for alpha in alphas:
            unique_alphas.add(alpha)

    unique_alphas = sorted(list(unique_alphas))

    assert spinham.M == len(unique_alphas)

    for i, alpha in enumerate(unique_alphas):
        assert spinham.magnetic_atoms.names[i] == spinham.atoms.names[alpha]


@pytest.mark.parametrize("n, p_n", CASES)
@given(data=st.data(), amount=st.integers(min_value=1, max_value=7))
def test_get_empty(n, p_n, data, amount):
    spinham = get_spinham()
    natoms = len(spinham.atoms.names)

    for i in range(amount):
        nus, alphas = data.draw(
            position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1),
            label=f"(v{i}) nus, alphas",
        )
        spinham.add(
            nus=nus,
            alphas=alphas,
            parameter=np.ones(tuple([3] * n)),
            when_present="skip",
        )

    empty_spinham = spinham.get_empty()

    assert empty_spinham.M == 0
    assert len(empty_spinham.parameters(n=n, p_n=p_n)) == 0
    assert len(empty_spinham.magnetic_atoms.names) == 0
    assert len(empty_spinham.parameters()) == 0
    assert len(empty_spinham._parameters._container) == 0
    assert empty_spinham.atoms.names == spinham.atoms.names


@pytest.mark.parametrize("n, p_n", CASES)
@given(data=st.data(), amount=st.integers(min_value=1, max_value=7))
def test_lists_not_tuples(n, p_n, data, amount):
    spinham = get_spinham()
    natoms = len(spinham.atoms.names)

    for i in range(amount):
        nus, alphas = data.draw(
            position_strategy(n=n, p_n=p_n, alpha_max=natoms - 1),
            label=f"(v{i}) nus, alphas",
        )
        spinham.add(
            nus=list(nus),
            alphas=list(alphas),
            parameter=np.ones(tuple([3] * n)),
            when_present="skip",
        )

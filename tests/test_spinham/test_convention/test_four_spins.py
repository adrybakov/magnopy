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
from hypothesis import given
from hypothesis import strategies as st

from magnopy import Convention


@given(st.floats(allow_nan=False), st.floats(allow_nan=False))
def test_c41(value, new_value):
    convention = Convention(c41=value)

    assert convention.c41 == value

    with pytest.raises(AttributeError):
        convention.c41 = new_value


@given(st.floats(allow_nan=False))
def test_eq_c41(c41):
    convention1 = Convention(c41=c41)
    convention2 = Convention(c41=c41)
    convention3 = Convention(c41=3 if c41 != 3 else 4)
    convention4 = Convention()

    assert convention1 == convention2
    assert convention1 != convention3
    assert convention1 != convention4
    assert convention2 != convention3
    assert convention2 != convention4
    assert convention3 != convention4


def test_get_modified_c41():
    convention = Convention(
        spin_normalized=True,
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
    )

    mod_convention = convention.get_modified(c41=2)

    assert mod_convention.spin_normalized
    assert mod_convention.multiple_counting
    assert mod_convention.c1 == 1
    assert mod_convention.c21 == 1
    assert mod_convention.c22 == 1
    assert mod_convention.c31 == 1
    assert mod_convention.c32 == 1
    assert mod_convention.c33 == 1
    assert mod_convention.c41 == 2
    assert mod_convention.c42 == 1
    assert mod_convention.c43 == 1
    assert mod_convention.c44 == 1
    assert mod_convention.c45 == 1


@given(st.floats(allow_nan=False), st.floats(allow_nan=False))
def test_c42(value, new_value):
    convention = Convention(c42=value)

    assert convention.c42 == value

    with pytest.raises(AttributeError):
        convention.c42 = new_value


@given(st.floats(allow_nan=False))
def test_eq_c42(c42):
    convention1 = Convention(c42=c42)
    convention2 = Convention(c42=c42)
    convention3 = Convention(c42=3 if c42 != 3 else 4)
    convention4 = Convention()

    assert convention1 == convention2
    assert convention1 != convention3
    assert convention1 != convention4
    assert convention2 != convention3
    assert convention2 != convention4
    assert convention3 != convention4


def test_get_modified_c42():
    convention = Convention(
        spin_normalized=True,
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
    )

    mod_convention = convention.get_modified(c42=2)

    assert mod_convention.spin_normalized
    assert mod_convention.multiple_counting
    assert mod_convention.c1 == 1
    assert mod_convention.c21 == 1
    assert mod_convention.c22 == 1
    assert mod_convention.c31 == 1
    assert mod_convention.c32 == 1
    assert mod_convention.c33 == 1
    assert mod_convention.c41 == 1
    assert mod_convention.c42 == 2
    assert mod_convention.c43 == 1
    assert mod_convention.c44 == 1
    assert mod_convention.c45 == 1


@given(st.floats(allow_nan=False), st.floats(allow_nan=False))
def test_c43(value, new_value):
    convention = Convention(c43=value)

    assert convention.c43 == value

    with pytest.raises(AttributeError):
        convention.c43 = new_value


@given(st.floats(allow_nan=False))
def test_eq_c43(c43):
    convention1 = Convention(c43=c43)
    convention2 = Convention(c43=c43)
    convention3 = Convention(c43=3 if c43 != 3 else 4)
    convention4 = Convention()

    assert convention1 == convention2
    assert convention1 != convention3
    assert convention1 != convention4
    assert convention2 != convention3
    assert convention2 != convention4
    assert convention3 != convention4


def test_get_modified_c43():
    convention = Convention(
        spin_normalized=True,
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
    )

    mod_convention = convention.get_modified(c43=2)

    assert mod_convention.spin_normalized
    assert mod_convention.multiple_counting
    assert mod_convention.c1 == 1
    assert mod_convention.c21 == 1
    assert mod_convention.c22 == 1
    assert mod_convention.c31 == 1
    assert mod_convention.c32 == 1
    assert mod_convention.c33 == 1
    assert mod_convention.c41 == 1
    assert mod_convention.c42 == 1
    assert mod_convention.c43 == 2
    assert mod_convention.c44 == 1
    assert mod_convention.c45 == 1


@given(st.floats(allow_nan=False), st.floats(allow_nan=False))
def test_c44(value, new_value):
    convention = Convention(c44=value)

    assert convention.c44 == value

    with pytest.raises(AttributeError):
        convention.c44 = new_value


@given(st.floats(allow_nan=False))
def test_eq_c44(c44):
    convention1 = Convention(c44=c44)
    convention2 = Convention(c44=c44)
    convention3 = Convention(c44=3 if c44 != 3 else 4)
    convention4 = Convention()

    assert convention1 == convention2
    assert convention1 != convention3
    assert convention1 != convention4
    assert convention2 != convention3
    assert convention2 != convention4
    assert convention3 != convention4


def test_get_modified_c44():
    convention = Convention(
        spin_normalized=True,
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
    )

    mod_convention = convention.get_modified(c44=2)

    assert mod_convention.spin_normalized
    assert mod_convention.multiple_counting
    assert mod_convention.c1 == 1
    assert mod_convention.c21 == 1
    assert mod_convention.c22 == 1
    assert mod_convention.c31 == 1
    assert mod_convention.c32 == 1
    assert mod_convention.c33 == 1
    assert mod_convention.c41 == 1
    assert mod_convention.c42 == 1
    assert mod_convention.c43 == 1
    assert mod_convention.c44 == 2
    assert mod_convention.c45 == 1


@given(st.floats(allow_nan=False), st.floats(allow_nan=False))
def test_c45(value, new_value):
    convention = Convention(c45=value)

    assert convention.c45 == value

    with pytest.raises(AttributeError):
        convention.c45 = new_value


@given(st.floats(allow_nan=False))
def test_eq_c45(c45):
    convention1 = Convention(c45=c45)
    convention2 = Convention(c45=c45)
    convention3 = Convention(c45=3 if c45 != 3 else 4)
    convention4 = Convention()

    assert convention1 == convention2
    assert convention1 != convention3
    assert convention1 != convention4
    assert convention2 != convention3
    assert convention2 != convention4
    assert convention3 != convention4


def test_get_modified_c45():
    convention = Convention(
        spin_normalized=True,
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
    )

    mod_convention = convention.get_modified(c45=2)

    assert mod_convention.spin_normalized
    assert mod_convention.multiple_counting
    assert mod_convention.c1 == 1
    assert mod_convention.c21 == 1
    assert mod_convention.c22 == 1
    assert mod_convention.c31 == 1
    assert mod_convention.c32 == 1
    assert mod_convention.c33 == 1
    assert mod_convention.c41 == 1
    assert mod_convention.c42 == 1
    assert mod_convention.c43 == 1
    assert mod_convention.c44 == 1
    assert mod_convention.c45 == 2

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

from magnopy._constants._units import (
    _PARAMETER_UNITS,
    _PARAMETER_UNITS_MAKEUP,
    _FREQ_UNITS,
    _FREQ_UNITS_MAKEUP,
    _ENERGY_UNITS,
    _ENERGY_UNITS_MAKEUP,
)


@pytest.mark.parametrize(
    "units, units_makeup",
    [
        (_PARAMETER_UNITS, _PARAMETER_UNITS_MAKEUP),
        (_FREQ_UNITS, _FREQ_UNITS_MAKEUP),
        (_ENERGY_UNITS, _ENERGY_UNITS_MAKEUP),
    ],
)
def test_keys_and_values(units, units_makeup):
    for key in units:
        assert key in units_makeup

    for key in units_makeup:
        assert key in units

    for key in units_makeup:
        assert units_makeup[key].lower() in units_makeup

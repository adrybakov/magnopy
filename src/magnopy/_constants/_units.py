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
from magnopy._constants._si import (
    BOLTZMANN_CONSTANT,
    ELECTRON_VOLT,
    JOULE,
    KELVIN,
    MILLI,
    RYDBERG_ENERGY,
    ERG,
    GIGA,
    TERA,
    PLANCK_CONSTANT,
)
from math import pi as PI


################################################################################
#                                    Energy                                    #
################################################################################

# Name : value when expressed in SI
_ENERGY_UNITS = {
    "ev": ELECTRON_VOLT,
    "mev": MILLI * ELECTRON_VOLT,
    "joule": JOULE,
    "j": JOULE,
    "ry": RYDBERG_ENERGY,
    "rydberg": RYDBERG_ENERGY,
    "erg": ERG,
}

# Name : Pretty name
_ENERGY_UNITS_MAKEUP = {
    "ev": "eV",
    "mev": "meV",
    "joule": "Joule",
    "j": "Joule",
    "ry": "Rydberg",
    "rydberg": "Rydberg",
    "erg": "Erg",
}

################################################################################
#                         Parameter of spin Hamiltonian                        #
################################################################################

# Name : value when expressed in SI
_PARAMETER_UNITS = {key: _ENERGY_UNITS[key] for key in _ENERGY_UNITS}
_PARAMETER_UNITS["k"] = BOLTZMANN_CONSTANT * KELVIN
_PARAMETER_UNITS["kelvin"] = BOLTZMANN_CONSTANT * KELVIN


# Name : Pretty name
_PARAMETER_UNITS_MAKEUP = {
    key: _ENERGY_UNITS_MAKEUP[key] for key in _ENERGY_UNITS_MAKEUP
}
_PARAMETER_UNITS_MAKEUP["k"] = "Kelvin"
_PARAMETER_UNITS_MAKEUP["kelvin"] = "Kelvin"

################################################################################
#                              Magnon frequencies                              #
################################################################################

# Name : value when expressed in SI
_FREQ_UNITS = {key: _ENERGY_UNITS[key] for key in _ENERGY_UNITS}
_FREQ_UNITS["hertz"] = 2 * PI * PLANCK_CONSTANT
_FREQ_UNITS["hz"] = 2 * PI * PLANCK_CONSTANT
_FREQ_UNITS["giga-hertz"] = 2 * PI * PLANCK_CONSTANT * GIGA
_FREQ_UNITS["ghz"] = 2 * PI * PLANCK_CONSTANT * GIGA
_FREQ_UNITS["tera-hertz"] = 2 * PI * PLANCK_CONSTANT * TERA
_FREQ_UNITS["thz"] = 2 * PI * PLANCK_CONSTANT * TERA


# Name : Pretty name
_FREQ_UNITS_MAKEUP = {key: _ENERGY_UNITS_MAKEUP[key] for key in _ENERGY_UNITS_MAKEUP}
_FREQ_UNITS_MAKEUP["hertz"] = "Hz"
_FREQ_UNITS_MAKEUP["hz"] = "Hz"
_FREQ_UNITS_MAKEUP["giga-hertz"] = "GHz"
_FREQ_UNITS_MAKEUP["ghz"] = "GHz"
_FREQ_UNITS_MAKEUP["tera-hertz"] = "THz"
_FREQ_UNITS_MAKEUP["thz"] = "THz"

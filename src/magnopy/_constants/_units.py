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
#                         Parameter of spinHamiltonian                         #
################################################################################

# Name : value when expressed in SI
_PARAMETER_UNITS = {
    "mev": MILLI * ELECTRON_VOLT,
    "joule": JOULE,
    "j": JOULE,
    "ry": RYDBERG_ENERGY,
    "rydberg": RYDBERG_ENERGY,
    "k": BOLTZMANN_CONSTANT * KELVIN,
    "kelvin": BOLTZMANN_CONSTANT * KELVIN,
    "erg": ERG,
}

# Name : Pretty name
_PARAMETER_UNITS_MAKEUP = {
    "mev": "meV",
    "joule": "Joule",
    "j": "Joule",
    "ry": "Rydberg",
    "rydberg": "Rydberg",
    "k": "Kelvin",
    "kelvin": "Kelvin",
    "erg": "Erg",
}

################################################################################
#                              Magnon frequencies                              #
################################################################################

# Name : value when expressed in SI
_FREQ_UNITS = {
    "mev": MILLI * ELECTRON_VOLT,
    "joule": JOULE,
    "j": JOULE,
    "ry": RYDBERG_ENERGY,
    "rydberg": RYDBERG_ENERGY,
    "erg": ERG,
    "hertz": 2 * PI * PLANCK_CONSTANT,
    "hz": 2 * PI * PLANCK_CONSTANT,
    "giga-hertz": 2 * PI * PLANCK_CONSTANT * GIGA,
    "ghz": 2 * PI * PLANCK_CONSTANT * GIGA,
    "tera-hertz": 2 * PI * PLANCK_CONSTANT * TERA,
    "thz": 2 * PI * PLANCK_CONSTANT * TERA,
}

# Name : Pretty name
_FREQ_UNITS_MAKEUP = {
    "mev": "meV",
    "joule": "Joule",
    "j": "Joule",
    "ry": "Rydberg",
    "rydberg": "Rydberg",
    "erg": "Erg",
    "hertz": "Hz",
    "hz": "Hz",
    "giga-hertz": "GHz",
    "ghz": "GHz",
    "tera-hertz": "THz",
    "thz": "THz",
}

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

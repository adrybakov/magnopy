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


R"""Pre-defined conventions of spin Hamiltonian"""

from magnopy._constants._si import (
    BOLTZMANN_CONSTANT,
    ELECTRON_VOLT,
    JOULE,
    KELVIN,
    MILLI,
    RYDBERG_ENERGY,
    ERG,
)

_CONVENTIONS = {
    "tb2j": dict(multiple_counting=True, spin_normalized=True, c21=-1, c22=-1),
    "grogu": dict(multiple_counting=True, spin_normalized=True, c21=1, c22=0.5),
    "vampire": dict(multiple_counting=True, spin_normalized=True, c21=-1, c22=-0.5),
    "spinw": dict(multiple_counting=True, spin_normalized=False, c21=1, c22=1),
}

# Name : value when expressed in SI
_SUPPORTED_UNITS = {
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
_SUPPORTED_UNITS_MAKEUP = {
    "mev": "meV",
    "joule": "Joule",
    "j": "Joule",
    "ry": "Rydberg",
    "rydberg": "Rydberg",
    "k": "Kelvin",
    "kelvin": "Kelvin",
    "erg": "Erg",
}

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
# Save local scope at this moment
from magnopy._constants._si import (
    BOLTZMANN_CONSTANT,
    ELECTRON_VOLT,
    JOULE,
    KELVIN,
    MILLI,
    RYDBERG_ENERGY,
    ERG,
)


old_dir = set(dir())
old_dir.add("old_dir")


def _convert_units(parameter, given_units="meV", return_units="meV"):
    r"""
    Convert the units of the parameter.

    Parameters
    ----------
    parameter : float or :numpy:`ndarray`
        Value of the parameter in the ``given_units``.
    given_units : str, default "meV"
        Units in which the parameter is given. Case-insensitive.
    return_units : str, default "meV"
        Units in  which the parameter shall be returned. Case-insensitive.


    Returns
    -------
    parameter : float or :numpy:`ndarray`
        Value of the parameter in the ``return_units``.

    Raises
    ------
    ValueError
        If ``given_units`` or ``return_units`` are not supported.
    """

    given_units = given_units.lower()
    return_units = return_units.lower()

    if given_units == return_units:
        return parameter

    # Name : value when expressed in SI
    SUPPORTED_UNITS = {
        "mev": MILLI * ELECTRON_VOLT,
        "joule": JOULE,
        "j": JOULE,
        "ry": RYDBERG_ENERGY,
        "rydberg": RYDBERG_ENERGY,
        "k": BOLTZMANN_CONSTANT * KELVIN,
        "kelvin": BOLTZMANN_CONSTANT * KELVIN,
        "erg": ERG,
    }

    if given_units not in SUPPORTED_UNITS:
        raise ValueError(
            f'Given units ("{given_units}") are not supported, please use one of\n  * '
            + "\n  * ".join(list(SUPPORTED_UNITS))
        )
    if return_units not in SUPPORTED_UNITS:
        raise ValueError(
            f'Return units ("{return_units}") are not supported, please use one of\n  * '
            + "\n  * ".join(list(SUPPORTED_UNITS))
        )

    return parameter * SUPPORTED_UNITS[given_units] / SUPPORTED_UNITS[return_units]


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir

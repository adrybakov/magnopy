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

from magnopy._constants._spinham_constants import _SUPPORTED_UNITS


old_dir = set(dir())
old_dir.add("old_dir")


def _get_conversion_factor(old_units="meV", new_units="meV"):
    r"""
    Convert the units of the parameter.

    Parameters
    ----------
    old_units : str, default "meV"
        Units in which the parameter is given. Case-insensitive.
    new_units : str, default "meV"
        Units in  which the parameter shall be returned. Case-insensitive.


    Returns
    -------
    conversion : float
        ``parameter_new_units = conversion_factor * parameter_old_units``.

    Raises
    ------
    ValueError
        If ``old_units`` or ``new_units`` are not supported.
    """

    old_units = old_units.lower()
    new_units = new_units.lower()

    if old_units == new_units:
        return 1.0

    if old_units not in _SUPPORTED_UNITS:
        raise ValueError(
            f'"{old_units}" Units are not supported, please use one of\n  * '
            + "\n  * ".join(list(_SUPPORTED_UNITS))
        )
    if new_units not in _SUPPORTED_UNITS:
        raise ValueError(
            f'"{new_units}" Units are not supported, please use one of\n  * '
            + "\n  * ".join(list(_SUPPORTED_UNITS))
        )

    return _SUPPORTED_UNITS[old_units] / _SUPPORTED_UNITS[new_units]


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir

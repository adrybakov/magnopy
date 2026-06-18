# ================================== LICENSE ===================================
# Magnopy - Python package for magnons.
#
# Copyright (C) 2023 Magnopy Team
#
# e-mail: anry@uv.es, web: magnopy.org
#
# This program is free software: you  can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the  Free Software
# Foundation,  either  version 3  of the License,  or (at your option) any later
# version.
#
# This program is distributed in the  hope  that it will be useful,  but WITHOUT
# ANY WARRANTY;  without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the  GNU General Public License  along with
# this program.  If not, see <https://www.gnu.org/licenses/>.
# ================================ END LICENSE =================================


from calendar import month_name
from datetime import datetime
import warnings

from magnopy import __doclink__, __release_date__, __version__

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")

# fmt: off
BINARY_LOGO  =  [
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,0,0,0,1,0,0,0,1,0,0,1,1,1,0,0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,1,1,0,0,1,1,1,1,0,0,1,0,0,0,1],
    [0,1,1,1,1,0,0,1,1,0,1,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,1,0,1,1],
    [0,1,1,1,1,0,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,0,1,1,0,1,0,1,0,1,0,1,0,0,0,1,0,1,1,1,1,0,0,0,1,1,1,0],
    [0,1,1,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0],
    [0,1,1,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
]

BINARY_CAT  =  [
    [1,0,0,0,1,0,0,0,0,0],
    [1,1,1,1,1,0,0,0,0,0],
    [1,0,1,0,1,0,0,0,0,0],
    [1,0,1,0,1,0,0,0,0,0],
    [1,1,1,1,1,0,0,0,0,0],
    [0,1,1,1,0,0,0,0,0,0],
    [0,1,1,1,0,0,0,1,1,0],
    [0,1,1,1,1,0,1,0,0,1],
    [0,1,1,1,1,0,1,0,0,1],
    [0,1,1,1,1,0,0,0,0,1],
    [0,1,1,1,1,0,0,0,0,1],
    [0,1,1,1,1,1,1,1,1,0],
]

BINARY_MAGNOPY_NARROW  =  [
    [1,0,0,0,1,0,0,1,1,1,0,0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,1,1,0,0,1,1,1,1,0,0,1,0,0,0,1],
    [1,1,0,1,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,1,0,1,1],
    [1,0,1,0,1,0,1,1,1,1,1,0,1,0,0,1,1,0,1,0,1,0,1,0,1,0,0,0,1,0,1,1,1,1,0,0,0,1,1,1,0],
    [1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0],
    [1,0,0,0,1,0,1,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0],
]

BINARY_MAGNOPY_WIDE = [
    [1,1,1,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,0,0,0,0,1,1],
    [1,1,1,1,0,0,1,1,1,1,0,0,1,1,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,1,1,0,0,1,1,0],
    [1,1,0,1,1,1,1,0,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0],
    [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
    [1,1,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
]

# fmt: on


def _convert(data, char_1="#", char_0=" "):
    return ["".join(char_1 if _ else char_0 for _ in row) for row in data]


def logo(date_time=False, comment_char=None, logo_width=None, **kwargs):
    """
    Generates a logo of Magnopy.

    Returns the logo and some information about the package.

    Parameters
    ----------
    date_time : bool, default False
        Whether to include the date and time to the info or not.

    comment_char : str or bool, optional

        .. versionchanged:: 0.6.0: Renamed from ``comment``

        Whether to use some character at the beginning of each string. If ``bool`` and
        ``True``, then "# " is used. If ``str``, then this string is used. If ``None``,
        then no character is used.

    logo_width : int, optional
        Including ``comment_char``. The logo will be centered in the string of this width.
        By default it is the maximum between the width of the logo and the width of lines
        in the ``info``.

    **kwargs
        For backwards compatibility.

    Returns
    -------

    logo_string : str
        Logo and information about the package. Use ``print(logo())`` to display it.

    """

    # Backwards compatibility
    if "comment" in kwargs and comment_char is None:
        warnings.warn(
            "The 'comment' option has been renamed to 'comment_char' in magnopy.logo() in version 0.6.0. Please use 'comment_char' instead of 'comment' in your code.",
            UserWarning,
            stacklevel=2,
        )
        comment_char = kwargs["comment"]
    if "flat" in kwargs:
        warnings.warn(
            "The 'flat' option has been removed from magnopy.logo() in version 0.6.0. There is only one variation of the logo now. Please remove the 'flat' option from your code.",
            UserWarning,
            stacklevel=2,
        )
    if "line_length" in kwargs:
        warnings.warn(
            "The 'line_length' option has been removed from magnopy.logo() in version 0.6.0. Use `logo_width` instead.",
            UserWarning,
            stacklevel=2,
        )
        if logo_width is None:
            logo_width = kwargs["line_length"]
    if "info" in kwargs:
        warnings.warn(
            "The 'info' option has been removed from magnopy.logo() in version 0.6.0. The info is always included now. Please remove the 'info' option from your code.",
            UserWarning,
            stacklevel=2,
        )

    if date_time:
        cd = datetime.now()
        info = [
            "",
            f"Time: {cd.hour:0>2}:{cd.minute:0>2}:{cd.second:0>2}",
            f"Date: {cd.day} {month_name[cd.month]} {cd.year}",
        ]
    else:
        info = []

    info += [
        "",
        f"Version: {__version__}",
        f"Release date: {__release_date__}",
        "",
        "License: GNU GPLv3",
        f"Documentation: {__doclink__}",
        "Copyright (C) 2023 Magnopy Team",
        "",
    ]

    # Prepare block of text
    lines_logo = _convert(BINARY_LOGO)

    if len(info) != 0:
        lines_logo += [f" ##{_:^{len(BINARY_LOGO[0]) - 7}}##" for _ in info]
        lines_logo.append(" " + "#" * (len(BINARY_LOGO[0]) - 3))

    # Add comment character
    if isinstance(comment_char, bool):
        if comment_char:
            comment_char = "# "
        else:
            comment_char = None
    if comment_char is not None:
        lines_logo = [f"{comment_char}{_}" for _ in lines_logo]

    # Center the logo within the specified width
    if logo_width is not None and logo_width > len(lines_logo[0]):
        left_spaces = " " * ((logo_width - len(lines_logo[0])) // 2)

        lines_logo = [f"{left_spaces}{_}" for _ in lines_logo]

    # Strip end spaces from each line
    lines_logo = [_.rstrip() for _ in lines_logo]

    return "\n".join(lines_logo)


def _warranty():
    r"""
    Outputs short warranty summary for terminal interactions
    """

    return """THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION."""


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir


if __name__ == "__main__":
    print(len(BINARY_LOGO[0]))
    print(logo(), end="\n\n")
    print(logo(logo_width=80), end="\n\n")
    print(logo(date_time=True), end="\n\n")
    print(logo(comment_char=True), end="\n\n")

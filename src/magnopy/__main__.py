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

import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from magnopy import __version__, __release_date__, __path__
from magnopy._package_info import _warranty, logo
from magnopy._tests import test


def main():
    parser = ArgumentParser(
        description=logo(logo_width=80) + "\n\nAvailable scripts are:\n\n"
        "* magnopy-optimize-sd\n\n"
        "* magnopy-lswt\n\n"
        "To call for help for each script type <script name> --help\n"
        "Information below is relevant only to 'magnopy' command.",
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "commands",
        default=None,
        help="command/commands on what to do. Use to display information about Magnopy. Choose from 'logo', 'warranty', 'test'",
        metavar="command",
        nargs="*",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="print version of Magnopy",
    )

    args = parser.parse_args()

    if args.version:
        print(f"Magnopy version : {__version__}")
        print(f"Release date    : {__release_date__}")
        try:
            print(f"Library path    : {os.path.abspath(__path__[0])}")
        except Exception as _:
            pass
        return

    if len(args.commands) == 0:
        parser.print_help()
        return

    for command in args.commands:
        if command == "logo":
            print(logo(logo_width=80))
        elif command == "warranty":
            print("\n" + _warranty() + "\n")
        elif command == "test":
            test()
        else:
            raise ValueError(f'Sub-command "{command}" is not recognized.')


if __name__ == "__main__":
    main()

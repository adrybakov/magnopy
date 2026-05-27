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
def test():
    r"""
    Runs unit tests for the whole Magnopy package.

    .. versionadded:: <dev-version-placeholder> Test suite is made part of the installable package.

    Notes
    -----

    Tests depend on two external packages: |pytest|_ and |hypothesis|_. These are not
    dependencies of Magnopy, so you need to install them separately to run tests. You can
    do so with pip (you may need to use ``pip3`` instead of ``pip`` depending on your
    Python setup):

    .. code-block:: bash

        pip install pytest hypothesis

    """

    # Check that pytest is installed
    try:
        import pytest
    except ImportError:
        print(
            "Require package 'pytest' to run tests. Install it with 'pip install pytest'."
        )
        return

    # Check that hypothesis is installed
    # Note: Use importlib.util.find_spec() to avoid rewrite warnings of pytest later on
    import importlib.util

    hypothesis_spec = importlib.util.find_spec("hypothesis")
    if not hypothesis_spec:
        print(
            "Require package 'hypothesis' to run tests. Install it with 'pip install hypothesis'."
        )
        return

    from numpy import __version__ as numpy_version
    from wulfric import __version__ as wulfric_version
    from magnopy import __version__ as magnopy_version

    print("Running tests...")
    print(
        "\n\n"
        + "\n".join(
            [
                f"magnopy version : {magnopy_version}",
                f"wulfric version : {wulfric_version}",
                f"numpy version   : {numpy_version}",
            ]
        )
        + "\n\n"
    )

    pytest.main(["--pyargs", "magnopy", "-s"])

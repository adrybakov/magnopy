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


import os
from argparse import ArgumentParser
from math import atan, pi

import matplotlib.pyplot as plt
import numpy as np


def arrow_with_text(
    ax, x, y, u, v, text=None, n_shift=2.1, quiver_kwargs=None, text_kwargs=None
):
    u, v = u - x, v - y
    if quiver_kwargs is None:
        quiver_kwargs = {}
    if text_kwargs is None:
        text_kwargs = {}

    center = np.array((x + u / 2, y + v / 2), dtype=float)

    if u != 0:
        normal = (-v / u, 1)
        angle = atan(v / u) / pi * 180
    else:
        normal = (1, -u / v)
        if v > 0:
            angle = 90
        else:
            angle = 270

    normal = np.array(normal, dtype=float)
    normal /= np.linalg.norm(normal)

    ax.quiver(x, y, u, v, **quiver_kwargs, zorder=6)

    if text is not None:
        ax.text(
            *(center + n_shift * normal),
            text,
            **text_kwargs,
            rotation=angle,
            rotation_mode="anchor",
            zorder=5,
        )


def main(root_directory):
    _, ax = plt.subplots(figsize=(5, 5))
    bbox = dict(
        boxstyle="round",
        ec=(35 / 255, 106 / 255, 211 / 255, 1),
        fc=(35 / 255, 106 / 255, 211 / 255, 0.5),
    )
    text_style = dict(bbox=bbox, size=15, va="center", ha="center")
    arrow_style = dict(
        angles="xy",
        scale_units="xy",
        scale=1,
        headlength=3,
        headaxislength=2.7,
        color=(35 / 255, 106 / 255, 211 / 255, 0.3),
    )

    ax.text(8, 40, "Cell", **text_style)
    ax.text(20, 40, "Atoms", **text_style)
    ax.text(37, 40, "Convention", **text_style)

    ax.text(15, 28, "SpinHamiltonian", **text_style)

    ax.text(37, 22, "spin_directions", **text_style)

    ax.text(12, 10, "Energy", **text_style)
    ax.text(32, 10, "LSWT", **text_style)

    arrow_with_text(
        ax,
        8,
        37,
        13,
        31,
        n_shift=-2.1,
        quiver_kwargs=arrow_style,
    )
    arrow_with_text(
        ax,
        20,
        37,
        15.5,
        31,
        n_shift=-2.1,
        quiver_kwargs=arrow_style,
    )
    arrow_with_text(
        ax,
        37,
        37,
        19,
        31,
        n_shift=-2.1,
        quiver_kwargs=arrow_style,
    )

    arrow_with_text(
        ax,
        14,
        25,
        12,
        13,
        n_shift=-2.1,
        quiver_kwargs=arrow_style,
    )
    arrow_with_text(
        ax,
        16,
        25,
        31,
        13,
        n_shift=-2.1,
        quiver_kwargs=arrow_style,
    )

    arrow_with_text(
        ax,
        37,
        19,
        33,
        13,
        n_shift=-2.1,
        quiver_kwargs=arrow_style,
    )

    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)

    ax.hlines([1, 49], 1, 49, color="black", lw=1)
    ax.vlines([1, 49], 1, 49, color="black", lw=1)

    ax.axis("off")
    filename = os.path.join(
        root_directory,
        "docs",
        "images",
        "data-structure.png",
    )
    plt.savefig(filename, dpi=600, bbox_inches="tight")
    print(f"File is saved in {os.path.abspath(filename)}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-rd",
        "--root_directory",
        type=str,
        help="Root directory of magnopy",
        required=True,
    )

    main(**vars(parser.parse_args()))

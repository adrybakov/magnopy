# ================================== LICENSE ===================================
# Magnopy - Python package for magnons.
# Copyright (C) 2023-2026 Magnopy Team
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

import matplotlib.pyplot as plt

# One column of A4
WIDTH = 0.36 * 8.27

# Style parameters
COLOR_BORDER = "#265DC3"
COLOR_FILL = "#E9EEF7"
FONTSIZE = 8


# Display the cat of magnopy's logo
def plot_logo(ax, x0, y0, size):
    sx = size
    sy = size / 3 * 4

    style = dict(color="white", lw=0, zorder=1)
    ax.fill_between(
        [x0 - 9.5 * sx, x0 - 5.5 * sx],
        [y0 + 8.5 * sy, y0 + 8.5 * sy],
        [y0 + 11.5 * sy, y0 + 11.5 * sy],
        **style,
    )

    style["color"] = COLOR_BORDER
    ax.fill_between(
        [
            x0 - 10 * sx,
            x0 - 9 * sx,
            x0 - 9 * sx,
            x0 - 8 * sx,
            x0 - 8 * sx,
            x0 - 7 * sx,
            x0 - 7 * sx,
            x0 - 6 * sx,
            x0 - 6 * sx,
            x0 - 5 * sx,
            x0 - 5 * sx,
            x0 - sx,
            x0 - sx,
            x0,
        ],
        [
            y0 + 8 * sy,
            y0 + 8 * sy,
            y0,
            y0,
            y0,
            y0,
            y0,
            y0,
            y0,
            y0,
            y0,
            y0,
            y0 + sy,
            y0 + sy,
        ],
        [
            y0 + 13 * sy,
            y0 + 13 * sy,
            y0 + 9 * sy,
            y0 + 9 * sy,
            y0 + 11 * sy,
            y0 + 11 * sy,
            y0 + 9 * sy,
            y0 + 9 * sy,
            y0 + 6 * sy,
            y0 + 6 * sy,
            y0 + sy,
            y0 + sy,
            y0 + 6 * sy,
            y0 + 6 * sy,
        ],
        **style,
    )

    ax.fill_between(
        [x0 - 9 * sx, x0 - 6 * sx, x0 - 6 * sx, x0 - 5 * sx],
        [y0 + 11 * sy, y0 + 11 * sy, y0 + 8 * sy, y0 + 8 * sy],
        [y0 + 12 * sy, y0 + 12 * sy, y0 + 13 * sy, y0 + 13 * sy],
        **style,
    )

    ax.fill_between(
        [x0 - 4 * sx, x0 - 3 * sx, x0 - 3 * sx, x0 - sx],
        [y0 + 4 * sy, y0 + 4 * sy, y0 + 6 * sy, y0 + 6 * sy],
        [y0 + 6 * sy, y0 + 6 * sy, y0 + 7 * sy, y0 + 7 * sy],
        **style,
    )


def main():
    ##################
    # Prepare canvas #
    ##################
    fig = plt.figure(figsize=(WIDTH, 0.75 * WIDTH))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ####################
    # Draw a rectangle #
    ####################
    # Fill
    ax.fill_between([10, 90], [15, 15], [85, 85], color=COLOR_FILL, zorder=0, lw=0)
    # Border
    border = dict(color=COLOR_BORDER, lw=3, solid_capstyle="butt", zorder=1)
    ax.plot([47, 10, 10, 47], [85, 85, 15, 15], **border)
    ax.plot([53, 90, 90, 53], [15, 15, 85, 85], **border)

    #################
    # Draw the logo #
    #################
    plot_logo(ax, 88, 17, 0.7)

    #################
    # Define styles #
    #################
    # Style of text
    text_out = dict(
        fontsize=FONTSIZE, color="black", ha="center", va="center", zorder=1
    )
    text_in = dict(
        color=COLOR_BORDER, va="center", ha="center", fontsize=FONTSIZE, zorder=1
    )
    text_in_small = dict(
        color=COLOR_BORDER, va="center", fontsize=0.75 * FONTSIZE, zorder=1
    )

    # Style of the arrows
    def arrow(x0, y0, x1, y1, color):
        ax.quiver(
            x0,
            y0,
            x1 - x0,
            y1 - y0,
            angles="xy",
            scale_units="xy",
            width=0.006,
            scale=1,
            headlength=3,
            headaxislength=2.7,
            color=color,
            zorder=1,
        )

    # Style of the lines
    def line(x0, y0, x1, y1):
        ax.plot([x0, x1], [y0, y1], color=COLOR_BORDER, lw=1, zorder=1)

    ########################
    # Text outside the box #
    ########################
    ax.text(50, 92.5, R"input (configuration & system parameters)", **text_out)
    ax.text(50, 7.5, R"output (visual & numerical)", **text_out)

    #######################
    # Text inside the box #
    #######################
    # Spin Hamiltonian
    ax.text(46, 72.5, "Spin Hamiltonian", **text_in)
    ax.text(70, 80, "unit cell", **text_in_small, ha="left")
    ax.text(70, 75, "site positions", **text_in_small, ha="left")
    ax.text(70, 70, "parameters", **text_in_small, ha="left")
    ax.text(70, 65, "convention", **text_in_small, ha="left")
    # Vacuum state
    ax.text(46, 56, "Vacuum state", **text_in)
    ax.text(70, 56, R"$\boldsymbol{z}_{\alpha}$", **text_in_small, ha="left")
    # LSWT
    ax.text(35, 41, "LSWT", **text_in)
    ax.text(25, 44, R"$E^{(2)}$", **text_in_small, ha="right")
    ax.text(25, 38, R"$\omega_{\beta}(\boldsymbol{k})$", **text_in_small, ha="right")
    # Energy
    ax.text(65, 41, "Energy", **text_in)
    ax.text(76, 44, R"$E^{(0)}$", **text_in_small, ha="left")
    ax.text(76, 38, R"$E^{corr}$", **text_in_small, ha="left")
    # Post-processing
    ax.text(50, 25, "Post-processing", **text_in)

    #################
    # Content lines #
    #################
    # Spin Hamiltonian
    line(63, 72.5, 69, 80)
    line(63, 72.5, 69, 75)
    line(63, 72.5, 69, 70)
    line(63, 72.5, 69, 65)
    # Vacuum state
    line(60, 56, 69, 56)
    # LSWT
    line(29, 41, 26, 44)
    line(29, 41, 26, 38)
    # Energy
    line(72, 41, 75, 44)
    line(72, 41, 75, 38)

    ##########
    # Arrows #
    ##########
    # In
    arrow(50, 89, 50, 81, "black")
    # Spin Hamiltonian -> Vacuum state
    arrow(50, 68.25, 50, 60.25, COLOR_BORDER)
    # Vacuum state -> LSWT
    arrow(46, 52.5, 35, 44.5, COLOR_BORDER)
    # Vacuum state -> Energy
    arrow(54, 52.5, 65, 44.5, COLOR_BORDER)
    # LSWT -> Post-processing
    arrow(35, 37, 46, 29, COLOR_BORDER)
    # Energy -> Post-processing
    arrow(65, 37, 54, 29, COLOR_BORDER)
    # Out
    arrow(50, 19, 50, 11, "black")

    ###############
    # Save figure #
    ###############
    plt.savefig("figure-3.eps", dpi=600)
    plt.savefig("figure-3.png", dpi=600)
    plt.close()


if __name__ == "__main__":
    main()

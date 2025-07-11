usage: magnopy-lswt [-h] -sf filename -ss name [-sd [S1_x S2_y S3_z ... ...]]
                    [-sv [S1 S2 S3 ... ...]] [-kp G-X-S|G-Y] [-kps KPOINTS]
                    [-r] [-mf MAGNETIC_FIELD MAGNETIC_FIELD MAGNETIC_FIELD]
                    [-of OUTPUT_FOLDER] [-np NUMBER_PROCESSORS]
                    [-msdi xa_1 xa_2 xa_3 xa_1 xa_2 xa_3 xa_1 xa_2 xa_3]
                    [-hpd]

███╗   ███╗  █████╗   ██████╗  ███╗   ██╗  ██████╗  ██████╗  ██╗   ██╗
████╗ ████║ ██╔══██╗ ██╔════╝  ████╗  ██║ ██╔═══██╗ ██╔══██╗ ╚██╗ ██╔╝
██╔████╔██║ ███████║ ██║  ███╗ ██╔██╗ ██║ ██║   ██║ ██████╔╝  ╚████╔╝
██║╚██╔╝██║ ██╔══██║ ██║  ╚██║ ██║╚██╗██║ ██║   ██║ ██╔═══╝    ╚██╔╝
██║ ╚═╝ ██║ ██║  ██║ ╚██████╔╝ ██║ ╚████║ ╚██████╔╝ ██║         ██║
╚═╝     ╚═╝ ╚═╝  ╚═╝  ╚═════╝  ╚═╝  ╚═══╝  ╚═════╝  ╚═╝         ╚═╝
                                                           ▄   ▄
                     Version: 0.1.10                       █▀█▀█
                Documentation: magnopy.org                 █▄█▄█
                 Release date: undefined                    ███   ▄▄
                    License: GNU GPLv3                      ████ █  █
          Copyright (C) 2023-2025  Magnopy Team             ████    █
                                                            ▀▀▀▀▀▀▀▀

This script solves the spin Hamiltonian at the level of Linear Spin Wave Theory (LSWT) and outputs (almost) every possible quantity.

options:
  -h, --help            show this help message and exit
  -sf, --spinham-filename filename
                        Path to the spin Hamiltonian file, from where the
                        parameters would be read.
  -ss, --spinham-source name
                        Source of the spin Hamiltonian. Either "GROGU" or
                        "TB2J"
  -sd, --spin-directions [S1_x S2_y S3_z ... ...]
                        To fully define the system for the calculations of
                        magnons one need the information about the ground
                        state in addition to the parameters of the
                        Hamiltonian. There are two ways to give this
                        information to magnopy: * Give a path to the file. In
                        the file there should be M lines with three numbers in
                        each. The order of the lines would match the order of
                        magnetic atoms in the spin Hamiltonian. * Give a
                        sequence of 3*M numbers directly to this parameter. If
                        none provided, then magnopy attempts to optimize the
                        spin directions prior to the LSWT calculations.
  -sv, --spin-values [S1 S2 S3 ... ...]
                        In the case when the parameters of spin Hamiltonian
                        comes from TB2J, one might want to change the values
                        of spins to be closer to half-integers. This option
                        allows that. Order of the M numbers should match the
                        order of magnetic atoms in the spin Hamiltonian. Note
                        that those numbers are always positive. To specify AFM
                        order use opposite spin directions and not spin values
                        of the opposite sign.
  -kp, --k-path G-X-S|G-Y
                        Path of high symmetry k-points for the plots of
                        dispersion and other quantities.
  -kps, --kpoints KPOINTS
                        Alternatively one could provide an explicit list of
                        k-points for calculation. In that case provide a path
                        to the file, in which each k-point is given in a
                        separate line with three numbers per line.
  -r, --relative        When an explicit list of k-points is given, this
                        option specify whether to consider them as relative or
                        absolute coordinates. Absolute by default.
  -mf, --magnetic-field MAGNETIC_FIELD MAGNETIC_FIELD MAGNETIC_FIELD
                        Vector of external magnetic field, given in the units
                        of Tesla.
  -of, --output-folder OUTPUT_FOLDER
                        Folder where all output files of magnopy wil be saved.
  -np, --number-processors NUMBER_PROCESSORS
                        Number of processes for multithreading. Uses all
                        available processors by default. Pass 1 to run in
                        serial.
  -msdi, --make-sd-image xa_1 xa_2 xa_3 xa_1 xa_2 xa_3 xa_1 xa_2 xa_3
                        Plots optimized spin directions and saves it in .html
                        file, that can be viewed within any modern browser.
                        Expects three integers as an input - the supercell
                        that will be plotted. Pass 1 1 1 to plot only the unit
                        cell.
  -hpd, --hide-personal-data
                        Whether to strip the parts of the paths as to hide the
                        file structure of you personal computer.

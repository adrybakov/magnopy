usage: magnopy-lswt [-h] -ss {GROGU,TB2J,tb2j,grogu} -sf FILENAME
                    [-sd [FILENAME ...]] [-mf B_X B_Y B_Z] [-of OUTPUT_FOLDER]
                    [-kp GAMMA-X-S|GAMMA-Y] [-kps KPOINTS] [-r]
                    [-spg-s NUMBER] [-np NUMBER_PROCESSORS] [-sv [S1 ...]]
                    [-no-html] [-hpd] [-spg-t [TYPE1 [TYPE2 ...]]]
                    [-msdi MAKE_SD_IMAGE MAKE_SD_IMAGE MAKE_SD_IMAGE]

███╗   ███╗  █████╗   ██████╗  ███╗   ██╗  ██████╗  ██████╗  ██╗   ██╗
████╗ ████║ ██╔══██╗ ██╔════╝  ████╗  ██║ ██╔═══██╗ ██╔══██╗ ╚██╗ ██╔╝
██╔████╔██║ ███████║ ██║  ███╗ ██╔██╗ ██║ ██║   ██║ ██████╔╝  ╚████╔╝
██║╚██╔╝██║ ██╔══██║ ██║  ╚██║ ██║╚██╗██║ ██║   ██║ ██╔═══╝    ╚██╔╝
██║ ╚═╝ ██║ ██║  ██║ ╚██████╔╝ ██║ ╚████║ ╚██████╔╝ ██║         ██║
╚═╝     ╚═╝ ╚═╝  ╚═╝  ╚═════╝  ╚═╝  ╚═══╝  ╚═════╝  ╚═╝         ╚═╝
                                                           ▄   ▄
                      Version: 0.4.0                       █▀█▀█
                Documentation: magnopy.org                 █▄█▄█
              Release date: 23 October 2025                 ███   ▄▄
                    License: GNU GPLv3                      ████ █  █
          Copyright (C) 2023-2025  Magnopy Team             ████    █
                                                            ▀▀▀▀▀▀▀▀

This script solves the spin Hamiltonian at the level of Linear Spin Wave Theory (LSWT) and outputs (almost) every possible quantity.

options:
  -h, --help            show this help message and exit
  -ss, --spinham-source {GROGU,TB2J,tb2j,grogu}
                        Magnopy supports two sources of spin Hamiltonian:
                        GROGU or TB2J. Source of the spin Hamiltonian can not
                        be deduced reliably from the Hamiltonian file. Thus,
                        magnopy asks you to specify what was the source of the
                        file that you pass to "--spinham-filename".
  -sf, --spinham-filename FILENAME
                        Path to the file with the parameters of spin
                        Hamiltonian. If you use "--spinham-source TB2J", then
                        this is an "exchange.out" file, produced by TB2J. If
                        you use "--spinham-source GROGU", then this is a .txt
                        file with the Hamiltonian parameters produced by
                        GROGU.
  -sd, --spin-directions [FILENAME ...]
                        Set of spin directions for every magnetic site in the
                        unit cell defines the ground state of the Hamiltonian.
                        Magnopy can try to identify the ground state on the
                        fly via energy minimization (see also magnopy-
                        optimize-sd). However, we recommend to provide the set
                        of spin directions explicitly. This argument expects a
                        filename for the file that contains three numbers per
                        line and has M lines in total. M is the amount of
                        magnetic sites. Alternatively, you can give a set of
                        3*M numbers directly to this argument. Then, first
                        three numbers define spin direction of the first
                        magnetic site, next three numbers - of the second and
                        so on. Magnetic sites are defined as atoms that have
                        at least one parameter associated with them.
  -mf, --magnetic-field B_X B_Y B_Z
                        Vector of the external magnetic field (magnetic flux
                        density, B), given in the units of Tesla.
  -of, --output-folder OUTPUT_FOLDER
                        Path to the folder where all output files of magnopy
                        wil be saved. Defaults to "magnopy-results". If the
                        folder does not exist, then magnopy will try to create
                        it.
  -kp, --k-path GAMMA-X-S|GAMMA-Y
                        Path in reciprocal space between high symmetry points.
                        Used for the plots of magnon dispersion and other
                        quantities. Ignored if "--kpoints FILENAME" is used.
                        List of available high symmetry points is calculated
                        automatically by wulfric package using convention of
                        HPKOT paper based on the space group of the crystal
                        structure (see wulfric.org for more details).
                        Numerical tolerance for the space group search via
                        spglib package can be controlled with "--spglib-
                        symprec NUMBER" argument. Note: high symmetry points
                        are defined by wulfric based on the reciprocal lattice
                        of the primitive cell, but their relative coordinates
                        are given in the basis of reciprocal cell of the input
                        cell (i. e. the same unit cell as in the TB2J or GROGU
                        file). Primitive cell might be different from the
                        input cell. If you want to control what atoms are
                        considered to be equivalent in the space group search
                        - manually change their names in the input file. To
                        learn how a name is translated into the spglib_type
                        see documentation of the wulfric package
                        (wulfric.org).
  -kps, --kpoints KPOINTS
                        Explicit list of k-points in reciprocal space. A
                        filename is expected. The file shall contain three
                        numbers per line. Each line specifies one k-point. By
                        default three numbers are understood as absolute
                        coordinates in reciprocal space. If "--relative" is
                        used, than three numbers are understood as relative
                        coordinates in the basis of the reciprocal cell of the
                        input unit cell (i. e. of the same unit cell as in the
                        TB2J or GROGU file, not of the primitive cell).
  -r, --relative        Relevant only if "--kpoints FILENAME" is used. See
                        description of "--kpoints".
  -spg-s, --spglib-symprec NUMBER
                        Tolerance parameter for the space group symmetry
                        search by spglib.
  -np, --number-processors NUMBER_PROCESSORS
                        Magnopy is parallelized over the k-points. By default
                        it uses all available processors. Pass 1 to run in
                        serial.
  -sv, --spin-values [S1 ...]
                        Only works with "--spinham-source TB2J". This option
                        changes spin values of the magnetic atoms. It expects
                        M numbers in the same order as the order of magnetic
                        atoms in the input TB2J file. Magnetic atoms are
                        defined as the atoms that have at least one
                        interaction associated with them. Spin values are
                        always positive. If you want to specify spin-down
                        state or AFM order use spin directions and not the
                        spin values.
  -no-html, --no-html   .html files are generally heavy (~ 5 Mb). This option
                        allows to disable their generation to save disk space.
  -hpd, --hide-personal-data
                        Whether not to use os.path.abspath. Hides the file
                        structure of your personal computer. Note, that the
                        relative paths can still expose the structure of you
                        filesystem.
  -spg-t, --spglib-types [TYPE1 [TYPE2 ...]]
                        Set of spglib types for the space group search by
                        spglib. Expects N non-zero integers in total. N is the
                        amount of all sites/atoms in the input files (notjust
                        magnetic, but all). If not given, then guesses
                        automatically by wulfric (see
                        wulfric.get_spglib_types() at wulfric.org types for
                        more details).
  -msdi, --make-sd-image MAKE_SD_IMAGE MAKE_SD_IMAGE MAKE_SD_IMAGE
                        DEPRECATED in v0.2.0. Interactive .html images are
                        generated by default, use "--no-html" to suppress.
                        This arguments will be removed from magnopy in March
                        of 2026

.. _user-guide_cli_magnopy-lswt:

************
magnopy-lswt
************

This scenario runs a calculation for the given spin Hamiltonian at the level of the
linear spin wave theory and outputs majority of the results that magnopy can compute.

Please visit |tutorial-lswt|_ for examples of input and output files of this
script. This page explains how to get a full reference of script's arguments and
describe some of them in details.

.. _user-guide_cli_lswt_help:

Getting help
============

The most accurate and full list of parameters for every script, that correspond to the
actually installed version of magnopy, you can execute

.. code-block::

    magnopy-lswt -h

or

.. code-block::

    magnopy-lswt --help

This command outputs to the standard output channel (terminal) magnopy's metadata and
*full* list of script's arguments. Here is an example of this output

.. hint::

    Go :ref:`here <user-guide_cli_common-notes_read-help>` to learn how to read this help message.

.. literalinclude:: help.inc
    :language: text


Output files
============

The script outputs human-readable text to the console with the progress of calculations
and compact output data. This output is meant to explain itself, thus we do not document
it here.

In addition, it prepares a number of .txt and/or .html files described below.

For examples of the output text and files you can visit |tutorial-lswt|_.

SPIN_VECTORS.txt
----------------

A file with the spin vectors that were used as the ground state.

There are M lines in the file. M is a number of magnetic atoms in the spin Hamiltonian.
Each line has four numbers on it, separated by at least one space symbol. First number is
an x component, second - y, third - z of the spin direction vector. Fourth number is the
spin value.

SPIN_DIRECTIONS.html
--------------------

**Requires** : Installation of |plotly|_ or ``magnopy[visual]``).

**Options** : Use ``--no-html`` to disable an output of this file.

An interactive .html file with the 3D image of the spin directions that were used as the
ground sate.


HIGH-SYMMETRY_POINTS.txt
------------------------

**Options** : Not produced if ``--kpoints`` is used.

There are :math:`N + 1` lines in the file. First line is the header for the data, that
indicate the meaning of each column. Then, there are :math:`N` lines for :math:`N`
high-symmetry points.

Each line has one string followed by six numbers, separated by at least one space symbol.

The string is a label of the high-symmetry point that can be used in the specification of
the k-path.

First three numbers are the *absolute* coordinates of the high-symmetry point in the
reciprocal space.

Last three numbers are the relative coordinates of the high-symmetry point in the basis of
the reciprocal cell of the given  unit cell (i. e. same unit cell as in the input file).

K-POINTS.html
-------------

**Requires** : Installation of |plotly|_ and |scipy|_ or ``magnopy[visual]``.

**Options** : Not produced if ``--kpoints`` is used.

An interactive .html file with the 3D image of the chose k-path, high-symmetry points and
first Brillouin zones of the given unit cell (i. e. same unit cell as in the input file)
and of the primitive cell.

K-POINTS.txt
------------

A file with the full list of the k-points that were used in the calculations.

There are :math:`L + 1` line in the file. First line is the header of the data, that
indicate the meaning of each column. Then, there are :math:`L` lines with :math:`L`
k-points.

Each line has seven numbers.

First three numbers are the *absolute* coordinates of the high-symmetry point in the
reciprocal space.

Next three numbers are the relative coordinates of the high-symmetry point in the basis of
the reciprocal cell of the given  unit cell (i. e. same unit cell as in the input file).

Last number is a single index for the k-point, that can be used for the plots (for example
band plots).

OMEGAS.txt
----------

A file with the values of magnon energies.

There are :math:`L + 1` line in the file. First line is the header of the data, that
indicate the meaning of each column. Then, there are :math:`L` lines with values of
magnon energies for each of :math:`L` k-points.

Each line has :math:`M` numbers. Each number is a magnon energy of :math:`i`-th magnon
mode.

OMEGAS.png
----------

**Requires** : Installation of |matplotlib|_ or ``magnopy[visual]``.

Static image with the magnon dispersion.

Data can be found in "OMEGA.txt" and "K-POINTS.txt"

OMEGAS-IMAG.txt
---------------

**Warning** If this file appeared, than something might be wrong with the set-up of the
calculations (wrong ground state, ...)

A file with the imaginary part of the values of magnon energies.

There are :math:`L + 1` line in the file. First line is the header of the data, that
indicate the meaning of each column. Then, there are :math:`L` lines with imaginary part
of the values of magnon energies for each of :math:`L` k-points.

Each line has :math:`M` numbers. Each number is an imaginary part of the magnon energy of
:math:`i`-th magnon mode.

OMEGAS-IMAG.png
---------------

**Warning** If this file appeared, than something might be wrong with the set-up of the
calculations (wrong ground state, ...)

**Requires** : Installation of |matplotlib|_ or ``magnopy[visual]``.

Static image with the imaginary part of the magnon dispersion.

Data can be found in "OMEGA-IMAG.txt" and "K-POINTS.txt"

DELTAS.txt
----------

A file with the values of the delta term of the magnon Hamiltonian.

There are :math:`L + 1` line in the file. First line is the header of the data, that
indicate the meaning of each column. Then, there are :math:`L` lines with values of
magnon energies for each of :math:`L` k-points.

Each line has number number. The number is a delta term of the magnon Hamiltonian.

DELTAS.png
----------

**Requires** : Installation of |matplotlib|_ or ``magnopy[visual]``.

Static image with the delta term of the magnon Hamiltonian.

Data can be found in "DELTAS.txt" and "K-POINTS.txt"






INITIAL_GUESS.TXT
-----------------

A file with the spin directions of the initial guess. Magnopy makes a new random guess
for the spin directions prior to each optimization (in other words, for each execution of
the script).

There are M lines in the file. M is a number of magnetic atoms in the spin Hamiltonian.
Each line has three numbers on it, separated by at least one space symbol. First number is
an x component, second - y, third - z of the spin direction vector.

SPIN_DIRECTIONS.txt
-------------------

A file with the optimized spin directions.

There are M lines in the file. M is a number of magnetic atoms in the spin Hamiltonian.
Each line has three numbers on it, separated by at least one space symbol. First number is
an x component, second - y, third - z of the spin direction vector.

SPIN_POSITIONS.txt
------------------

A file with the *absolute* positions of the magnetic sites.

There are M lines in the file. M is a number of magnetic atoms in the spin Hamiltonian.
Each line has three numbers on it, separated by at least one space symbol. First number is
an x coordinate, second - y, third - z.

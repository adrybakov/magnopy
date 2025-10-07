.. _user-guide_cli_magnopy-lswt:

************
magnopy-lswt
************

This scenario runs a calculation for the given spin Hamiltonian at the level of the
linear spin wave theory and outputs majority of the results that magnopy can compute.

Visit |tutorial-lswt|_ for examples of input and output files.

.. _user-guide_cli_lswt_help:

Getting help
============

We recommend to get the accurate and full list of script's parameters, that reflects
installed version of magnopy with the command

.. code-block::

    magnopy-lswt --help

which outputs to the standard output channel (console or terminal) magnopy's metadata and
*full* list of script's arguments. Here is an example of this output

.. hint::

    Go :ref:`here <user-guide_cli_common-notes_read-help>` to learn how to read this help
    message.

.. literalinclude:: help.inc
    :language: text


Output files
============

Human-readable text with the progress of calculations and compact output data is printed
directly to the console. This output is meant to explain itself, thus we do not document
it here.

In addition, a number of .txt and/or .html files is produced.

Visit |tutorial-lswt|_ for examples of the output text and files.

DELTAS.png
----------

**Requires** : Installation of |matplotlib|_ or ``magnopy[visual]``.

Static image with the delta term of the magnon Hamiltonian.

Data can be found in "DELTAS.txt" and "K-POINTS.txt".

DELTAS.txt
----------

A file with the values of the delta term of the magnon Hamiltonian.

There are :math:`L + 1` lines in the file. First line is a header, that indicates the
meaning of each column. Then, there are :math:`L` lines with values of magnon energies for
each of :math:`L` k-points.

Each line has one number on it. The number is a delta term of the magnon Hamiltonian.


HIGH-SYMMETRY_POINTS.txt
------------------------

.. versionadded:: 0.2.0

**Options** : Not produced if ``--kpoints`` is used.

There are :math:`N + 1` lines in the file. First line is a header, that indicates the
meaning of each column. Then, there are :math:`N` lines for :math:`N` high-symmetry
points.

Each line has one string followed by six numbers on it, separated by at least one space
symbol.

The string is a label of the high-symmetry point that can be used in the specification of
the k-path.

First three numbers are the *absolute* coordinates of the high-symmetry point in the
reciprocal space.

Last three numbers are the relative coordinates of the high-symmetry point in the basis of
the reciprocal cell of the given  unit cell (i. e. same unit cell as in the input file).

K-POINTS.html
-------------

.. versionadded:: 0.2.0

**Requires** : Installation of |plotly|_ and |scipy|_ or ``magnopy[visual]``.

**Options** : Not produced if ``--kpoints`` is used. Use ``--no-html`` to disable an
output of this file.

An interactive .html file with 3D image of the chose k-path, high-symmetry points and
first Brillouin zones of the given unit cell (i. e. same unit cell as in the input file)
and of the primitive cell.

Part of the data can be found in "HIGH-SYMMETRY_POINTS.txt".

K-POINTS.txt
------------

.. versionadded:: 0.2.0

A file with the full list of the k-points that were used in the calculations.

There are :math:`L + 1` lines in the file. First line is a header, that indicates the
meaning of each column. Then, there are :math:`L` lines with :math:`L` k-points.

Each line has seven numbers on it, separated by at least one space symbol.

First three numbers are the *absolute* coordinates of the high-symmetry point in the
reciprocal space.

Next three numbers are the relative coordinates of the high-symmetry point in the basis of
the reciprocal cell of the given  unit cell (i. e. same unit cell as in the input file).

Last number is a single index for the k-point, that can be used for the plots (for example
band plots).

OMEGAS.png
----------

**Requires** : Installation of |matplotlib|_ or ``magnopy[visual]``.

Static image with the magnon dispersion.

Data can be found in "OMEGAS.txt" and "K-POINTS.txt".

OMEGAS.txt
----------

A file with the values of magnon energies.

There are :math:`L + 1` lines in the file. First line is a header, that indicates the
meaning of each column. Then, there are :math:`L` lines with values of magnon energies for
each of :math:`L` k-points.

Each line has :math:`M` numbers on it, separated by at least one space symbol.

Each number is a magnon energy of :math:`i`-th magnon mode.

OMEGAS-IMAG.png
---------------

**Warning** If this file appeared, then something might be wrong with the set-up of the
calculations (wrong ground state, ...)

**Requires** : Installation of |matplotlib|_ or ``magnopy[visual]``.

Static image with the imaginary part of the magnon dispersion.

Data can be found in "OMEGAS-IMAG.txt" and "K-POINTS.txt".

OMEGAS-IMAG.txt
---------------

**Warning** If this file appeared, then something might be wrong with the set-up of the
calculations (wrong ground state, ...)

A file with the imaginary part of the values of magnon energies.

There are :math:`L + 1` lines in the file. First line is a header, that indicates the
meaning of each column. Then, there are :math:`L` lines with imaginary part of the values
of magnon energies for each of :math:`L` k-points.

Each line has :math:`M` numbers on it, separated by at least one space symbol.

Each number is an imaginary part of the magnon energy of :math:`i`-th magnon mode.

SPIN_DIRECTIONS.html
--------------------

.. versionadded:: 0.2.0

**Requires** : Installation of |plotly|_ or ``magnopy[visual]``).

**Options** : Use ``--no-html`` to disable an output of this file.

An interactive .html file with 3D image of the spin directions that were used as the
ground sate.

Part of the data can be found in "SPIN_VECTORS.txt".

SPIN_VECTORS.txt
----------------

.. versionadded:: 0.2.0

A file with the spin vectors that were used as the ground state.

There are M lines in the file. M is a number of magnetic atoms in the spin Hamiltonian.

Each line has four numbers on it, separated by at least one space symbol.

First number is an x component, second - y, third - z of the spin direction vector. Fourth
number is the spin value.

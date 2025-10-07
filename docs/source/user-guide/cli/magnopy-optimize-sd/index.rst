.. _user-guide_cli_optimize-sd:

*******************
magnopy-optimize-sd
*******************

This scenario optimizes classical energy of the spin Hamiltonian and finds the spin
directions that describe a local minima of the energy landscape. It implements an
algorithm described in [1]_.

Please visit |tutorial-optimize-sd|_ for examples of input and output files of this
script. This page explains how to get a full reference of script's arguments and
describe some of them in details.

.. _user-guide_cli_optimize-sd_help:

Getting help
============

The most accurate and full list of parameters for every script, that correspond to the
actually installed version of magnopy, you can execute

.. code-block::

    magnopy-optimize-sd -h

or

.. code-block::

    magnopy-optimize-sd --help

This command outputs to the standard output channel (terminal) magnopy's metadata and
*full* list of script's arguments. Here is an example of this output

.. hint::

    Go :ref:`here <user-guide_cli_common-notes_read-help>` to learn how to read this help message.

.. literalinclude:: help.inc
    :language: text

.. _user-guide_cli_optimize-sd_output-files:


Output files
============

The script outputs human-readable text to the console with the progress of calculations
and compact output data. This output is meant to explain itself, thus we do not document
it here.

In addition, it prepares a number of .txt and/or .html files described below.

For examples of the output text and files you can visit |tutorial-optimize-sd|_.

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

SPIN_DIRECTIONS.html
--------------------

**Requires** : Installation of |plotly|_ or ``magnopy[visual]``.

**Options to disable** : ``-no-html`` or ``--no-html``.

An interactive .html file with the 3D image of both minimized spin directions and of the
initial guess in the form of vectors.

References
==========

.. [1] Ivanov, A.V., Uzdin, V.M. and Jónsson, H., 2021.
    Fast and robust algorithm for energy minimization of spin systems applied
    in an analysis of high temperature spin configurations in terms of skyrmion
    density.
    Computer Physics Communications, 260, p.107749.

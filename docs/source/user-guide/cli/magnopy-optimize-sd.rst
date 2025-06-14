.. _user-guide_cli_optimize-sd:

*******************
magnopy-optimize-sd
*******************

This scenario optimizes classical energy of the spin Hamiltonian and finds the spin
directions that describe a local minima of the energy landscape.


Arguments of the script
=======================

To get the best description of the input parameters that correspond to the magnopy
version that you have installed run the command

.. code-block::

    magnopy-optimize-sd --help

That should output something similar to

.. literalinclude:: magnopy-optimize-sd-help.inc
    :language: text

At the very beginning there is a syntax for the usage of the script, where required
arguments are given without brackets and optional arguments are written with brackets.
Then there is a logo of magnopy, followed by the list of supported arguments with their
short and long names and explanation of what they represent.

For example, for the filename with the parameters of the spin Hamiltonian one can use a
keyword argument with short name "-sf" or with its long name "--spinham-filename" like

.. code-block::

    magnopy-optimize-sd -sf spinHamiltonian.txt

Interpretation of the output
============================

The script print in the console the progress of the calculation. Use the stream redirect
to save it to a file

.. code-block:: bash

    magnopy-optimize-sd ... > output.txt

Some of the data and pictures will be saved in the folder with the name defined by the
value of ``-of, --output-folder`` argument.

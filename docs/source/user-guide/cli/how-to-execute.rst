.. _user-guide_cli_common-notes:

***********************
How to execute scripts?
***********************

On this page we explain how the command-line interface of magnopy works.

There is a number of scripts defined in magnopy, name of every single one of them starts
with ``magnopy-``. Examples on this page use ``magnopy-scenario`` as a placeholder for
the script's name.

Getting help
============

To display the help message and check what parameters are available for each script use


.. code-block:: bash

    magnopy-scenario -h

or

.. code-block:: bash

    magnopy-scenario --help

Arguments
=========

Every script expects several "arguments" (or "parameters" or "options") as an input. There
are three types of arguments.

Positional arguments
--------------------

Only the *value* of an argument is expected and script recognizes its meaning from the
position of that value.

For example, assume that a script expects two positional arguments: first for the input
filename and second for the output filename. If you execute

.. code-block:: bash

    magnopy-scenario input_file.txt output_file.txt

a script will use the file "input_file.txt" as an input filename and "output_file.txt"
as an output filename. However, if you execute

.. code-block:: bash

    magnopy-scenario output_file.txt input_file.txt

then "input_file.txt" will be used as an output filename and "output_file.txt" will be
used as an input filename.

.. important::

    Order of positional arguments matters.

Keyword arguments with value
----------------------------

Both *keyword* and the *value* of an argument are expected. The keyword is fixed and
used to indicate the meaning of the argument. The value is some data that are passed to
the script, one or more values are expected. Keyword arguments are given *after*
positional ones. Order of keyword arguments does not matter.

For example, assume that a script has an argument with the keyword "--input-file", that
expects a single value. If you execute

.. code-block:: bash

    magnopy-scenario --input-file input.txt

then "--input-file" is a keyword and "input.txt" is the value.

Next, assume that a script has an argument with the keyword "--magnetic-field" that
expects three values. If you execute

.. code-block:: bash

    magnopy-scenario --magnetic-field 0 0 1

then "--magnetic-field" is a keyword and "0", "0" and "1" are the values. In this example
the values describe components of the magnetic field vector :math:`h = (0, 0, 1)`.

.. important::

    The keywords always start with "-" or "--".


Keyword arguments without value
-------------------------------

Only the *keyword* is expected. The keyword is fixed and used both to indicate the meaning
of the argument and its value. That type of arguments is typically used for the arguments
that have two possible values:  ``True`` or ``False``. When such an argument is given to
the script it switches the default value to its opposite.

For example, assume that a script has an argument with the keyword "--relative" and
default value "False". If you execute

.. code-block:: bash

    magnopy-scenario

a script will use ``False`` as a value for the argument with the keyword ``--relative``.
However, if you execute

.. code-block:: bash

    magnopy-scenario --relative

a script will use ``True`` as a value for the argument with the keyword ``--relative``.

.. important::

    The keywords always start with "-" or "--".

Long vs short keywords
======================

Majority of arguments in magnopy's scripts have two equivalent keywords: a long one and a
short one. You are free to use either of them. The long version of the keyword starts with
``--`` and the short version of the keyword starts with a single ``-``.

The purpose of having both long and short keywords is to provide descriptive keywords
(i. e. "long" ones), but to allow experienced users an option of using the short ones.

For example, assume that a script has a set of the arguments defined

==================== ============= ==============
Long keyword         Short keyword Value
==================== ============= ==============
``--input-file``     ``-if``       One string
``--output-file``    ``-of``       One string
``--magnetic-field`` ``-mf``       Three numbers
``--relative``       ``-r``        Nothing
==================== ============= ==============

Then, two commands below are equivalent

.. code-block:: bash

    magnopy-scenario --input-file input.txt --output-file output.txt --magnetic-field 0 0 1 --relative

.. code-block:: bash

    magnopy-scenario -if input.txt -of output.txt -mf 0 0 1 -r

The first one is descriptive, but the second one is more compact.

.. hint::

    You can use long keywords for some of the arguments and short ones for the other. The
    arguments are independent.

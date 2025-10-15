.. _user-guide_usage_cell:

****
Cell
****

Cell is a set of three vectors that define periodic lattice in real space.

To store it, magnopy uses the approach that is typical for many python-based codes
(|spglib|_, |wulfric|_, ...).

``cell`` is a two-dimensional :math:`3\times3` matrix (|array-like|_), that groups
three lattice vectors. The rows of the ``cell`` are vectors, while the columns are
cartesian coordinates. Here is an example of a simple orthorhombic cell

.. doctest::

    >>> cell = [
    ...     [3.5534, 0.0000, 0.0000],
    ...     [0.0000, 4.7449, 0.0000],
    ...     [0.0000, 0.0000, 8.7605],
    ... ]

with the three lattice vectors being

.. doctest::

    >>> cell[0] # a_1
    [3.5534, 0.0000, 0.0000]
    >>> cell[1] # a_2
    [0.0000, 4.7449, 0.0000]
    >>> cell[2] # a_3
    [0.0000, 0.0000, 8.7605]

``cell`` is one of the three objects that are required for creation of the
:py:class:`.SpinHamiltonian` class. It is stored as an immutable attribute
:py:attr:`.SpinHamiltonian.cell`.

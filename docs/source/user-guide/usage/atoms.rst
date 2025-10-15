.. _user-guide_usage_atoms:

*****
Atoms
*****

``atoms`` data structure is implemented in a variety of codes (if not in each one of
them). Magnopy does not re-implement it, but rather use the same approach as in another
python package called |wulfric|_.

Here we briefly describe how atoms are stored, if you want to read the original
description of |wulfric|_ we refer you to |wulfric-key-concepts|_.

Atoms are stored as a plain python dictionary. Keys of the ``atoms`` are
properties of atoms. Values are lists of :math:`M^{\prime}` elements each,
where :math:`M^{\prime}` is an amount of atoms. Here is an example of the ``atoms``
dictionary with six atoms in it

.. doctest::

    >>> atoms = {
    ...     "names": ["Cr1", "Br1", "S1", "Cr2", "Br2", "S2"],
    ...     "species": ["Cr", "Br", "S", "Cr", "Br", "S"],
    ...     "positions": [
    ...         [0.5, 0.0, 0.882382],
    ...         [0.0, 0.0, 0.677322],
    ...         [0.5, 0.5, 0.935321],
    ...         [0.0, 0.5, 0.117618],
    ...         [0.5, 0.5, 0.322678],
    ...         [0.0, 0.0, 0.064679],
    ...     ],
    ... }
    >>> f"{len(atoms['names'])} atoms"
    '6 atoms'
    >>> for name, species, pos in zip(atoms["names"], atoms["species"], atoms["positions"]):
    ...     print(f'Atom "{name}" located at {pos} is of species "{species}"')
    Atom "Cr1" located at [0.5, 0.0, 0.882382] is of species "Cr"
    Atom "Br1" located at [0.0, 0.0, 0.677322] is of species "Br"
    Atom "S1" located at [0.5, 0.5, 0.935321] is of species "S"
    Atom "Cr2" located at [0.0, 0.5, 0.117618] is of species "Cr"
    Atom "Br2" located at [0.5, 0.5, 0.322678] is of species "Br"
    Atom "S2" located at [0.0, 0.0, 0.064679] is of species "S"

Magnopy recognizes the following keys

*   "names" :
    ``list`` of ``str``. Inherited from |wulfric|_. Arbitrary labels of atoms.
*   "species" :
    ``list`` of ``str``. Inherited from |wulfric|_. Chemical species of atoms.
*   "spglib_types" :
    ``list`` of ``int``. Inherited from |wulfric|_. Atomic types as defined in |spglib|_.
    Used in the symmetry analysis (via |wulfric|_ and |spglib|_). See
    :py:func:`wulfric.get_spglib_data` and :py:func:`wulfric.get_spglib_types` for
    details.
*   "positions" :
    ``list`` of ``list`` of ``float``. **Relative** coordinates of atoms. Inherited from
    |wulfric|_. Each element is an |array-like|_ of length :math:`3`.
*   "spins" :
    ``list`` of ``float``. Spin values for each atom.
*   "g_factors" :
    ``list`` of ``float``. g-factors for each atom.

We specify keys of the ``atoms`` dictionary that are expected by magnopy in the docstrings
of the relevant functions and classes.

.. hint::

    All lists in the ``atoms`` dictionary must have the same length :math:`M^{\prime}`.
    The order of atoms is preserved, i.e. the :math:`i`-th element of each list
    corresponds to the same atom.

    Magnopy extends the definition of ``atoms`` from |wulfric|_, therefore, any function
    of |wulfric|_ can be used on it.


``atoms`` is one of the three objects that are required for creation of the
:py:class:`.SpinHamiltonian` class. It is stored as an immutable attribute
:py:attr:`.SpinHamiltonian.cell`.

Magnetic vs non-magnetic atoms
==============================

Magnopy defines magnetic atom as an atom that has at least one parameter of the spin
Hamiltonian associated with it. Each spin Hamiltonian contains :math:`M` magnetic atoms
(:py:attr:`.SpinHamiltonian.M`). However, the crystal (cell & atoms) that are used for
the definition of the spin Hamiltonian can contain :math:`M^{\prime} \ne M` atoms.

Attribute :py:attr:`.SpinHamiltonian.atoms` returns a dictionary with all atoms of the
crystal, while :py:attr:`.SpinHamiltonian.magnetic_atoms` returns a dictionary with only
magnetic atoms. The order of atoms is the same in both.

.. _user-guide_usage_spin-directions:

***************
Spin directions
***************

Spin directions is rather simple data structure: a list of 3D unit vectors (|array-like|_).
It is used to defined some state of the Hamiltonian, for example its ground state.

Number of unit vectors in the list must be equal to the number of the magnetic atoms in
the unit cell of the spin Hamiltonian  (i. e. :py:attr:`.SpinHamiltonian.M`). Order of the
unit vectors in the list must correspond to the order of the atoms in
:py:attr:`.SpinHamiltonian.magnetic_atoms`.

* ``len(spin_directions) == spinham.M``
* ``spin_directions[i]`` is the spin direction (or local quantization axis) for the
  ``i``-th magnetic atom in the unit cell (i. e. for the
  ``spinham.magnetic_atoms.names[i]`` atom).


See also :ref:`user-guide_usage_spin-hamiltonian_magnetic-vs-non-magnetic`.

Here is an example of how to create a list of spin directions for a system with 3 atoms in
total (two magnetic and one non-magnetic)

.. doctest::

    >>> import numpy as np
    >>> import magnopy
    >>> # Create a Hamiltonian with three atoms
    >>> atoms = dict(
    ...     names=["Cr1", "Cr2", "Cr3"],
    ...     spins = [3/2, 3/2, 3/2],
    ...     g_factors=[2, 2, 2],
    ...     positions=[[0, 0, 0],[0.5, 0, 0],[0, 0.5, 0]]
    ... )
    >>> conv = magnopy.Convention(
    ...     multiple_counting=True,
    ...     spin_normalized=False,
    ...     c21=1
    ... )
    >>> spinham = magnopy.SpinHamiltonian(
    ...     cell=np.eye(3),
    ...     atoms=atoms,
    ...     convention=conv
    ... )
    >>> # Add an on-site quadratic anisotropy to the first and third atom
    >>> spinham.add_21(alpha=0, parameter = np.diag([1, 2, 3]))
    >>> spinham.add_21(alpha=2, parameter = np.diag([1, 2, 3]))


There are two magnetic atoms (Cr1 and Cr3) and one non-magnetic (Cr2). Therefore, the list
of spin directions must contain two unit vectors, for example

.. doctest::

    >>> spin_directions = [
    ...     [1, 0, 0],  # spin direction or local quantization axis for Cr1
    ...     [0, 0, 1]   # spin direction or local quantization axis for Cr3
    ... ]

If we add one more parameter that involves the second atom, for example an isotropic
exchange interaction between the first and second atoms

.. doctest::

    >>> spinham.add_22(alpha=0, beta=1, nu=(0, 0, 0), parameter=np.eye(3))

Then the list of spin directions must contain three unit vectors

.. doctest::

    >>> spin_directions = [
    ...     [1, 0, 0],  # spin direction or local quantization axis for Cr1
    ...     [0, 1, 0],  # spin direction or local quantization axis for Cr2
    ...     [0, 0, 1]   # spin direction or local quantization axis for Cr3
    ... ]

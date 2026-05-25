# ================================== LICENSE ===================================
# Magnopy - Python package for magnons.
#
# Copyright (C) 2023 Magnopy Team
#
# e-mail: anry@uv.es, web: magnopy.org
#
# This program is free software: you  can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the  Free Software
# Foundation,  either  version 3  of the License,  or (at your option) any later
# version.
#
# This program is distributed in the  hope  that it will be useful,  but WITHOUT
# ANY WARRANTY;  without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the  GNU General Public License  along with
# this program.  If not, see <https://www.gnu.org/licenses/>.
# ================================ END LICENSE =================================


import numpy as np
import warnings

from magnopy._spinham._convention import Convention
from magnopy._spinham._hamiltonian import SpinHamiltonian

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def load_grogu(
    filename,
    spin_values=None,
    spglib_types=None,
    g_factors=None,
    missing_bonds="restore",
    when_present="raise error",
) -> SpinHamiltonian:
    r"""
    Reads spin Hamiltonian from the .txt file produced by |GROGU|_.

    For more information on GROGU's file format see |GROGU-FF|_.

    Parameters
    ----------

    filename : str
        Path to the .txt file produced by |GROGU|_.

    spin_values : (M, ) iterable of floats, optional
        Spin values for all magnetic atom. Order is the same as in |GROGU|_ file. Magnetic
        atoms are defined as those that have at least one parameter associated with them.
        If none given, Magnopy uses spin values computed from DFT (as provided in the
        |GROGU|_ file).

    spglib_types : (M_prime, ) iterable of ints, optional
        Spglib types for all atoms (not only for magnetic ones, but for all). Order is the
        same as in |GROGU|_ file. If none given, then there will be no "spglib_types" key
        in ``spinham.atoms``.

    g_factors : (M, ) iterable of floats, optional

        .. versionadded:: 0.5.2

        g-factors for all atoms. Order is the same as in |TB2J|_ file. If none given, then
        Magnopy sets :math:`g = 2` for all atoms.

    missing_bonds : bool, default "restore"

        .. versionadded:: 0.5.2

        What to do if some of the equivalent bonds are missing (see
        :ref:`user-guide_theory-behind_equivalent-parameters`
        and :ref:`user-guide_theory-behind_convention_multiple-counting` for more details
        on equivalent bonds). Case-insensitive. Supported options are

        * "restore" (default)
          Magnopy adds missing equivalent bonds, by inserting additional parameters.

        * "ignore"

          Magnopy does nothing.

    when_present : str, default "raise error"

        .. versionadded:: 0.5.2

        What to do if the exact same interaction is repeated twice in the file.
        See :py:meth:`.SpinHamiltonian.add` for supported values.

    Returns
    -------

    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian, that is built from the |GROGU|_ file.

    Raises
    ------

    ValueError
        If ``spin_values`` is provided and its length does not match the number of
        magnetic atoms in the Hamiltonian.

    ValueError
        If ``spglib_types`` is provided and its length does not match the number of
        atoms in the Hamiltonian.

    """

    # Read the content of the file
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Read the convention
    i = 0
    CONVENTION_FOUND = True
    while "hamiltonian" not in lines[i].lower() or "convention" not in lines[i].lower():
        i += 1
        if i >= len(lines):
            CONVENTION_FOUND = False
            warnings.warn(
                "Could not find Hamiltonian convention section in the file from GROGU. Using default convention values.",
                UserWarning,
                stacklevel=2,
            )
            break

    if CONVENTION_FOUND:
        i += 1
        convention_data = []
        for _ in range(4):
            convention_data.append(lines[i].lower())
            i += 1

        # Double counting      true
        # Normalized spins     true
        # Intra-atomic factor  +1
        # Exchange factor      +0.5

        for entry in convention_data:
            if "double" in entry and "counting" in entry:
                value = entry.split()[-1].lower()
                if value in ["1", "true", "yes"]:
                    double_counting = True
                elif value in ["0", "false", "no"]:
                    double_counting = False
                else:
                    raise ValueError(
                        f"Could not parse double counting value from GROGU file: {entry}"
                    )
            elif "normalized" in entry and "spins" in entry:
                value = entry.split()[-1].lower()
                if value in ["1", "true", "yes"]:
                    spin_normalized = True
                elif value in ["0", "false", "no"]:
                    spin_normalized = False
                else:
                    raise ValueError(
                        f"Could not parse normalized spins value from GROGU file: {entry}"
                    )
            elif "intra-atomic" in entry and "factor" in entry:
                value = entry.split()[-1]
                try:
                    intra_atomic_factor = float(value)
                except ValueError:
                    raise ValueError(
                        f"Could not parse intra-atomic factor value from GROGU file: {entry}"
                    )
            elif "exchange" in entry and "factor" in entry:
                value = entry.split()[-1]
                try:
                    exchange_factor = float(value)
                except ValueError:
                    raise ValueError(
                        f"Could not parse exchange factor value from GROGU file: {entry}"
                    )
            else:
                raise RuntimeError(
                    f"Could not parse convention entry from GROGU file: {entry}"
                )

        convention = Convention(
            multiple_counting=double_counting,
            spin_normalized=spin_normalized,
            c21=intra_atomic_factor,
            c22=exchange_factor,
        )
    else:
        i = 0
        convention = Convention.get_predefined("grogu")

    # Read the cell
    while "cell" not in lines[i].lower() or "(ang)" not in lines[i].lower():
        i += 1
        if i >= len(lines):
            raise RuntimeError("Could not find cell section in the file from GROGU.")

    i += 1

    cell = [
        list(map(float, lines[i].split())),
        list(map(float, lines[i + 1].split())),
        list(map(float, lines[i + 2].split())),
    ]

    # Read the atoms
    while "magnetic" not in lines[i].lower() or "sites" not in lines[i].lower():
        i += 1
        if i >= len(lines):
            raise RuntimeError(
                "Could not find magnetic sites section in the file from GROGU."
            )

    i += 1
    M = int(lines[i].split()[3])
    i += 1

    # Check if spin_values were provided and of correct length
    if spin_values is not None and len(spin_values) != M:
        raise ValueError(f"Expected {M} spin values, got {len(spin_values)}")
    # Check if spglib_types were provided and of correct length
    if spglib_types is not None and len(spglib_types) != M:
        raise ValueError(f"Expected {M} spglib types, got {len(spglib_types)}")
    # Check if g_factors were provided and of correct length
    if g_factors is not None and len(g_factors) != M:
        raise ValueError(f"Expected {M} g-factors, got {len(g_factors)}")

    # Populate g_factors of atoms
    if g_factors is None:
        g_factors = [2] * M

    name_to_index = {}
    atoms = dict(names=[], positions=[], spins=[], g_factors=g_factors)

    for atom_index in range(M):
        i += 1
        words = lines[i].split()

        name = words[0]
        name_to_index[name] = atom_index

        positions = list(map(float, words[1:4]))
        positions = positions @ np.linalg.inv(cell)

        if spin_values is not None:
            spin = spin_values[atom_index]
        else:
            spin = float(words[4])

        atoms["names"].append(name)
        atoms["positions"].append(positions)
        atoms["spins"].append(spin)

    # Add spglib types if provided
    if spglib_types is not None:
        atoms["spglib_types"] = list(map(int, spglib_types))

    # Construct spin Hamiltonian
    spinham = SpinHamiltonian(convention=convention, cell=cell, atoms=atoms)

    while (
        "intra-atomic" not in lines[i].lower()
        or "anisotropy" not in lines[i].lower()
        or "tensor" not in lines[i].lower()
        or "(mev)" not in lines[i].lower()
    ):
        i += 1
        if i >= len(lines):
            raise RuntimeError(
                "Could not find intra-atomic anisotropy section in the file from GROGU."
            )

    for _ in range(M):
        i += 2
        name = lines[i].split()[0]
        alpha = name_to_index[name]
        i += 2
        parameter = [
            list(map(float, lines[i].split())),
            list(map(float, lines[i + 1].split())),
            list(map(float, lines[i + 2].split())),
        ]
        i += 2
        spinham.add(
            nus=[(0, 0, 0)],
            alphas=[alpha, alpha],
            parameter=parameter,
            when_present=when_present,
        )

    while (
        "exchange" not in lines[i].lower()
        or "tensor" not in lines[i].lower()
        or "(mev)" not in lines[i].lower()
    ):
        i += 1
        if i >= len(lines):
            raise RuntimeError(
                "Could not find exchange section in the file from GROGU."
            )

    i += 1
    N = int(lines[i].split()[3])
    i += 2

    for _ in range(N):
        i += 2

        words = lines[i].split()
        alpha = name_to_index[words[0]]
        beta = name_to_index[words[1]]
        nu = tuple(list(map(int, words[2:5])))

        i += 2

        parameter = [
            list(map(float, lines[i].split())),
            list(map(float, lines[i + 1].split())),
            list(map(float, lines[i + 2].split())),
        ]

        i += 2

        spinham.add(
            nus=[nu],
            alphas=[alpha, beta],
            parameter=parameter,
            when_present=when_present,
        )

    missing_bonds = missing_bonds.lower()
    if missing_bonds == "restore":
        spinham.restore_missing_parameters(strategy="mean")
    else:
        if missing_bonds != "ignore":
            raise ValueError(
                f"Unsupported value for missing_bonds. Expected 'restore' or 'ignore', got {missing_bonds}."
            )

    spinham._reset_internals()

    return spinham


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir

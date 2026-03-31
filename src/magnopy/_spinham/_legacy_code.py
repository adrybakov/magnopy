# ================================== LICENSE ===================================
# Magnopy - Python package for magnons.
# Copyright (C) 2023-2026 Magnopy Team
#
# e-mail: anry@uv.es, web: magnopy.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ================================ END LICENSE =================================

################################################################################
#                                     (1)                                      #
################################################################################


def _add_1(
    spinham, alpha: int, parameter, units=None, when_present="raise error"
) -> None:
    """
    Adds a parameter of one spin & one site term of the Hamiltonian (partition 1).

    .. deprecated:: 0.5.0 Use :py:meth:`.SpinHamiltonian.add` instead.

    See :ref:`user-guide_theory-behind_spin-hamiltonian` for the
    definition of the relevant term of the Hamiltonian.

    See :py:meth:`.SpinHamiltonian.add` for the detailed description of ``units``,
    ``when_present``, and ``populate_equivalent`` arguments.

    Parameters
    ----------
    alpha : int
        Index of an atom in the unit cell, with which the parameter is associated.
        ``0 <= alpha < len(spinham.atoms.names)``.

    parameter : (3, ) |array-like|_
        Value of the parameter (:math:`3\times1` vector). Given in the units of ``units``.

    units : str, optional
        .. versionadded:: 0.3.0

        Passed directly to :py:meth:`.SpinHamiltonian.add`.

    when_present : str, default "raise error"
        .. versionadded:: 0.4.0

        Passed directly to :py:meth:`.SpinHamiltonian.add`.

    See Also
    --------
    p1
    add
    remove
    parameters
    """

    spinham.add(
        nus=(),
        alphas=(alpha,),
        parameter=parameter,
        units=units,
        populate_equivalent=True,
        when_present=when_present,
    )


def _remove_1(spinham, alpha: int) -> None:
    """
    Removes a parameter of one spin & one site term of the Hamiltonian (partition 1).

    .. deprecated:: 0.5.0 Use :py:meth:`.SpinHamiltonian.remove` instead.

    See :ref:`user-guide_theory-behind_spin-hamiltonian` for the
    definition of the relevant term of the Hamiltonian.

    Parameters
    ----------
    alpha : int
        Index of an atom in the unit cell, with which the parameter is associated.
        ``0 <= alpha < len(spinham.atoms.names)``.

    See Also
    --------
    p1
    add
    remove
    parameters
    """

    spinham.remove(nus=(), alphas=(alpha,), remove_equivalent=True)


################################################################################
#                                    (2+0)                                     #
################################################################################


def _add_21(spinham, alpha: int, parameter, units=None, when_present="raise error"):
    """
    Adds a parameter of two spins & one site term of the Hamiltonian (partition 2+0).

    .. deprecated:: 0.5.0 Use :py:meth:`.SpinHamiltonian.add` instead.

    See :ref:`user-guide_theory-behind_spin-hamiltonian` for the
    definition of the relevant term of the Hamiltonian.

    See :py:meth:`.SpinHamiltonian.add` for the detailed description of ``units``,
    ``when_present``, and ``populate_equivalent`` arguments.

    Parameters
    ----------
    alpha : int
        Index of an atom in the unit cell, with which the parameter is associated.
        ``0 <= alpha < len(spinham.atoms.names)``.

    parameter : (3, 3) |array-like|_
        Value of the parameter (:math:`3\times3` matrix). Given in the units of ``units``.

    units : str, optional
        .. versionadded:: 0.3.0

        Passed directly to :py:meth:`.SpinHamiltonian.add`.

    when_present : str, default "raise error"
        .. versionadded:: 0.4.0

        Passed directly to :py:meth:`.SpinHamiltonian.add`.

    See Also
    --------
    p21
    add
    remove
    parameters
    """

    spinham.add(
        nus=((0, 0, 0),),
        alphas=(alpha, alpha),
        parameter=parameter,
        units=units,
        populate_equivalent=True,
        when_present=when_present,
    )


def _remove_21(spinham, alpha: int) -> None:
    """
    Removes a parameter of two spins & one site term of the Hamiltonian (partition 2+0).

    .. deprecated:: 0.5.0 Use :py:meth:`.SpinHamiltonian.remove` instead.

    See :ref:`user-guide_theory-behind_spin-hamiltonian` for the
    definition of the relevant term of the Hamiltonian.

    Parameters
    ----------
    alpha : int
        Index of an atom in the unit cell, with which the parameter is associated.
        ``0 <= alpha < len(spinham.atoms.names)``.

    See Also
    --------
    p21
    add
    remove
    parameters
    """

    spinham.remove(nus=((0, 0, 0),), alphas=(alpha, alpha), remove_equivalent=True)


################################################################################
#                                    (1+1)                                     #
################################################################################


def _add_22(
    spinham,
    alpha: int,
    beta: int,
    nu: tuple,
    parameter,
    units=None,
    when_present="raise error",
):
    """
    Adds a parameter of two spins & two sites term of the Hamiltonian (partition 1+1).

    .. deprecated:: 0.5.0 Use :py:meth:`.SpinHamiltonian.add` instead.

    See :ref:`user-guide_theory-behind_spin-hamiltonian` for the
    definition of the relevant term of the Hamiltonian.

    See :py:meth:`.SpinHamiltonian.add` for the detailed description of ``units``,
    ``when_present``, and ``populate_equivalent`` arguments.

    Parameters
    ----------
    alpha : int
        Index of an atom from the (0, 0, 0) unit cell.

        ``0 <= alpha < len(spinham.atoms.names)``.

    beta : int
        Index of an atom from the nu unit cell.

        ``0 <= beta < len(spinham.atoms.names)``.

    nu : tuple of 3 int
        Three relative coordinates with respect to the three lattice vectors, that
        specify the unit cell for the second atom.

    parameter : (3, 3) |array-like|_
        Value of the parameter (:math:`3\times3` matrix). Given in the units of ``units``.

    units : str, optional
        .. versionadded:: 0.3.0

        Passed directly to :py:meth:`.SpinHamiltonian.add`.

    when_present : str, default "raise error"
        .. versionadded:: 0.4.0

        Passed directly to :py:meth:`.SpinHamiltonian.add`.

    See Also
    --------
    p22
    add
    remove
    parameters
    """

    spinham.add(
        nus=(nu,),
        alphas=(alpha, beta),
        parameter=parameter,
        units=units,
        populate_equivalent=True,
        when_present=when_present,
    )


def _remove_22(spinham, alpha: int, beta: int, nu: tuple) -> None:
    """
    Removes a parameter of two spins & two sites term of the Hamiltonian (partition 1+1).

    .. deprecated:: 0.5.0 Use :py:meth:`.SpinHamiltonian.remove` instead.

    See :ref:`user-guide_theory-behind_spin-hamiltonian` for the
    definition of the relevant term of the Hamiltonian.

    Parameters
    ----------
    alpha : int
        Index of an atom from the (0, 0, 0) unit cell.

        ``0 <= alpha < len(spinham.atoms.names)``.

    beta : int
        Index of an atom from the nu unit cell.

        ``0 <= beta < len(spinham.atoms.names)``.

    nu : tuple of 3 int
        Three relative coordinates with respect to the three lattice vectors, that
        specify the unit cell for the second atom.

    See Also
    --------
    p22
    add
    remove
    parameters
    """

    spinham.remove(nus=(nu,), alphas=(alpha, beta), remove_equivalent=True)


################################################################################
#                                   (3+0+0)                                    #
################################################################################


def _add_31(spinham, alpha: int, parameter, units=None, when_present="raise error"):
    """
    Adds a parameter of three spins & one site term of the Hamiltonian (partition 3+0+0).

    .. deprecated:: 0.5.0 Use :py:meth:`.SpinHamiltonian.add` instead.

    See :ref:`user-guide_theory-behind_spin-hamiltonian` for the
    definition of the relevant term of the Hamiltonian.

    See :py:meth:`.SpinHamiltonian.add` for the detailed description of ``units``,
    ``when_present``, and ``populate_equivalent`` arguments.

    Parameters
    ----------
    alpha : int
        Index of an atom in the unit cell, with which the parameter is associated.
        ``0 <= alpha < len(spinham.atoms.names)``.

    parameter : (3, 3, 3) |array-like|_
        Value of the parameter (:math:`3\times3\times3` matrix). Given in the units of ``units``.

    units : str, optional
        .. versionadded:: 0.3.0

        Passed directly to :py:meth:`.SpinHamiltonian.add`.

    when_present : str, default "raise error"
        .. versionadded:: 0.4.0

        Passed directly to :py:meth:`.SpinHamiltonian.add`.

    See Also
    --------
    p31
    add
    remove
    parameters
    """

    spinham.add(
        nus=((0, 0, 0), (0, 0, 0)),
        alphas=(alpha, alpha, alpha),
        parameter=parameter,
        units=units,
        populate_equivalent=True,
        when_present=when_present,
    )


def _remove_31(spinham, alpha: int) -> None:
    """
    Removes a parameter of three spins & one site term of the Hamiltonian (partition 3+0+0).

    .. deprecated:: 0.5.0 Use :py:meth:`.SpinHamiltonian.remove` instead.

    See :ref:`user-guide_theory-behind_spin-hamiltonian` for the
    definition of the relevant term of the Hamiltonian.

    Parameters
    ----------
    alpha : int
        Index of an atom in the unit cell, with which the parameter is associated.
        ``0 <= alpha < len(spinham.atoms.names)``.

    See Also
    --------
    p31
    add
    remove
    parameters
    """

    spinham.remove(
        nus=((0, 0, 0), (0, 0, 0)), alphas=(alpha, alpha, alpha), remove_equivalent=True
    )


################################################################################
#                                  (4+0+0+0)                                   #
################################################################################


def _add_41(spinham, alpha: int, parameter, units=None, when_present="raise error"):
    """
    Adds a parameter of four spins & one site term of the Hamiltonian (partition 4+0+0+0).

    .. deprecated:: 0.5.0 Use :py:meth:`.SpinHamiltonian.add` instead.

    See :ref:`user-guide_theory-behind_spin-hamiltonian` for the
    definition of the relevant term of the Hamiltonian.

    See :py:meth:`.SpinHamiltonian.add` for the detailed description of ``units``,
    ``when_present``, and ``populate_equivalent`` arguments.

    Parameters
    ----------
    alpha : int
        Index of an atom in the unit cell, with which the parameter is associated.
        ``0 <= alpha < len(spinham.atoms.names)``.

    parameter : (3, 3, 3, 3) |array-like|_
        Value of the parameter (:math:`3\times3\times3\times3` matrix). Given in the units of ``units``.

    units : str, optional
        .. versionadded:: 0.3.0

        Passed directly to :py:meth:`.SpinHamiltonian.add`.

    when_present : str, default "raise error"
        .. versionadded:: 0.4.0

        Passed directly to :py:meth:`.SpinHamiltonian.add`.

    See Also
    --------
    p31
    add
    remove
    parameters
    """

    spinham.add(
        nus=((0, 0, 0), (0, 0, 0), (0, 0, 0)),
        alphas=(alpha, alpha, alpha, alpha),
        parameter=parameter,
        units=units,
        populate_equivalent=True,
        when_present=when_present,
    )


def _remove_41(spinham, alpha: int) -> None:
    """
    Removes a parameter of four spins & one site term of the Hamiltonian (partition 4+0+0+0).

    .. deprecated:: 0.5.0 Use :py:meth:`.SpinHamiltonian.remove` instead.

    See :ref:`user-guide_theory-behind_spin-hamiltonian` for the
    definition of the relevant term of the Hamiltonian.

    Parameters
    ----------
    alpha : int
        Index of an atom in the unit cell, with which the parameter is associated.
        ``0 <= alpha < len(spinham.atoms.names)``.

    See Also
    --------
    p31
    add
    remove
    parameters
    """

    spinham.remove(
        nus=((0, 0, 0), (0, 0, 0), (0, 0, 0)),
        alphas=(alpha, alpha, alpha, alpha),
        remove_equivalent=True,
    )

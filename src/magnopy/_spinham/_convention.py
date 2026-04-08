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


R"""
Convention of spin Hamiltonian
"""

from magnopy._constants._conventions import _SPINHAM_CONVENTIONS
from magnopy._exceptions import ConventionError

ATTRIBUTE_ERROR_MESSAGE = "It is intentionally forbidden to change individual properties of convention. Use convention.get_modified(...) and/or spinham.convention = spinham.convention.get_modified(...)"

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


class Convention:
    R"""
    Convention of the spin Hamiltonian.

    For more details see :ref:`user-guide_theory-behind_convention` and
    :ref:`user-guide_theory-behind_spin-hamiltonian`.

    Parameters
    ----------

    multiple_counting : bool, optional
        Whether the pairs of spins are counted multiple times in the Hamiltonian's sums.

    spin_normalized : bool, optional
        Whether spin vectors/operators are "normalized" to 1. If ``True``, then spin
        vectors/operators are "normalized".

    c1 : float, optional
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_1-1`).

    c21 : float, optional
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_2-1`).

    c22 : float, optional
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_2-2`).

    c31 : float, optional
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_3-1`).

    c32 : float, optional
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_3-2`).

    c33 : float, optional
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_3-3`).

    c41 : float, optional
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_4-1`).

    c42 : float, optional
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_4-2`).

    c43 : float, optional
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_4-3`).

    c44 : float, optional
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_4-4`).

    c45 : float, optional
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_4-5`).

    name : str, default "custom"
        A label for the convention. Any string, case-insensitive.

    Examples
    --------

    Creating conventions

    .. doctest::

        >>> import magnopy
        >>> conv_1 = magnopy.Convention(True, True, c21=1, c22=-0.5, name="conv #1")
        >>> conv_2 = magnopy.Convention(False, True, c21=1, c22=-0.5, name="conv #2")
        >>> conv_3 = magnopy.Convention(False, True, c22=-0.5, name="conv #3")

    Individual properties of the convention

    .. doctest::

        >>> conv_1.multiple_counting
        True
        >>> conv_3.c21
        Traceback (most recent call last):
        ...
        magnopy._exceptions.ConventionError: Convention of spin Hamiltonian has an undefined property 'c21':
        "conv #3" convention where
          * Bonds are counted once in the sum;
          * Spin vectors are normalized to 1;
          * Undefined c1 factor;
          * Undefined c21 factor;
          * c22 = -0.5;
          * Undefined c31 factor;
          * Undefined c32 factor;
          * Undefined c33 factor;
          * Undefined c41 factor;
          * Undefined c42 factor;
          * Undefined c43 factor;
          * Undefined c44 factor;
          * Undefined c45 factor.
        >>> conv_3.name
        'conv #3'

    Full summary of the convention

    .. doctest::

        >>> print(conv_1)
        "conv #1" convention where
          * Bonds are counted multiple times in the sum;
          * Spin vectors are normalized to 1;
          * Undefined c1 factor;
          * c21 = 1.0;
          * c22 = -0.5;
          * Undefined c31 factor;
          * Undefined c32 factor;
          * Undefined c33 factor;
          * Undefined c41 factor;
          * Undefined c42 factor;
          * Undefined c43 factor;
          * Undefined c44 factor;
          * Undefined c45 factor.

    Comparing conventions

    .. doctest::

        >>> conv_1 == conv_2
        False
        >>> conv_1 != conv_3
        True

    """

    __slots__ = (
        "_multiple_counting",
        "_spin_normalized",
        "_c1",
        "_c21",
        "_c22",
        "_c31",
        "_c32",
        "_c33",
        "_c41",
        "_c42",
        "_c43",
        "_c44",
        "_c45",
        "_name",
    )

    __comparison_attributes__ = (
        "_multiple_counting",
        "_spin_normalized",
        "_c1",
        "_c21",
        "_c22",
        "_c31",
        "_c32",
        "_c33",
        "_c41",
        "_c42",
        "_c43",
        "_c44",
        "_c45",
    )

    def __init__(
        self,
        multiple_counting: bool = None,
        spin_normalized: bool = None,
        c1: float = None,
        c21: float = None,
        c22: float = None,
        c31: float = None,
        c32: float = None,
        c33: float = None,
        c41: float = None,
        c42: float = None,
        c43: float = None,
        c44: float = None,
        c45: float = None,
        name: str = "custom",
    ) -> None:
        if multiple_counting is not None:
            self._multiple_counting = bool(multiple_counting)
        else:
            self._multiple_counting = None

        if spin_normalized is not None:
            self._spin_normalized = bool(spin_normalized)
        else:
            self._spin_normalized = None

        if c1 is not None:
            self._c1 = float(c1)
        else:
            self._c1 = None

        if c21 is not None:
            self._c21 = float(c21)
        else:
            self._c21 = None

        if c22 is not None:
            self._c22 = float(c22)
        else:
            self._c22 = None

        if c31 is not None:
            self._c31 = float(c31)
        else:
            self._c31 = None

        if c32 is not None:
            self._c32 = float(c32)
        else:
            self._c32 = None

        if c33 is not None:
            self._c33 = float(c33)
        else:
            self._c33 = None

        if c41 is not None:
            self._c41 = float(c41)
        else:
            self._c41 = None

        if c42 is not None:
            self._c42 = float(c42)
        else:
            self._c42 = None

        if c43 is not None:
            self._c43 = float(c43)
        else:
            self._c43 = None

        if c44 is not None:
            self._c44 = float(c44)
        else:
            self._c44 = None

        if c45 is not None:
            self._c45 = float(c45)
        else:
            self._c45 = None

        self._name = str(name).lower()

    ################################################################################
    #                                   Summary                                    #
    ################################################################################

    def __repr__(self):
        return (
            "\n    ".join(
                [
                    "magnopy.Convention(",
                    f"multiple_counting = {self._multiple_counting},",
                    f"spin_normalized = {self._spin_normalized},",
                    f"c1 = {self._c1},",
                    f"c21 = {self._c21},",
                    f"c22 = {self._c22},",
                    f"c31 = {self._c31},",
                    f"c32 = {self._c32},",
                    f"c33 = {self._c33},",
                    f"c41 = {self._c41},",
                    f"c42 = {self._c42},",
                    f"c43 = {self._c43},",
                    f"c44 = {self._c44},",
                    f"c45 = {self._c45},",
                    f'name = "{self.name}"',
                ]
            )
            + "\n)"
        )

    def __str__(self):
        summary = [f'"{self.name}" convention where']

        if self._multiple_counting is None:
            summary.append("  * Undefined multiple counting;")
        elif self._multiple_counting:
            summary.append("  * Bonds are counted multiple times in the sum;")
        else:
            summary.append("  * Bonds are counted once in the sum;")

        if self._spin_normalized is None:
            summary.append("  * Undefined spin normalization;")
        elif self._spin_normalized:
            summary.append("  * Spin vectors are normalized to 1;")
        else:
            summary.append("  * Spin vectors are not normalized;")

        # One spin
        if self._c1 is None:
            summary.append("  * Undefined c1 factor;")
        else:
            summary.append(f"  * c1 = {self._c1};")

        # Two spins
        if self._c21 is None:
            summary.append("  * Undefined c21 factor;")
        else:
            summary.append(f"  * c21 = {self._c21};")

        if self._c22 is None:
            summary.append("  * Undefined c22 factor;")
        else:
            summary.append(f"  * c22 = {self._c22};")

        # Three spins
        if self._c31 is None:
            summary.append("  * Undefined c31 factor;")
        else:
            summary.append(f"  * c31 = {self._c31};")

        if self._c32 is None:
            summary.append("  * Undefined c32 factor;")
        else:
            summary.append(f"  * c32 = {self._c32};")

        if self._c33 is None:
            summary.append("  * Undefined c33 factor;")
        else:
            summary.append(f"  * c33 = {self._c33};")

        # Four spins
        if self._c41 is None:
            summary.append("  * Undefined c41 factor;")
        else:
            summary.append(f"  * c41 = {self._c41};")

        if self._c42 is None:
            summary.append("  * Undefined c42 factor;")
        else:
            summary.append(f"  * c42 = {self._c42};")

        if self._c43 is None:
            summary.append("  * Undefined c43 factor;")
        else:
            summary.append(f"  * c43 = {self._c43};")

        if self._c44 is None:
            summary.append("  * Undefined c44 factor;")
        else:
            summary.append(f"  * c44 = {self._c44};")

        if self._c45 is None:
            summary.append("  * Undefined c45 factor.")
        else:
            summary.append(f"  * c45 = {self._c45}.")

        summary = ("\n").join(summary)

        return summary

    # DEPRECATED in v0.4.0
    # Remove in May 2026
    def summary(self, return_as_string=False):
        r"""
        Gives human-readable summary of the convention.

        .. deprecated:: 0.4.0
            Will be removed in May of 2026. Use ``print(convention)`` or ``str(convention)`` instead.

        Parameters
        ----------
        return_as_string : bool, default False
            Whether to print or return a ``str``. If ``True``, then returns a ``str``.
            If ``False``, then prints it.

        Examples
        --------

        .. doctest::

            >>> from magnopy import Convention
            >>> conv_1 = Convention(True, True, c21=1, c22=-0.5)
            >>> conv_1.summary()
            "custom" convention where
              * Bonds are counted multiple times in the sum;
              * Spin vectors are normalized to 1;
              * Undefined c1 factor;
              * c21 = 1.0;
              * c22 = -0.5;
              * Undefined c31 factor;
              * Undefined c32 factor;
              * Undefined c33 factor;
              * Undefined c41 factor;
              * Undefined c42 factor;
              * Undefined c43 factor;
              * Undefined c44 factor;
              * Undefined c45 factor.
        """

        import warnings

        warnings.warn(
            "The 'summary' method is deprecated since Magnopy 0.4.0. Use print(convention) or str(convention) instead. magnopy.Convention.summary will be removed in May of 2026.",
            DeprecationWarning,
            stacklevel=2,
        )

        summary = self.__str__()

        if return_as_string:
            return summary

        print(summary)

    @property
    def name(self) -> str:
        r"""
        A label for the convention.

        Arbitrary string, case-insensitive.

        Returns
        -------

        name : str

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(name="Conv #1")
            >>> conv.name
            'conv #1'
        """

        return self._name

    @name.setter
    def name(self, new_value: str):
        self._name = str(new_value).lower()

    ################################################################################
    #                               Multiple counting                              #
    ################################################################################
    @property
    def multiple_counting(self) -> bool:
        r"""
        Whether the all elements of the equivalent sets of interaction parameters are
        included in the Hamiltonian's sums.

        If ``True``, then each element of the set of equivalent interaction parameters is
        included in the Hamiltonian's sums. If ``False``, then only one element of the
        set of equivalent interaction parameters is included in the Hamiltonian's sums.

        Returns
        -------

        multiple_counting : bool

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(multiple_counting=True)
            >>> conv.multiple_counting
            True

        """
        if self._multiple_counting is None:
            raise ConventionError(convention=self, property="multiple_counting")
        return self._multiple_counting

    @multiple_counting.setter
    def multiple_counting(self, new_value: bool):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    ################################################################################
    #                            Normalization of spins                            #
    ################################################################################
    @property
    def spin_normalized(self) -> bool:
        r"""
        Whether spin vectors/operators are "normalized" to 1.

        If ``True``, then spin vectors/operators are "normalized". If ``False``, then
        spin vectors/operators are not "normalized".

        Returns
        -------

        spin_normalized : bool

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(spin_normalized=False)
            >>> conv.spin_normalized
            False
        """
        if self._spin_normalized is None:
            raise ConventionError(convention=self, property="spin_normalized")
        return self._spin_normalized

    @spin_normalized.setter
    def spin_normalized(self, new_value: bool):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    ################################################################################
    #                                   One spin                                   #
    ################################################################################
    @property
    def c1(self) -> float:
        r"""
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_1-1`).

        Returns
        -------

        c1 : float

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(c1=0.5)
            >>> conv.c1
            0.5

        """
        if self._c1 is None:
            raise ConventionError(convention=self, property="c1")
        return self._c1

    @c1.setter
    def c1(self, new_value: float):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    ################################################################################
    #                                   Two spins                                  #
    ################################################################################
    @property
    def c21(self) -> float:
        r"""
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_2-1`).

        Returns
        -------

        c21 : float

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(c21=-1)
            >>> conv.c21
            -1.0
        """
        if self._c21 is None:
            raise ConventionError(convention=self, property="c21")
        return self._c21

    @c21.setter
    def c21(self, new_value: float):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    @property
    def c22(self) -> float:
        r"""
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_2-2`).

        Returns
        -------

        c22 : float

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(c22=1 / 2)
            >>> conv.c22
            0.5

        """
        if self._c22 is None:
            raise ConventionError(convention=self, property="c22")
        return self._c22

    @c22.setter
    def c22(self, new_value: float):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    ################################################################################
    #                                  Three spins                                 #
    ################################################################################
    @property
    def c31(self) -> float:
        r"""
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_3-1`).

        Returns
        -------

        c31 : float

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(c31=-1)
            >>> conv.c31
            -1.0

        """
        if self._c31 is None:
            raise ConventionError(convention=self, property="c31")
        return self._c31

    @c31.setter
    def c31(self, new_value: float):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    @property
    def c32(self) -> float:
        r"""
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_3-2`).

        Returns
        -------

        c32 : float

        Examples
        --------
        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(c32=1 / 3)
            >>> conv.c32
            0.3333333333333333

        """
        if self._c32 is None:
            raise ConventionError(convention=self, property="c32")
        return self._c32

    @c32.setter
    def c32(self, new_value: float):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    @property
    def c33(self) -> float:
        r"""
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_3-3`).

        Returns
        -------

        c33 : float

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(c33=1 / 6)
            >>> conv.c33
            0.16666666666666666

        """
        if self._c33 is None:
            raise ConventionError(convention=self, property="c33")
        return self._c33

    @c33.setter
    def c33(self, new_value: float):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    ################################################################################
    #                                  Four spins                                  #
    ################################################################################
    @property
    def c41(self) -> float:
        r"""
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_4-1`).

        Returns
        -------

        c41 : float

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(c41=-1)
            >>> conv.c41
            -1.0

        """
        if self._c41 is None:
            raise ConventionError(convention=self, property="c41")
        return self._c41

    @c41.setter
    def c41(self, new_value: float):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    @property
    def c42(self) -> float:
        r"""
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_4-2`).

        Returns
        -------

        c42 : float

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(c42=1 / 4)
            >>> conv.c42
            0.25
        """
        if self._c42 is None:
            raise ConventionError(convention=self, property="c42")
        return self._c42

    @c42.setter
    def c42(self, new_value: float):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    @property
    def c43(self) -> float:
        r"""
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_4-3`).

        Returns
        -------

        c43 : float

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(c43=1 / 6)
            >>> conv.c43
            0.16666666666666666

        """
        if self._c43 is None:
            raise ConventionError(convention=self, property="c43")
        return self._c43

    @c43.setter
    def c43(self, new_value: float):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    @property
    def c44(self) -> float:
        r"""
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_4-4`).

        Returns
        -------

        c44 : float

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(c44=1 / 12)
            >>> conv.c44
            0.08333333333333333

        """
        if self._c44 is None:
            raise ConventionError(convention=self, property="c44")
        return self._c44

    @c44.setter
    def c44(self, new_value: float):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    @property
    def c45(self) -> float:
        r"""
        Numerical factor before the sum over sites in the spin Hamiltonian
        (:ref:`ug_tb_sh_4-5`).

        Returns
        -------

        c45 : float

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(c45=1 / 24)
            >>> conv.c45
            0.041666666666666664
        """
        if self._c45 is None:
            raise ConventionError(convention=self, property="c45")
        return self._c45

    @c45.setter
    def c45(self, new_value: float):
        raise AttributeError(ATTRIBUTE_ERROR_MESSAGE)

    ################################################################################
    #                              Comparison and has                              #
    ################################################################################

    # Note: semi-private attributes are compared intentionally, as public ones raise
    # an error if not defined.
    # When attributes are not defined in both conventions, then these attributes are
    # considered equal.
    def __eq__(self, other):
        if not isinstance(other, Convention):
            return NotImplemented

        return all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__comparison_attributes__
        )

    def __hash__(self):

        return hash(
            tuple(getattr(self, attr) for attr in self.__comparison_attributes__)
        )

    ################################################################################
    #                                Simple getters                                #
    ################################################################################

    @staticmethod
    def get_predefined(name: str):
        r"""
        Returns one of the predefined conventions.

        Parameters
        ----------

        name : str
            Name of the desired predefined convention. Supported are

            * "tb2j"
            * "grogu"
            * "vampire"
            * "spinw"

            Case-insensitive.

        Returns
        -------

        convention : :py:class:`.Convention`

        Notes
        -----

        To check which conventions are hard-coded in Magnopy one can do

        .. doctest::

            >>> from magnopy._constants._conventions import _SPINHAM_CONVENTIONS
            >>> print(list(_SPINHAM_CONVENTIONS.keys()))
            ['tb2j', 'grogu', 'vampire', 'spinw']

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> tb2j = magnopy.Convention.get_predefined("TB2J")
            >>> print(tb2j)
            "tb2j" convention where
              * Bonds are counted multiple times in the sum;
              * Spin vectors are normalized to 1;
              * Undefined c1 factor;
              * c21 = -1.0;
              * c22 = -1.0;
              * Undefined c31 factor;
              * Undefined c32 factor;
              * Undefined c33 factor;
              * Undefined c41 factor;
              * Undefined c42 factor;
              * Undefined c43 factor;
              * Undefined c44 factor;
              * Undefined c45 factor.

        .. doctest::

            >>> grogu = magnopy.Convention.get_predefined("GROGU")
            >>> print(grogu)
            "grogu" convention where
              * Bonds are counted multiple times in the sum;
              * Spin vectors are normalized to 1;
              * Undefined c1 factor;
              * c21 = 1.0;
              * c22 = 0.5;
              * Undefined c31 factor;
              * Undefined c32 factor;
              * Undefined c33 factor;
              * Undefined c41 factor;
              * Undefined c42 factor;
              * Undefined c43 factor;
              * Undefined c44 factor;
              * Undefined c45 factor.

        .. doctest::

            >>> vampire = magnopy.Convention.get_predefined("Vampire")
            >>> print(vampire)
            "vampire" convention where
              * Bonds are counted multiple times in the sum;
              * Spin vectors are normalized to 1;
              * Undefined c1 factor;
              * c21 = -1.0;
              * c22 = -0.5;
              * Undefined c31 factor;
              * Undefined c32 factor;
              * Undefined c33 factor;
              * Undefined c41 factor;
              * Undefined c42 factor;
              * Undefined c43 factor;
              * Undefined c44 factor;
              * Undefined c45 factor.

        .. doctest::

            >>> spinW = magnopy.Convention.get_predefined("spinW")
            >>> print(spinW)
            "spinw" convention where
              * Bonds are counted multiple times in the sum;
              * Spin vectors are not normalized;
              * Undefined c1 factor;
              * c21 = 1.0;
              * c22 = 1.0;
              * Undefined c31 factor;
              * Undefined c32 factor;
              * Undefined c33 factor;
              * Undefined c41 factor;
              * Undefined c42 factor;
              * Undefined c43 factor;
              * Undefined c44 factor;
              * Undefined c45 factor.
        """

        name = name.lower()

        if name not in _SPINHAM_CONVENTIONS:
            raise ValueError(
                f'"{name}" convention is undefined. Supported are\n - '
                + "\n - ".join([f'"{key}"' for key in _SPINHAM_CONVENTIONS])
            )

        return Convention(name=name, **_SPINHAM_CONVENTIONS[name])

    def get_modified(
        self,
        multiple_counting: bool = None,
        spin_normalized: bool = None,
        c1: float = None,
        c21: float = None,
        c22: float = None,
        c31: float = None,
        c32: float = None,
        c33: float = None,
        c41: float = None,
        c42: float = None,
        c43: float = None,
        c44: float = None,
        c45: float = None,
        name: str = None,
    ):
        r"""
        Returns a new instance of the :py:class:`.Convention` class.

        Properties of the new instance are the same as in the original convention, except
        for those explicitly given as arguments of this method.

        Parameters
        ----------

        multiple_counting : bool, optional
            Whether the pairs of spins are counted multiple times in the Hamiltonian's
            sums.

        spin_normalized : bool, optional
            Whether spin vectors/operators are normalized to 1. If ``True``, then spin
            vectors/operators are normalized.

        c1 : float, optional
            Numerical factor before the sum over sites in the spin Hamiltonian
            (:ref:`ug_tb_sh_1-1`).

        c21 : float, optional
            Numerical factor before the sum over sites in the spin Hamiltonian
            (:ref:`ug_tb_sh_2-1`).

        c22 : float, optional
            Numerical factor before the sum over sites in the spin Hamiltonian
            (:ref:`ug_tb_sh_2-2`).

        c31 : float, optional
            Numerical factor before the sum over sites in the spin Hamiltonian
            (:ref:`ug_tb_sh_3-1`).

        c32 : float, optional
            Numerical factor before the sum over sites in the spin Hamiltonian
            (:ref:`ug_tb_sh_3-2`).

        c33 : float, optional
            Numerical factor before the sum over sites in the spin Hamiltonian
            (:ref:`ug_tb_sh_3-3`).

        c41 : float, optional
            Numerical factor before the sum over sites in the spin Hamiltonian
            (:ref:`ug_tb_sh_4-1`).

        c42 : float, optional
            Numerical factor before the sum over sites in the spin Hamiltonian
            (:ref:`ug_tb_sh_4-2`).

        c43 : float, optional
            Numerical factor before the sum over sites in the spin Hamiltonian
            (:ref:`ug_tb_sh_4-3`).

        c44 : float, optional
            Numerical factor before the sum over sites in the spin Hamiltonian
            (:ref:`ug_tb_sh_4-4`).

        c45 : float, optional
            Numerical factor before the sum over sites in the spin Hamiltonian
            (:ref:`ug_tb_sh_4-5`).

        name : str, optional
            A label for the convention. Any string, case-insensitive.

        Notes
        -----

        Giving ``None`` as the value to the keyword arguments of this method does not
        change the corresponding properties of the convention

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(name="original", c21=1)
            >>> mod_conv = conv.get_modified(name="modified", c21=None)
            >>> # Still 1, not None
            >>> mod_conv.c21
            1.0

        Examples
        --------

        .. doctest::

            >>> import magnopy
            >>> conv = magnopy.Convention(
            ...     name="original",
            ...     multiple_counting=True,
            ...     spin_normalized=False,
            ...     c1=1,
            ...     c21=1,
            ...     c22=-1,
            ... )
            >>> print(conv)
            "original" convention where
              * Bonds are counted multiple times in the sum;
              * Spin vectors are not normalized;
              * c1 = 1.0;
              * c21 = 1.0;
              * c22 = -1.0;
              * Undefined c31 factor;
              * Undefined c32 factor;
              * Undefined c33 factor;
              * Undefined c41 factor;
              * Undefined c42 factor;
              * Undefined c43 factor;
              * Undefined c44 factor;
              * Undefined c45 factor.

        .. doctest::

            >>> mod_conv = conv.get_modified(name="modified", c22=1, c33=-3)
            >>> print(mod_conv)
            "modified" convention where
              * Bonds are counted multiple times in the sum;
              * Spin vectors are not normalized;
              * c1 = 1.0;
              * c21 = 1.0;
              * c22 = 1.0;
              * Undefined c31 factor;
              * Undefined c32 factor;
              * c33 = -3.0;
              * Undefined c41 factor;
              * Undefined c42 factor;
              * Undefined c43 factor;
              * Undefined c44 factor;
              * Undefined c45 factor.

        """

        if multiple_counting is None:
            multiple_counting = self._multiple_counting

        if spin_normalized is None:
            spin_normalized = self._spin_normalized

        if c1 is None:
            c1 = self._c1

        if c21 is None:
            c21 = self._c21

        if c22 is None:
            c22 = self._c22

        if c31 is None:
            c31 = self._c31

        if c32 is None:
            c32 = self._c32

        if c33 is None:
            c33 = self._c33

        if c41 is None:
            c41 = self._c41

        if c42 is None:
            c42 = self._c42

        if c43 is None:
            c43 = self._c43

        if c44 is None:
            c44 = self._c44

        if c45 is None:
            c45 = self._c45

        if name is None:
            name = self.name

        return Convention(
            spin_normalized=spin_normalized,
            multiple_counting=multiple_counting,
            c1=c1,
            c21=c21,
            c22=c22,
            c31=c31,
            c32=c32,
            c33=c33,
            c41=c41,
            c42=c42,
            c43=c43,
            c44=c44,
            c45=c45,
            name=name,
        )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir

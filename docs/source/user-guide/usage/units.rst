.. _user-guide_usage_units:

*****
Units
*****


Magnopy supports a number of units for some of the data it deals with. Both for the input
and the output. On this page we describe what units are supported and in which context.

.. _user-guide_usage_units_energy-units:

Units of energy
===============

Magnopy outputs a number of properties that have units of energy. By default magnopy
outputs energy in the units of "meV", but the user can ask for other supported units.

.. hint::
    To check what units are hardcoded in magnopy's source code one can use the trick:

    .. doctest::

        >>> from magnopy._constants._units import _ENERGY_UNITS
        >>> print(list(_ENERGY_UNITS))
        ['ev', 'mev', 'joule', 'j', 'ry', 'rydberg', 'erg']

*   Electronvolt (eV)

    Keywords: "eV"

*   Millielectronvolt (meV)

    Keywords: "meV"

*   Joule

    Keywords: "Joule", "J"

*   Rydberg units of energy

    Keywords: "Ry", "Rydberg"

*   Erg

    Keywords: "Erg"

Below are the conversion factors between all those units.

.. doctest::

    >>> import magnopy
    >>> eV = magnopy.si.ELECTRON_VOLT
    >>> meV = magnopy.si.MILLI * magnopy.si.ELECTRON_VOLT
    >>> Joule = magnopy.si.JOULE
    >>> Rydberg = magnopy.si.RYDBERG_ENERGY
    >>> Erg = magnopy.si.ERG

.. doctest::

    >>> print(f"{eV / meV:.8e} meV in 1 eV")
    1.00000000e+03 meV in 1 eV
    >>> print(f"{eV / Joule:.8e} Joule in 1 eV")
    1.60217663e-19 Joule in 1 eV
    >>> print(f"{eV / Rydberg:.8e} Rydberg in 1 eV")
    7.34986444e-02 Rydberg in 1 eV
    >>> print(f"{eV / Erg:.8e} Erg in eV")
    1.60217663e-12 Erg in eV

.. doctest::

    >>> print(f"{meV / eV:.8e} eV in 1 meV")
    1.00000000e-03 eV in 1 meV
    >>> print(f"{meV / Joule:.8e} Joule in 1 meV")
    1.60217663e-22 Joule in 1 meV
    >>> print(f"{meV / Rydberg:.8e} Rydberg in 1 meV")
    7.34986444e-05 Rydberg in 1 meV
    >>> print(f"{meV / Erg:.8e} Erg in meV")
    1.60217663e-15 Erg in meV


.. doctest::

    >>> print(f"{Joule / eV:.8e} eV in 1 Joule")
    6.24150907e+18 eV in 1 Joule
    >>> print(f"{Joule / meV:.8e} meV in 1 Joule")
    6.24150907e+21 meV in 1 Joule
    >>> print(f"{Joule / Rydberg:.8e} Rydberg in 1 Joule")
    4.58742456e+17 Rydberg in 1 Joule
    >>> print(f"{Joule / Erg:.8e} Erg in Joule")
    1.00000000e+07 Erg in Joule


.. doctest::

    >>> print(f"{Rydberg / eV:.7f} eV in 1 Rydberg")
    13.6056931 eV in 1 Rydberg
    >>> print(f"{Rydberg / meV:.4f} meV in 1 Rydberg")
    13605.6931 meV in 1 Rydberg
    >>> print(f"{Rydberg / Joule:.8e} Joule in 1 Rydberg")
    2.17987236e-18 Joule in 1 Rydberg
    >>> print(f"{Rydberg / Erg:.8e} Erg in Rydberg")
    2.17987236e-11 Erg in Rydberg

.. doctest::

    >>> print(f"{Erg / eV:.8e} eV in 1 Erg")
    6.24150907e+11 eV in 1 Erg
    >>> print(f"{Erg / meV:.8e} meV in 1 Erg")
    6.24150907e+14 meV in 1 Erg
    >>> print(f"{Erg / Joule:.8e} Joule in 1 Erg")
    1.00000000e-07 Joule in 1 Erg
    >>> print(f"{Erg / Rydberg:.8e} Rydberg in 1 Erg")
    4.58742456e+10 Rydberg in 1 Erg


.. _user-guide_usage_units_parameter-units:

Units of Hamiltonian's parameters
=================================

Parameters of the :ref:`user-guide_theory-behind_spin-hamiltonian` are typically stored
in some units of energy (i.e meV or Joule) or some units that offer direct conversion to
some energy scale (like Kelvin, via Boltzmann constant). Magnopy takes the same approach
and support a number of energy-like units.

.. hint::
    To check what units are hardcoded in magnopy's source code one can use the trick:

    .. doctest::

        >>> from magnopy._constants._units import _PARAMETER_UNITS
        >>> print(list(_PARAMETER_UNITS))
        ['ev', 'mev', 'joule', 'j', 'ry', 'rydberg', 'erg', 'k', 'kelvin']

For the parameters fo the spin Hamiltonian magnopy supports all
:ref:`user-guide_usage_units_energy-units` from above and

*   Kelvin

    Keywords: "K", "Kelvin"


Below are the conversion factors.

.. doctest::

    >>> Kelvin = magnopy._constants._units._PARAMETER_UNITS["kelvin"]
    >>> print(f"{Kelvin / eV:.8e} eV in 1 Kelvin")
    8.61733326e-05 eV in 1 Kelvin
    >>> print(f"{Kelvin / meV:.8f} meV in 1 Kelvin")
    0.08617333 meV in 1 Kelvin
    >>> print(f"{Kelvin / Joule:.8e} Joule in 1 Kelvin")
    1.38064900e-23 Joule in 1 Kelvin
    >>> print(f"{Kelvin / Rydberg:.8e} Rydberg in 1 Kelvin")
    6.33362313e-06 Rydberg in 1 Kelvin
    >>> print(f"{Kelvin / Erg:.8e} Erg in 1 Kelvin")
    1.38064900e-16 Erg in 1 Kelvin

.. doctest::

    >>> print(f"{eV / Kelvin:.4f} Kelvin in 1 eV")
    11604.5181 Kelvin in 1 eV
    >>> print(f"{meV / Kelvin:.7f} Kelvin in 1 meV")
    11.6045181 Kelvin in 1 meV
    >>> print(f"{Joule / Kelvin:.8e} Kelvin in 1 Joule")
    7.24297052e+22 Kelvin in 1 Joule
    >>> print(f"{Rydberg / Kelvin:.3f} Kelvin in 1 Rydberg")
    157887.512 Kelvin in 1 Rydberg
    >>> print(f"{Erg / Kelvin:.8e} Kelvin in 1 Erg")
    7.24297052e+15 Kelvin in 1 Erg

.. _user-guide_usage_units_magnon-energy-units:

Units of magnon energies
========================

.. hint::
    To check what units are hardcoded in magnopy's source code one can use the trick:

    .. doctest::

        >>> from magnopy._constants._units import _FREQ_UNITS
        >>> print(list(_FREQ_UNITS))
        ['ev', 'mev', 'joule', 'j', 'ry', 'rydberg', 'erg', 'hertz', 'hz', 'giga-hertz', 'ghz', 'tera-hertz', 'thz']

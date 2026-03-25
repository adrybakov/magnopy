.. toctree::
    :maxdepth: 1
    :hidden:

    User Guide <user-guide/index>
    user-support/index
    api/index
    release-notes/index
    cite
    development/index

:Release: |version|
:Date: |release_date|

**Useful links**:
|issue-tracker|_ |
:ref:`Cite <cite>` |
:ref:`support` |
|magnopy-tutorials|_

.. hint::

    We recommend to install Magnopy with optional dependencies (|plotly|_ and |matplotlib|_)
    whether possible.

    .. code-block:: bash

        pip install "magnopy[visual]"

    as then Magnopy produces graphical output (.html and .png files) in addition to the
    .txt files with the source data.

    However, if you can not install either |plotly|_ or |matplotlib|_, then all functions
    of Magnopy are still available. Visualization would be the only missing part.

What is Magnopy?
================

Magnopy is a python code that, given
:ref:`spin Hamiltonian<user-guide_theory-behind_spin-hamiltonian>` in **any**
:ref:`convention <user-guide_theory-behind_convention>` and a
:ref:`vacuum state <user-guide_theory-behind_vacuum-state>`, computes bosonic (magnon)
Hamiltonian of the form

.. include:: core-formulas/bosonic-hamiltonian.inc

where

* :math:`E^{(0)}` is a classical energy of the vacuum state;
* :math:`E^{(2)}` is a quantum correction to the energy of the vacuum state that arises at
  the level of linear spin wave theory (LSWT);
* :math:`\omega_{\alpha}(\boldsymbol{k})` is magnon dispersion relation derived at the
  level of LSWT;

In addition to the LSWT Hamiltonian, Magnopy is capable of computing full quantum
correction to the classical energy of the vacuum state, :math:`E^{corr}`, while LSWT
only gives a part of it. In other words,

.. math::

  E^{corr}
  =
  E^{(2)}
  +
  \dfrac{1}{2}
  \sum_{\beta}
  \sum_{\boldsymbol{k}}
  \omega_{\beta}(\boldsymbol{k})
  +
  \ldots

and Magnopy can independently compute the left and right hand sides of this equation.


What can it do?
===============

* Computes :ref:`all terms of the magnon Hamiltonian <user-guide_cli_magnopy-lswt>` from
  above.
* Supports :ref:`spin Hamiltonian <user-guide_theory-behind_spin-hamiltonian>` in any
  :ref:`convention <user-guide_theory-behind_convention>`.
* Supports a number of :ref:`physical units <user-guide_usage_units>` both for
  Hamiltonian's parameters and for the output quantities.
* :ref:`Minimizes classical energy <user-guide_cli_optimize-sd>` as a function of the spin
  directions.
* Visualizes spin Hamiltonian (experimental)

How to support Magnopy?
=======================

Magnopy is a relatively young code and we would highly appreciate your support.

* If you use and like Magnopy, please give it a star on `GitHub <https://github.com/magnopy/magnopy>`_.
* Please give feedback on your experience with Magnopy (see :ref:`support` page).
* If you use Magnopy in your research, cite it (see :ref:`cite` page).

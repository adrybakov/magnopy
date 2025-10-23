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

    We recommend to install magnopy with optional dependencies (|plotly|_ and |matplotlib|_)
    whether possible.

    .. code-block:: bash

        pip install "magnopy[visual]"

    Then, magnopy will produce graphical output (.html and .png) files in addition to the
    .txt output with the actual data.

    Note that if you can not install either |plotly|_ or |matplotlib|_, then all functions
    of magnopy are still available to you. The only missing part would be the
    visualization.

What is magnopy?
================

Magnopy is a python code that, given
:ref:`spin Hamiltonian<user-guide_theory-behind_spin-hamiltonian>` in **any**
:ref:`convention <user-guide_theory-behind_convention-problem>`, computes bosonic (magnon)
Hamiltonian of the form

.. include:: core-formulas/bosonic-hamiltonian.inc

where

* :math:`E^{(0)}` is a classical energy of the ground state;

Next three terms are derived within the Linear Spin Wave Theory (LSWT):

* :math:`E^{(2)}` is a quantum correction to the ground state energy;
* :math:`\omega_{\alpha}(\boldsymbol{k})` is magnon dispersion at the level of LSWT;
* :math:`\sum_{\boldsymbol{k}}\Delta(\boldsymbol{k})` is an energy measure of
  :math:`\pm \boldsymbol{k}` asymmetry.

What can it do?
===============

* Computes :ref:`all terms of the magnon Hamiltonian <user-guide_cli_magnopy-lswt>` from
  above.
* Supports :ref:`spin Hamiltonian <user-guide_theory-behind_spin-hamiltonian>` in any
  :ref:`convention <user-guide_theory-behind_convention-problem>`.
* Supports a number of :ref:`physical units <user-guide_usage_units>` both for
  Hamiltonian's parameters and for the output quantities.
* :ref:`Minimizes classical energy <user-guide_cli_optimize-sd>` as a function of the spin
  directions.
* Visualizes spin Hamiltonian (experimental)

How to support magnopy?
=======================

Magnopy is a relatively young code and we would highly appreciate your support.

* If you use and like magnopy, please give it a star on `GitHub <https://github.com/magnopy/magnopy>`_.
* Please give feedback on your experience with magnopy (see :ref:`support` page).
* If you use magnopy in your research, please cite it (see :ref:`cite` page).

.. _user-guide_theory-behind_convention:

*****************************
Convention of the Hamiltonian
*****************************

The convention of the Hamiltonian, i. e. the question of how the Hamiltonian is written
is very important as the interaction parameters of the same Hamiltonian can have different
values in different conventions.

We describe the general approach to the convention of the Hamiltonian in the supplementary
note 2 of the |paper-2026|_ and in this page briefly summarize how the convention of the
Hamiltonian is reflected in the code.

The general idea in Magnopy is not to give preference to any convention and support
as many conventions as possible. In that way, the user is responsible for choosing
the convention at the beginning of calculation and Magnopy does all the necessary grunt
work of converting between different conventions if needed. If the Hamiltonian is read
from the know source (i.e. |TB2J|_, |GROGU|_), the convention is known and set
automatically.

Before reading about the convention we recommend to take a look at how the Hamiltonian is
written: :ref:`user-guide_theory-behind_spin-hamiltonian`.

Constants before the sum
========================

First property that defines the convention of the Hamiltonian is the constants that are
written before the sum over the magnetic sites (the popular choices for bilinear term are
:math:`\pm 1` and :math:`\pm \frac{1}{2}`). We expect the user to define either all
or some of eleven constants placed in front of the sum over the magnetic sites for each
group of terms of the Hamiltonian

.. math::
    &C_1
    \\
    &C_{2,1} \qquad
    C_{2,2}
    \\
    &C_{3,1} \qquad
    C_{3,2} \qquad
    C_{3,3}
    \\
    &C_{4,1} \qquad
    C_{4,2} \qquad
    C_{4,3} \qquad
    C_{4,4} \qquad
    C_{4,5}


Normalization of spins
======================

The keyword for this property of convention that you can encounter in the code is
``spin_normalized``.

In magnopy we treat spins as operators. Therefore, the question of normalization of spins
is ill defined. However, the classical version of the quantum spin Hamiltonian can be
written by assuming the spin vectors to be normalized to unit length. Magnopy supports
the parameters that enter that classical version of the Hamiltonian.

If by convention the spins are considered to be "normalized" (``spin_normalized = True``),
then the parameters that user enters are interpreted as

.. math::

    J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2}
    S_{\alpha_1}
    S_{\alpha_2}

If by convention the spins are considered to be "not normalized"
(``spin_normalized = False``), then the parameters that user enters are interpreted as

.. math::
    J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2}

where :math:`S_{\alpha_1}` and :math:`S_{\alpha_2}` are the spin quantum numbers of the
corresponding magnetic sites.


Multiple counting
=================

The keyword for this property of convention that you can encounter in the code is
``multiple_counting``.

For the bilinear parameters that property is known as "double counting". In other words,
whether both parameters :math:`J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2}` and
:math:`J^{i_2, i_1}_{-\nu_2; \alpha_2, \alpha_1}` are included in the summation over the
magnetic sites (``multiple_counting = True``) or only one of them
(``multiple_counting = False``).

The generalization of this property for the higher order terms is not as straightforward
as one would expect and linked with the symmetrization of the interaction parameters that
we discuss at length in the supplementary material of the |paper-2026|_.

The two interaction parameters from the example above form what we call an "equivalent
set" of parameters, as only their sum is relevant for the Hamiltonian and not the
individual values of each of them. For the terms with more than two spin operators, the
equivalent sets can include more than two parameters. The equivalent sets of parameters
for each case of bilinear, trilinear and quadlinear terms, discussed in
:ref:`user-guide_theory-behind_spin-hamiltonian` page, are defined by equations
(S.21)—(S.27) from the supplementary material of the |paper-2026|_.

Symmetrization of parameters
============================

The sum of parameters from the equivalent set can be arbitrary distributed between the
parameters of that set. In Magnopy we assume the parameters to be symmetrized, i.e. the
parameters of the equivalent set to be equal to each other. The user is free to input
non-symmetrized parameters, but Magnopy will symmetrize them right away.

For example, if the user enters :math:`J^{x,y}_{\nu_2; \alpha_1, \alpha_2} = 1` and
:math:`J^{y, x}_{-\nu_2; \alpha_2, \alpha_1} = 2`, Magnopy will symmetrize these
parameters as
:math:`J^{x,y}_{\nu_2; \alpha_1, \alpha_2} = J^{y, x}_{-\nu_2; \alpha_2, \alpha_1} = 1.5`.

More information about the symmetrization can be found in the supplementary
note 3 of the |paper-2026|_.

.. note::
    The symmetrization of the parameters **do not** place any condition on the components
    of the vector/matrix/tensor of each individual parameter. It only connects components
    of the vector/matrix/tensor of **different** parameters. For instance, it **does
    not** forbid an antisymmetric Dzyaloshinskii-Moriya interaction.

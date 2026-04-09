.. _user-guide_theory-behind_convention:

*****************************
Convention of the Hamiltonian
*****************************

The convention of the Hamiltonian, i. e. the question of how the Hamiltonian is written,
is very important as the values of the interaction parameters of the Hamiltonian can be
different in different conventions.

We describe the general approach to the convention of the Hamiltonian in the supplementary
note 2 of the |paper-2026|_ and in this page briefly summarize how the convention of the
Hamiltonian is reflected in the code.

The general idea in Magnopy is to support as many conventions as possible. Therefore,
the user is responsible for choosing the convention while creating a spin Hamiltonian.
Magnopy does all the grunt work of converting between different conventions when
necessary.

.. hint::
    If the Hamiltonian is read from the know source (such as |TB2J|_, |GROGU|_), the
    convention is known and set automatically.

Before reading about convention we recommend to take a look at how the Hamiltonian is
written: :ref:`user-guide_theory-behind_spin-hamiltonian`.

Constants before the sum
========================

*   Keywords of the :py:class:`magnopy.Convention`: ``c1``, ``c21``, ``c22``, ``c31``,
    ``c32``, ``c33``, ``c41``, ``c42``, ``c43``, ``c44``, ``c45``.

First property that defines the convention of the Hamiltonian is the set of constants
being written before the summation sign (the popular choices for bilinear term are
:math:`\pm 1` or :math:`\pm \frac{1}{2}`). We expect the user to define either all or some
of eleven constants placed in front of the summation sign for different types of
Hamiltonian's terms

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

*   Keyword of the :py:class:`magnopy.Convention`: ``spin_normalized``.

In Magnopy we treat spins as operators. Therefore, the question of normalization of spins
is ill defined (one can always write :math:`\hat{S} \rightarrow S \frac{\hat{S}}{S}`,
though). Nevertheless, Magnopy supports the values of the interaction parameters under the
assumption that the spin vectors are normalized to unit length in the classical version of
the quantum spin Hamiltonian.

Let us give an example for the bilinear term of the Hamiltonian:

.. math::
    C_2
    \sum_{\substack{\mu, \nu_2, \\ \alpha_1, \alpha_2, \\ i_1, i_2}}
    J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2}
    S_{\mu, \alpha_1}^{i_1}
    S_{\mu + \nu_2, \alpha_2}^{i_2}

*   If by convention the spins are considered to be "not normalized"
    (``spin_normalized = False``), and user inputs parameters
    :math:`J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2}`, then the Hamiltonian would be
    written as

    .. math::
        C_2
        \sum_{\substack{\mu, \nu_2, \\ \alpha_1, \alpha_2, \\ i_1, i_2}}
        J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2}
        S_{\mu, \alpha_1}^{i_1}
        S_{\mu + \nu_2, \alpha_2}^{i_2}

*   If by convention the spins are considered to be "normalized" (``spin_normalized = True``),
    and user inputs parameters
    :math:`J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2}`, then the Hamiltonian would be
    written as

    .. math::
        C_2
        \sum_{\substack{\mu, \nu_2, \\ \alpha_1, \alpha_2, \\ i_1, i_2}}
        J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2}
        \frac{S_{\mu, \alpha_1}^{i_1}}{S_{\alpha_1}}
        \frac{S_{\mu + \nu_2, \alpha_2}^{i_2}}{S_{\alpha_2}}

where :math:`S_{\alpha_1}` and :math:`S_{\alpha_2}` are the spin quantum numbers of the
spin operators :math:`S_{\mu, \alpha_1}^{i_1}` and :math:`S_{\mu + \nu_2, \alpha_2}^{i_2}`
respectively.

As the Hamiltonian should not change with the change of convention (only the values of the
parameters should), the values of the interaction parameters in these two conventions
are related as

.. math::
    \Biggl(J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2} \Biggr)_{\text{not normalized}}
    =
    \dfrac{1}{S_{\alpha_1} S_{\alpha_2}}
    \Biggl(J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2} \Biggr)_{\text{normalized}}


Multiple counting
=================

*   Keyword of the :py:class:`magnopy.Convention`: ``multiple_counting``.

This property is known as "double counting" in the case of the bilinear terms
(:ref:`ug_tb_sh_2-2`). It specifies, whether both parameters
:math:`J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2}` and
:math:`J^{i_2, i_1}_{-\nu_2; \alpha_2, \alpha_1}` are included in the summation over the
magnetic sites (``multiple_counting = True``) or only one of them
(``multiple_counting = False``). The two interaction parameters from the example above
form what we call an "equivalent set" of parameters, as only their sum is relevant for the
Hamiltonian and not the individual values of each of them.

The generalization of this property for the other terms (with 3 and more components of
spin operators) is not as straightforward as one would expect and is linked with the
symmetrization of the interaction parameters that we discuss at length in the
supplementary note 3 of the |paper-2026|_. For the terms with more than two spin
operators, the equivalent sets can include more than two parameters. The equivalent sets
of parameters for each case of bilinear, trilinear and quadlinear terms, discussed in
:ref:`user-guide_theory-behind_spin-hamiltonian` page, are defined by equations
(S.21)—(S.27) from the supplementary material of the |paper-2026|_.

*   If by convention the multiple counting is allowed (``multiple_counting = True``), then
    the Hamiltonian includes all the parameters from the equivalent set and user is
    expected to manually input each of them.

*   If by convention the multiple counting is not allowed (``multiple_counting = False``),
    then only one of the parameters from the equivalent set is included in the Hamiltonian
    and user is expected to input only that single parameter.


.. hint::
    When ``multiple_counting = True``, one can pass ``populate_equivalent = True`` to the
    :py:meth:`magnopy.SpinHamiltonian.add` method to automatically populate the equivalent
    parameters and avoid the manual input of each of them.

.. _user-guide_theory-behind_convention_symmetrization:

Symmetrization of parameters
============================

The sum of parameters from the equivalent set can be arbitrary distributed between the
parameters of that set. In Magnopy we assume only two types of symmetrization:

*   The parameters of the equivalent set are equal to each other. For example, for the
    bilinear term, we assume that
    :math:`J^{i_1, i_2}_{\nu_2; \alpha_1, \alpha_2} = J^{i_2, i_1}_{-\nu_2; \alpha_2, \alpha_1}`.
    This is the ``multiple_counting = True`` convention.

*   The whole sum is attributed to the single parameter from the equivalent set and
    the rest of the parameters from that set are zero. This is the same as the
    ``multiple_counting = False`` convention.


The user is free to input non-symmetrized parameters, but Magnopy will symmetrize them
right away in most cases.

For example, if ``multiple_counting = True``, and the user enters
:math:`J^{x,y}_{\nu_2; \alpha_1, \alpha_2} = 1` and
:math:`J^{y, x}_{-\nu_2; \alpha_2, \alpha_1} = 2`, Magnopy will symmetrize these
parameters as
:math:`J^{x,y}_{\nu_2; \alpha_1, \alpha_2} = J^{y, x}_{-\nu_2; \alpha_2, \alpha_1} = 1.5`.

More information about the symmetrization can be found in the supplementary
note 3 of the |paper-2026|_.

.. note::
    The symmetrization of the parameters **do not** place any restrictions on the
    components of the vector/matrix/tensor of each individual parameter. It only relates
    components of the vector/matrix/tensor of **different** parameters. For instance, it
    **does not** forbid an antisymmetric Dzyaloshinskii-Moriya interaction.

# ================================== LICENSE ===================================
# Magnopy - Python package for magnons.
# Copyright (C) 2023-2025 Magnopy Team
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


from math import sqrt
import numpy as np

from magnopy import LSWT, Convention, SpinHamiltonian


def test_ferromagnet_one_spin_cubic():
    a = 1
    S = 0.5
    A = 0.3
    B = 0.1
    k = [0.0, 0.0, 0.0]

    atoms = {"names": ["Fe"], "spins": [S], "positions": [[0, 0, 0]]}

    omega_anal = 2 * S * A * sqrt(1 - B / A)

    spinham = SpinHamiltonian(
        cell=[[a, 0, 0], [0, a, 0], [0, 0, a]],
        atoms=atoms,
        convention=Convention(spin_normalized=False, multiple_counting=True, c21=-1),
    )

    spinham.add_21(alpha=0, parameter=np.diag([B, 0.0, A]))

    disp = LSWT(spinham=spinham, spin_directions=[[0, 0, 1]])

    assert disp.M == 1

    assert len(disp._J2) == 1
    assert len(disp._J1) == 1

    assert len(disp.A2) == 1
    assert len(disp.B2) == 1

    assert abs(disp.A(k=k) - (S * A - S * B / 2)) < 1e-8

    assert abs(disp.B(k=k) + S * B / 2) < 1e-8

    assert np.allclose(
        disp.GDM(k=k),
        [
            [S * A - S * B / 2, -S * B / 2],
            [-S * B / 2, S * A - S * B / 2],
        ],
    )
    omega = disp.omega(k=[0.0, 0.0, 0.0])

    assert len(omega) == 1

    omega = omega[0]

    assert abs(omega.imag) < 1e-8

    assert abs(omega.real - omega_anal) < 1e-8

"""Risk spike: check whether ESBMC's Python frontend can verify a 1-qubit
state vector represented as a numpy complex128 array.

This is the highest-risk assumption of the project: that numpy complex
arrays are a usable representation for quantum state vectors under ESBMC.
"""

import numpy as np

state = np.array([1 / np.sqrt(2), 1 / np.sqrt(2)], dtype=np.complex128)

norm_squared = abs(state[0]) ** 2 + abs(state[1]) ** 2

assert abs(norm_squared - 1.0) < 1e-6

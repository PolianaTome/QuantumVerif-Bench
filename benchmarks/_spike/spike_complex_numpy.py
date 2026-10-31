"""Spike de risco: verificar se o front-end Python do ESBMC consegue
verificar um vetor de estado de 1 qubit representado como um array
numpy complex128.

Essa é a suposição de maior risco do projeto: que arrays complexos do numpy
são uma representação utilizável para vetores de estado quântico sob o ESBMC.
"""

import numpy as np

# Um estado normalizado de 1 qubit (|0> + |1>) / sqrt(2), armazenado como um
# array numpy com dtype complexo explícito -- essa é a construção que acabou
# falhando (veja docs/methodology.md, Spike 1): tanto um elemento de array
# não literal quanto o próprio dtype complex128 são rejeitados pelo
# front-end Python do ESBMC.
state = np.array([1 / np.sqrt(2), 1 / np.sqrt(2)], dtype=np.complex128)

# Propriedade sob teste: normalização, a soma dos módulos ao quadrado das
# amplitudes sobre os dois estados de base deve ser igual a 1.
norm_squared = abs(state[0]) ** 2 + abs(state[1]) ** 2

assert abs(norm_squared - 1.0) < 1e-6

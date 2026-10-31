"""Circuito do estado de Bell: H no qubit 0 seguido de CNOT(controle=q0,
alvo=q1), partindo de |00>. Verifica a normalização do estado e as
amplitudes esperadas do par de Bell.

O vetor de estado é representado como duas listas paralelas de floats
(partes real e imaginária), com a base ordenada como índice 0=|00>, 1=|01>,
2=|10>, 3=|11> (veja docs/methodology.md para o motivo de não usar tipos
complex/numpy).
"""

SQRT1_2 = 0.70710678118654752440  # 1 / sqrt(2), constante de normalização da porta Hadamard

# Estado inicial |00>: toda a massa de probabilidade no índice 0, puramente real.
re = [1.0, 0.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0]

# H no qubit 0 age independentemente sobre os pares (|00>,|10>) e (|01>,|11>),
# ou seja, os pares de índice (0,2) e (1,3), já que q0 é o bit de maior ordem
# do índice de 2 qubits (índice = 2*q0 + q1). H = (1/sqrt2) * [[1, 1], [1, -1]]
# aplicada a cada par, com as partes real e imaginária transformadas da mesma forma.
new_re0 = SQRT1_2 * (re[0] + re[2])  # nova amplitude de |00>: (|00> + |10>) / sqrt2
new_re2 = SQRT1_2 * (re[0] - re[2])  # nova amplitude de |10>: (|00> - |10>) / sqrt2
new_im0 = SQRT1_2 * (im[0] + im[2])
new_im2 = SQRT1_2 * (im[0] - im[2])
new_re1 = SQRT1_2 * (re[1] + re[3])  # nova amplitude de |01>: (|01> + |11>) / sqrt2
new_re3 = SQRT1_2 * (re[1] - re[3])  # nova amplitude de |11>: (|01> - |11>) / sqrt2
new_im1 = SQRT1_2 * (im[1] + im[3])
new_im3 = SQRT1_2 * (im[1] - im[3])

# Consolida o vetor de estado pós-H.
re = [new_re0, new_re1, new_re2, new_re3]
im = [new_im0, new_im1, new_im2, new_im3]

# CNOT(controle=q0, alvo=q1): inverte q1 sempre que q0=1, ou seja, troca as
# amplitudes de |10> e |11> (índice 2 e índice 3); os índices 0 e 1
# (ramo q0=0) permanecem intocados.
re[2], re[3] = re[3], re[2]
im[2], im[3] = im[3], im[2]

# Propriedade 1 (normalização): a soma dos módulos ao quadrado das amplitudes
# sobre os 4 estados de base deve ser igual a 1, dentro da tolerância numérica.
norm_sq = 0.0
for i in range(4):
    norm_sq = norm_sq + re[i] * re[i] + im[i] * im[i]
assert abs(norm_sq - 1.0) < 1e-6

# Propriedade 2 (estado de Bell esperado): o circuito acima deve ter produzido
# exatamente (|00> + |11>) / sqrt(2), ou seja, amplitude +1/sqrt2 em |00> e
# |11>, amplitude zero em |01> e |10>, todas puramente reais.
assert abs(re[0] - SQRT1_2) < 1e-6  # amplitude de |00> é +1/sqrt2
assert abs(im[0]) < 1e-6            # ...e não tem parte imaginária
assert abs(re[1]) < 1e-6            # amplitude de |01> se anula
assert abs(im[1]) < 1e-6
assert abs(re[2]) < 1e-6            # amplitude de |10> se anula
assert abs(im[2]) < 1e-6
assert abs(re[3] - SQRT1_2) < 1e-6  # amplitude de |11> é +1/sqrt2
assert abs(im[3]) < 1e-6            # ...e não tem parte imaginária

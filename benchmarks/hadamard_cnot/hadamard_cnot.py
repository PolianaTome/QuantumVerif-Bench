"""Sequência de portas H e CNOT em 2 qubits, partindo de |00>, verificando
que o estado permanece normalizado (consistência unitária) após CADA
operação individual, não apenas ao final.

Vetor de estado: duas listas paralelas de floats (partes real, imaginária),
com a base ordenada como índice 0=|00>, 1=|01>, 2=|10>, 3=|11> (primeiro
dígito q0, segundo dígito q1). Veja docs/methodology.md para o motivo dessa
representação em vez de numpy/complex.
"""

SQRT1_2 = 0.70710678118654752440  # 1 / sqrt(2), constante de normalização da porta Hadamard


def check_norm(re, im):
    """Propriedade: a soma dos módulos ao quadrado das amplitudes sobre os 4
    estados de base deve ser igual a 1, dentro da tolerância numérica.
    Chamada após cada porta abaixo, não só ao final, para verificar a
    consistência unitária passo a passo."""
    norm_sq = 0.0
    for i in range(4):
        norm_sq = norm_sq + re[i] * re[i] + im[i] * im[i]
    assert abs(norm_sq - 1.0) < 1e-6


# Estado inicial |00>: toda a massa de probabilidade no índice 0, puramente real.
re = [1.0, 0.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0]
check_norm(re, im)

# H em q0 (mistura os pares de índice (0,2) e (1,3), já que q0 é o bit de
# maior ordem do índice de 2 qubits). H = (1/sqrt2) * [[1, 1], [1, -1]] por par.
r0 = SQRT1_2 * (re[0] + re[2])
r2 = SQRT1_2 * (re[0] - re[2])
r1 = SQRT1_2 * (re[1] + re[3])
r3 = SQRT1_2 * (re[1] - re[3])
i0 = SQRT1_2 * (im[0] + im[2])
i2 = SQRT1_2 * (im[0] - im[2])
i1 = SQRT1_2 * (im[1] + im[3])
i3 = SQRT1_2 * (im[1] - im[3])
re = [r0, r1, r2, r3]
im = [i0, i1, i2, i3]
check_norm(re, im)

# H em q1 (mistura os pares de índice (0,1) e (2,3), já que q1 é o bit de
# menor ordem do índice de 2 qubits).
r0 = SQRT1_2 * (re[0] + re[1])
r1 = SQRT1_2 * (re[0] - re[1])
r2 = SQRT1_2 * (re[2] + re[3])
r3 = SQRT1_2 * (re[2] - re[3])
i0 = SQRT1_2 * (im[0] + im[1])
i1 = SQRT1_2 * (im[0] - im[1])
i2 = SQRT1_2 * (im[2] + im[3])
i3 = SQRT1_2 * (im[2] - im[3])
re = [r0, r1, r2, r3]
im = [i0, i1, i2, i3]
check_norm(re, im)

# CNOT(controle=q0, alvo=q1): inverte q1 sempre que q0=1, ou seja, troca as
# amplitudes de |10> e |11> (índice 2 e índice 3).
re[2], re[3] = re[3], re[2]
im[2], im[3] = im[3], im[2]
check_norm(re, im)

# H em q0 novamente (mesma transformação do primeiro H em q0 acima).
r0 = SQRT1_2 * (re[0] + re[2])
r2 = SQRT1_2 * (re[0] - re[2])
r1 = SQRT1_2 * (re[1] + re[3])
r3 = SQRT1_2 * (re[1] - re[3])
i0 = SQRT1_2 * (im[0] + im[2])
i2 = SQRT1_2 * (im[0] - im[2])
i1 = SQRT1_2 * (im[1] + im[3])
i3 = SQRT1_2 * (im[1] - im[3])
re = [r0, r1, r2, r3]
im = [i0, i1, i2, i3]
check_norm(re, im)

# CNOT(controle=q1, alvo=q0): inverte q0 sempre que q1=1, ou seja, troca as
# amplitudes de |01> e |11> (índice 1 e índice 3) -- os papéis de
# controle/alvo estão invertidos em relação ao CNOT acima.
re[1], re[3] = re[3], re[1]
im[1], im[3] = im[3], im[1]
check_norm(re, im)

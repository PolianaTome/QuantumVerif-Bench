"""Algoritmo de Deutsch em um único qubit de entrada (q0, "x") e um qubit
ancilla (q1, "y"), usando o circuito padrão H - Uf - H. nondet_bool() escolhe
entre um oráculo constante (f(x) = 0) e um oráculo balanceado (f(x) = x), e o
benchmark verifica que o algoritmo mede deterministicamente q0 = 0 no caso
constante e q0 = 1 no caso balanceado, em uma única consulta.

Vetor de estado: duas listas paralelas de floats (partes real, imaginária),
com a base ordenada como índice 0=|00>, 1=|01>, 2=|10>, 3=|11> (primeiro
dígito q0, segundo dígito q1). Veja docs/methodology.md para o motivo dessa
representação em vez de numpy/complex.
"""

SQRT1_2 = 0.70710678118654752440  # 1 / sqrt(2), constante de normalização da porta Hadamard

# nondet_bool() é um intrínseco do front-end Python do ESBMC: faz o
# verificador explorar AMBOS os ramos (True e False) simbolicamente, então
# essa única execução prova o algoritmo correto para os dois tipos de
# oráculo, não apenas para um caso amostrado.
is_balanced = nondet_bool()

# Estado inicial |0>_x |1>_y = |01> = índice 1 (q1 é preparado em |1> para que
# o truque de phase-kickback do algoritmo de Deutsch funcione).
re = [0.0, 1.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0]

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

# Oráculo Uf: |x,y> -> |x, y XOR f(x)>.
# Oráculo constante f(x) = 0: y nunca é invertido, então Uf é a identidade aqui.
# Oráculo balanceado f(x) = x: y só é invertido quando x = 1, ou seja, troca
# as amplitudes de |10> e |11> (índice 2 e índice 3) e deixa as amplitudes
# com x=0 (índice 0, 1) intocadas.
if is_balanced:
    re[2], re[3] = re[3], re[2]
    im[2], im[3] = im[3], im[2]

# H em q0 novamente (mesma transformação do primeiro H em q0 acima): é isso
# que converte o phase-kickback do oráculo em um resultado de medição
# determinístico.
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

# Massa de probabilidade em q0 = 0 (índices 0,1, ou seja, |0y>) versus q0 = 1
# (índices 2,3, ou seja, |1y>) -- é isso que "medir q0" colapsa.
prob_q0_0 = re[0] * re[0] + im[0] * im[0] + re[1] * re[1] + im[1] * im[1]
prob_q0_1 = re[2] * re[2] + im[2] * im[2] + re[3] * re[3] + im[3] * im[3]

# Propriedade: o algoritmo de Deutsch deve ser totalmente determinístico em
# uma única consulta -- para o oráculo balanceado, TODA a massa de
# probabilidade deve estar em q0=1 (prob_q0_0 ~ 0); para o oráculo
# constante, TODA a massa deve estar em q0=0.
if is_balanced:
    expected_bit = 1
    assert prob_q0_0 < 1e-6
else:
    expected_bit = 0
    assert prob_q0_1 < 1e-6

# Medição simulada: como o algoritmo é determinístico, o lado que concentra
# mais da metade da massa de probabilidade é o resultado de fato.
if prob_q0_1 > 0.5:
    measured_bit = 1
else:
    measured_bit = 0

# Propriedade: a medição simulada deve concordar com a expectativa derivada
# do oráculo, tanto no ramo constante quanto no balanceado.
assert measured_bit == expected_bit

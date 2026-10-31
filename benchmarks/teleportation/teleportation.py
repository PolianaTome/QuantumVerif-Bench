"""Protocolo de teleportação quântica com 3 qubits: q0 guarda o estado de
entrada arbitrário de Alice (alpha|0> + beta|1>), q1 e q2 compartilham um
par de Bell (Alice fica com q1, Bob fica com q2). Alice aplica CNOT(q0,q1) e
H(q0), depois mede q0 e q1, enviando os dois bits clássicos (m0, m1) para
Bob. Bob aplica uma correção (X se m1, depois Z se m0) em q2. O benchmark
garante que o qubit final de Bob é igual ao original de Alice (alpha, beta),
para cada um dos quatro resultados clássicos possíveis e para todo estado de
entrada real normalizado.

Simplificação: alpha e beta são tomados como reais (im = 0), o que mantém
todas as amplitudes deste benchmark com valor real. Uma entrada simbólica
(nondet_float() mais __ESBMC_assume() normalizando) foi tentada primeiro,
mas tornou a resolução em ponto flutuante do Z3 intratável (sem resultado
após minutos, em 302 VCCs); em vez disso, usa-se um estado de entrada fixo,
não trivial e normalizado (alpha, beta), enquanto nondet_bool() continua
explorando os quatro resultados de medição clássica (m0, m1) e suas
correções. Veja docs/methodology.md.
Ordem da base para o estado de 3 qubits: índice = 4*q0 + 2*q1 + q2.
"""

SQRT1_2 = 0.70710678118654752440  # 1 / sqrt(2), constante de normalização da Hadamard/par de Bell

# Qubit de entrada fixo de Alice: alpha^2 + beta^2 = 0.36 + 0.64 = 1, então o
# estado já está normalizado (0.6 = 3/5, 0.8 = 4/5, um par pitagórico).
alpha = 0.6
beta = 0.8

# Estado inicial de 3 qubits: q0 = alpha|0> + beta|1>, (q1,q2) = par de Bell
# (|00> + |11>) / sqrt2. Apenas 4 das 8 amplitudes de base são não nulas:
# |000>, |011> (de q0=0 combinado com cada termo de Bell) e |100>, |111>
# (de q0=1 combinado com cada termo de Bell).
amp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
amp[0] = alpha * SQRT1_2  # |000> = q0=0, (q1,q2)=00
amp[3] = alpha * SQRT1_2  # |011> = q0=0, (q1,q2)=11
amp[4] = beta * SQRT1_2   # |100> = q0=1, (q1,q2)=00
amp[7] = beta * SQRT1_2   # |111> = q0=1, (q1,q2)=11

# CNOT(controle=q0, alvo=q1): inverte q1 sempre que q0=1, ou seja, troca
# |100><->|110> (índice 4<->6) e |101><->|111> (índice 5<->7). Os índices com
# q0=0 (0-3) permanecem intocados, pois o bit de controle é 0 ali.
amp[4], amp[6] = amp[6], amp[4]
amp[5], amp[7] = amp[7], amp[5]

# H em q0: mistura os pares de índice (i, i+4) para i em range(4), já que q0
# é o bit de maior ordem do índice de 3 qubits (índice = 4*q0 + 2*q1 + q2).
# H = (1/sqrt2) * [[1, 1], [1, -1]] aplicada a cada par (i, i+4).
new_amp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
for i in range(4):
    new_amp[i] = SQRT1_2 * (amp[i] + amp[i + 4])      # ramo q0=0 após H
    new_amp[i + 4] = SQRT1_2 * (amp[i] - amp[i + 4])  # ramo q0=1 após H
amp = new_amp

# Alice mede q0, q1 e envia os dois bits clássicos (m0, m1) para Bob.
# nondet_bool() faz o ESBMC explorar simbolicamente as quatro combinações,
# então essa única execução prova o protocolo correto para todo resultado
# possível, não apenas para um par de resultados de medição amostrado.
m0 = nondet_bool()
m1 = nondet_bool()

# Par de amplitudes do qubit de Bob (q2) para o ramo selecionado por (m0, m1):
# cada par (bob0, bob1) guarda a amplitude de q2 para q2=0 e q2=1
# respectivamente, condicionada ao resultado da medição clássica de Alice.
if m0 and m1:
    bob0 = amp[6]  # |110>
    bob1 = amp[7]  # |111>
elif m0 and (not m1):
    bob0 = amp[4]  # |100>
    bob1 = amp[5]  # |101>
elif (not m0) and m1:
    bob0 = amp[2]  # |010>
    bob1 = amp[3]  # |011>
else:
    bob0 = amp[0]  # |000>
    bob1 = amp[1]  # |001>

# Correção de Bob, guiada pelos bits clássicos de Alice: aplica X (inversão
# de bit) se m1 estiver ativo, depois Z (inversão de fase em |1>) se m0
# estiver ativo.
if m1:
    bob0, bob1 = bob1, bob0  # X: troca as amplitudes de |0> e |1>
if m0:
    bob1 = -bob1              # Z: inverte o sinal da amplitude de |1>

# Cada um dos quatro ramos acima seleciona uma fatia do estado completo cujo
# módulo ao quadrado é exatamente 1/4 sempre que alpha^2 + beta^2 = 1 (já que
# os outros 3 ramos carregam igualmente os 3/4 restantes da massa de
# probabilidade); renormalizar esse ramo de volta a um estado de 1 qubit
# válido significa multiplicar as amplitudes por 2 (já que 1/sqrt(1/4) = 2).
final0 = bob0 * 2.0
final1 = bob1 * 2.0

# Propriedade: após a correção de Bob e a renormalização, o qubit dele deve
# ser igual ao estado original de Alice (alpha, beta) -- para cada um dos 4
# ramos explorados via nondet_bool() acima.
assert abs(final0 - alpha) < 1e-4
assert abs(final1 - beta) < 1e-4

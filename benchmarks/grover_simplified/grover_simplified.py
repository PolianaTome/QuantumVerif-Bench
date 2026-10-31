"""Busca de Grover simplificada em 3 qubits (N=8 estados de base), buscando
um único item marcado com 2 iterações de Grover (próximo do ótimo
round(pi/4 * sqrt(8)) = 2 iterações para N=8). Verifica que a amplitude do
item marcado cresce estritamente a cada iteração, que o estado permanece
normalizado, e que a amplitude após 2 iterações bate com o valor exato em
forma fechada para este caso.

As amplitudes de estado são uma única lista de floats (todas com valor real
aqui, já que a inversão de fase do oráculo e o operador de difusão usados
são reais; veja docs/methodology.md para a decisão de representação). A
ordem da base é o índice simples 0..7 do estado de base computacional de
3 qubits.
"""

SQRT1_8 = 0.35355339059327376220  # 1 / sqrt(8), a amplitude da superposição uniforme para N=8

N = 8
# O item marcado é o índice 3 (um índice literal; veja docs/methodology.md
# para uma limitação separada do front-end que este benchmark encontrou com
# `amp[i] = -amp[i]`).

# Estado inicial: superposição uniforme sobre os 8 estados de base, como
# produzida ao aplicar H em cada um dos 3 qubits partindo de |000>.
amp = [SQRT1_8, SQRT1_8, SQRT1_8, SQRT1_8, SQRT1_8, SQRT1_8, SQRT1_8, SQRT1_8]

# Registrado antes de qualquer iteração, usado abaixo para provar que a
# amplitude marcada cresce estritamente após cada iteração de Grover.
initial_marked_amp = amp[3]

# --- Iteração 1 de Grover: oráculo (inversão de fase no item marcado) e
# depois difusão (inversão em torno da média). ---

# Oráculo: inverte o sinal apenas da amplitude do item marcado, deixando
# todas as outras amplitudes intocadas. `amp[3] = -amp[3]` falha na
# inferência de tipos do ESBMC ao negar um elemento de lista in-place;
# `0.0 - amp[3]` é usado no lugar (veja docs/methodology.md).
amp[3] = 0.0 - amp[3]

# Passo 1 do operador de difusão: calcula a média das amplitudes sobre todos
# os N estados (pós-oráculo), necessária para a reflexão de "inversão em
# torno da média" abaixo.
mean = 0.0
for i in range(N):
    mean = mean + amp[i]
mean = mean / N

# Passo 2 do operador de difusão: reflete cada amplitude em torno da média
# (amp[i] -> 2*mean - amp[i]). Como a amplitude do item marcado foi invertida
# para negativa pelo oráculo, essa reflexão a amplifica, enquanto as
# amplitudes dos itens não marcados encolhem ligeiramente.
new_amp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
for i in range(N):
    new_amp[i] = 2.0 * mean - amp[i]
amp = new_amp

# Propriedade: a amplitude do item marcado deve ter crescido após a iteração 1.
amp_after_iter1 = amp[3]
assert amp_after_iter1 > initial_marked_amp

# --- Iteração 2 de Grover: os mesmos passos de oráculo + difusão da iteração 1. ---
amp[3] = 0.0 - amp[3]

mean = 0.0
for i in range(N):
    mean = mean + amp[i]
mean = mean / N

new_amp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
for i in range(N):
    new_amp[i] = 2.0 * mean - amp[i]
amp = new_amp

# Propriedade: a amplitude do item marcado deve ter crescido ainda mais após
# a iteração 2 (crescimento monótono nessas 2 primeiras iterações, próximas
# do ótimo).
amp_after_iter2 = amp[3]
assert amp_after_iter2 > amp_after_iter1

# Propriedade: o operador de Grover (oráculo + difusão) é unitário, então o
# estado deve continuar normalizado após as duas iterações.
norm_sq = 0.0
for i in range(N):
    norm_sq = norm_sq + amp[i] * amp[i]
assert abs(norm_sq - 1.0) < 1e-6

# Propriedade: a amplitude do item marcado após exatamente 2 iterações deve
# bater com o valor exato em forma fechada para este caso de N=8 com um
# único item marcado (uma previsão numérica precisa, não apenas "algum" crescimento).
expected = 11.0 * SQRT1_8 / 4.0
assert abs(amp_after_iter2 - expected) < 1e-6

"""Spike de risco: verificar se uma lista simples do Python com floats
(usada para guardar as partes real/imaginária de um vetor de estado com
várias amplitudes) é suportada pelo front-end Python do ESBMC."""

# Um estado com 4 amplitudes (equivalente a 2 qubits), cada amplitude
# dividida em partes real e imaginária guardadas em duas listas paralelas --
# essa é a representação que escala a ideia de par (re, im) de floats de
# spike_float_pair.py para múltiplas amplitudes, indexada com um loop
# `for i in range(N)`.
state_re = [0.5, 0.5, 0.5, 0.5]
state_im = [0.0, 0.0, 0.0, 0.0]

# Propriedade sob teste: normalização, somada via um loop sobre as 4
# amplitudes em vez de escrita manualmente -- confirma que tanto a
# indexação de lista quanto o unwind de loop funcionam sob o front-end
# Python do ESBMC (veja docs/methodology.md, Spike 4).
norm_squared = 0.0
for i in range(4):
    norm_squared = norm_squared + state_re[i] * state_re[i] + state_im[i] * state_im[i]

assert abs(norm_squared - 1.0) < 1e-4

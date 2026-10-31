"""Spike de risco: checagem de sanidade de que o ESBMC reporta um
contraexemplo quando a asserção de normalização é de fato violada (estado
não normalizado)."""

# Amplitudes deliberadamente não normalizadas: 0.9^2 + 0.9^2 = 1.62 != 1,
# então a asserção abaixo deve falhar. Isso confirma que o front-end Python
# do ESBMC tanto verifica QUANTO refuta corretamente a representação em par
# (re, im) de floats (veja docs/methodology.md, Spike 3) -- ou seja, que o
# contraexemplo que ele produz tem a estrutura que
# scripts/collect_counterexamples.py precisa analisar.
a_re = 0.9
a_im = 0.0
b_re = 0.9
b_im = 0.0

# Mesma checagem de normalização de spike_float_pair.py, esperada para FALHAR aqui.
norm_squared = (a_re * a_re + a_im * a_im) + (b_re * b_re + b_im * b_im)

assert abs(norm_squared - 1.0) < 1e-4

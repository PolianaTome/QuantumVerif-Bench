"""Spike de risco: verificar se o front-end Python do ESBMC suporta o tipo
complex nativo do Python como representação para amplitudes quânticas."""

# Duas amplitudes de um estado normalizado de 1 qubit, usando o tipo
# `complex` embutido em vez do numpy. O parsing disso funciona (diferente de
# spike_complex_numpy.py), mas chamar abs() em um valor complex abaixo é o
# que acaba sendo inviável: passa pelo modelo interno de libm exp/expm1 do
# ESBMC, que nunca chega a um ponto fixo dentro de um limite de unwind
# razoável (veja docs/methodology.md, Spike 2).
a = complex(0.70710678, 0.0)
b = complex(0.70710678, 0.0)

# Propriedade sob teste: normalização, a soma dos módulos ao quadrado das
# duas amplitudes deve ser igual a 1. Esta é a linha cuja chamada abs() não
# termina em tempo prático sob o ESBMC.
norm_squared = abs(a) ** 2 + abs(b) ** 2

assert abs(norm_squared - 1.0) < 1e-4

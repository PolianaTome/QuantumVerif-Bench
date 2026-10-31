"""Spike de risco: representar uma amplitude quântica como um par manual
(real, imaginário) de floats, em vez de numpy complex128 ou complex nativo
do Python."""

# Amplitude a = 1/sqrt2 + 0i, dividida manualmente em partes real e
# imaginária em vez de usar um valor com tipo complex.
a_re = 0.70710678
a_im = 0.0
# Amplitude b = 1/sqrt2 + 0i, mesma representação.
b_re = 0.70710678
b_im = 0.0

# Propriedade sob teste: normalização. |a|^2 = a_re^2 + a_im^2 (e o mesmo
# para b) é calculado diretamente a partir das partes real/imaginária, sem
# nenhum tipo complex ou chamada abs() envolvida -- essa é a representação
# que funcionou (veja docs/methodology.md, Spike 3): VERIFICATION
# SUCCESSFUL em ~2,5s.
norm_squared = (a_re * a_re + a_im * a_im) + (b_re * b_re + b_im * b_im)

assert abs(norm_squared - 1.0) < 1e-4

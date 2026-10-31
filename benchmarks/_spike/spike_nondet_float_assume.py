"""Spike de risco: verificar o suporte a nondet_float() e __ESBMC_assume(),
necessários para verificar a teleportação com um estado de entrada
simbólico (arbitrário)."""

# nondet_float() cria um valor float totalmente simbólico (não um valor
# sorteado aleatoriamente de um intervalo, mas um que o ESBMC precisa provar
# a propriedade para qualquer valor possível). a e b representam as partes
# real/imaginária (ou, aqui, os dois componentes reais de amplitude) de um
# estado arbitrário de 1 qubit.
a = nondet_float()
b = nondet_float()

# __ESBMC_assume() restringe o espaço de busca simbólico: considera apenas
# pares (a, b) normalizados, dentro de uma pequena margem de tolerância, em
# vez de todo valor float possível.
__ESBMC_assume(a * a + b * b > 1.0 - 1e-6)
__ESBMC_assume(a * a + b * b < 1.0 + 1e-6)

# Propriedade sob teste: dada a suposição acima, a norma deve de fato ser
# (aproximadamente) 1 para qualquer a, b que o ESBMC escolher. Essa
# combinação faz parsing e verifica para este exemplo pequeno, mas tornar o
# qubit de entrada de teleportation.py totalmente simbólico dessa forma
# tornou a resolução em ponto flutuante do Z3 intratável na prática (veja
# docs/methodology.md) -- teleportation.py usa um estado de entrada
# concreto e fixo em vez disso, por esse motivo.
norm_sq = a * a + b * b
assert abs(norm_sq - 1.0) < 1e-5

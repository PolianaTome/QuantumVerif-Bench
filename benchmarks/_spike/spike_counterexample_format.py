"""Spike de risco: inspecionar o formato completo do rastro [Counterexample]
que o ESBMC produz quando uma variável nondet está envolvida, para
projetar collect_counterexamples.py."""

# Um inteiro simbólico, restrito ao intervalo 1..9 via __ESBMC_assume().
x = nondet_int()
__ESBMC_assume(x > 0)
__ESBMC_assume(x < 10)

# Deliberadamente insatisfazível para qualquer x nesse intervalo: essa
# asserção deve FALHAR para todo valor possível, que é o objetivo -- isso
# força o ESBMC a emitir um rastro [Counterexample] (com o x concreto que
# escolheu) contra o qual as expressões regulares de
# scripts/collect_counterexamples.py foram projetadas.
assert x > 100

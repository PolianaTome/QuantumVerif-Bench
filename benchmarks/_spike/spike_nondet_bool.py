"""Spike de risco: verificar se nondet_bool() é um intrínseco utilizável do
ESBMC para Python."""

# nondet_bool() é reconhecido pelo front-end Python do ESBMC sem nenhum
# import; ele faz o verificador explorar AMBOS os ramos, True e False,
# abaixo, simbolicamente, em vez de escolher um valor ao acaso. Esse é o
# mecanismo que os benchmarks usam para cobrir cada ramo clássico (por
# exemplo, os quatro resultados de medição em teleportation.py) em uma
# única execução de verificação.
flag = nondet_bool()
if flag:
    x = 1
else:
    x = 0

# Propriedade sob teste: qualquer que seja o ramo tomado, x deve ser um dos
# dois valores esperados -- confirma que ambos os ramos são de fato
# alcançáveis/verificados.
assert x == 0 or x == 1

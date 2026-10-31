"""Spike de risco: verificar se o front-end Python do ESBMC suporta negar um
elemento de lista in-place. A negação unária direta (amp[i] = -amp[i])
falhou com um erro de inferência de tipos; este spike testa o contorno
0.0 - amp[i] no lugar."""

amp = [1.0, 2.0, 3.0]
# Contorno para a limitação do front-end: `amp[0] = -amp[0]` falha com
# "ERROR: Type inference failed for Assign" mesmo com um índice literal;
# reescrever a negação unária como uma subtração binária a partir de 0.0
# evita o problema e é usado em grover_simplified.py sempre que é preciso
# inverter o sinal de uma amplitude in-place.
amp[0] = 0.0 - amp[0]

assert amp[0] == -1.0

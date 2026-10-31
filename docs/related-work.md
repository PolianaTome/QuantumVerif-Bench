# Related Work

| Trabalho | Foco | Técnica | Tipo | Detecta bugs? |
|---|---|---|---|---|
| Huang & Martonosi (ISCA 2019) | Assertions estatísticas | Projetor de estado | Dinâmica | Parcial |
| Paltenghi & Pradel (OOPSLA 2022) | Estudo empírico de 223 bugs reais | Análise manual/estatística | Manual | Sim |
| Perdrix & Valiron | Sistema de tipos | Tipos | Estática | Não |
| Quetschlich & Di Matteo (Computing, Springer, 2025; arXiv:2509.03280) | Taxonomia de 14 bugs quânticos | Experiência + análise de repositórios | Manual | Sim |
| symQV (Bauer-Marquart et al., FM 2023; arXiv:2212.02267) | Teleportação, QFT, QPE, difusão de Grover | SMT (Z3 + dReal) | Formal/Simbólica | Sim |
| AutoQ 2.0 | Circuitos/programas (incl. Grover c/ medição fraca) | Autômatos | Formal | Sim |
| QSynth | Síntese (não verificação) de 10 programas unitários | SMT (Z3) | Formal/Síntese | N/A |
| QuantumVerif-Bench (este projeto) | Suíte de benchmarks + taxonomia + verificação | ESBMC (SMT/SBMC) | Formal/SBMC | Sim |

## Correções em relação à proposta original do PIBITI

A proposta original do PIBITI cita, na referência [7], "Jiang, L. et al." para o
trabalho sobre taxonomia de 14 bugs quânticos. Esse nome está incorreto: os autores
corretos são **Quetschlich e Di Matteo** (Computing, Springer, 2025; arXiv:2509.03280),
como listado na tabela acima. A referência [9] da proposta cita "Liu, J. et al." para
o estudo empírico de 223 bugs reais; esse nome também está incorreto — os autores
corretos são **Paltenghi e (muito provavelmente) Pradel** (OOPSLA 2022). Esta seção
serve como nota de correção para quem revisar a proposta original posteriormente; os
nomes corretos são usados em toda a documentação nova deste repositório.

## Discussão

Verificação formal automatizada de programas quânticos via SMT não é, isoladamente,
uma contribuição inédita — symQV e AutoQ 2.0 já fazem exatamente isso, com foco em
circuitos como teleportação, QFT, QPE e a difusão de Grover (symQV) ou autômatos sobre
circuitos e programas, incluindo Grover com medição fraca (AutoQ 2.0). QSynth ocupa um
nicho relacionado mas distinto: síntese, não verificação, de programas unitários via
SMT.

O ineditismo real deste projeto está em outro lugar: usar uma ferramenta de propósito
geral e já madura — o ESBMC, competitiva em SV-COMP e Test-COMP — que verifica Python
diretamente, e não uma DSL de circuitos quânticos feita sob medida como as usadas por
symQV ou AutoQ 2.0. Isso significa que o mesmo processo de verificação que checa
propriedades de estado quântico (normalização, consistência unitária, validade de
medições) também detecta, sem nenhum mecanismo adicional, bugs de software convencional
no mesmo código — divisão por zero, índice fora dos limites, tipo incorreto. Nenhuma das
ferramentas formais citadas (symQV, AutoQ 2.0, QSynth) oferece essa combinação, porque
todas operam sobre uma representação de circuito e não sobre código Python de uso geral.

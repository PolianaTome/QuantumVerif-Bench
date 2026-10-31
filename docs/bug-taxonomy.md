# Bug Taxonomy

## Categorias operacionais deste projeto

QuantumVerif-Bench organiza as propriedades verificadas em três categorias
operacionais, usadas consistentemente nos 5 benchmarks (ver os respectivos
`properties.md`):

1. **Normalização de estados** — a soma dos módulos ao quadrado das amplitudes de
   um vetor de estado deve ser 1 (dentro de tolerância numérica). Verificada em
   `bell`, `deutsch`, `teleportation`, `hadamard_cnot` e `grover_simplified`.
2. **Consistência de operações unitárias** — cada operação (gate) aplicada a um
   estado deve preservar sua norma, e deve produzir exatamente a transformação
   algébrica esperada (não apenas "alguma" transformação normalizada).
   Verificada explicitamente passo a passo em `hadamard_cnot`, e implicitamente em
   todos os demais benchmarks via os asserts de amplitude esperada.
3. **Medições inválidas** — o resultado de uma medição (ou de uma correção
   condicionada a uma medição, como em `teleportation`) deve ser consistente com a
   amplitude real do estado antes da medição, cobrindo todos os desfechos
   possíveis. Verificada em `deutsch` (bit medido corresponde ao oráculo simulado)
   e em `teleportation` (estado final de Bob após correção condicional).

## Mapeamento para a taxonomia de Quetschlich & Di Matteo (arXiv:2509.03280)

> **PENDENTE DE VERIFICAÇÃO** — Quetschlich & Di Matteo (Computing, Springer, 2025;
> arXiv:2509.03280) propõem uma taxonomia de 14 categorias de bugs quânticos. Não
> tenho confiança suficiente no conteúdo detalhado dessa taxonomia (artigo publicado
> em setembro de 2025, cujos 14 nomes de categoria não foram fornecidos nesta
> conversa) para listar as 14 categorias e mapear cada uma das 3 categorias
> operacionais acima para seus nomes exatos sem risco de inventar rótulos que não
> correspondem ao artigo real. Esta seção deve ser completada consultando o PDF do
> artigo diretamente. A tabela abaixo é a estrutura a preencher — a coluna
> "Categoria (Quetschlich & Di Matteo)" está com placeholders `[TODO: confirmar no artigo]`
> que precisam ser substituídos pelos nomes exatos das categorias do artigo antes
> deste documento ser considerado final.

| Categoria operacional (este projeto) | Categoria(s) correspondente(s) (Quetschlich & Di Matteo, arXiv:2509.03280) |
|---|---|
| Normalização de estados | `[TODO: confirmar no artigo]` |
| Consistência de operações unitárias | `[TODO: confirmar no artigo]` |
| Medições inválidas | `[TODO: confirmar no artigo]` |

Ao preencher esta tabela, vale registrar também quais das 14 categorias do artigo
**não** têm correspondência em nenhum dos 3 benchmarks atuais (por exemplo, bugs de
natureza puramente sintática/de tipo em SDKs específicos, que não fariam sentido no
front-end Python do ESBMC), para deixar explícito o que a suíte atual cobre e o que
fica como trabalho futuro.

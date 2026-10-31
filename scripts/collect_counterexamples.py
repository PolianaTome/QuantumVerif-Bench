#!/usr/bin/env python3
"""Analisa os logs de verificação do ESBMC em results/ e produz um resumo
JSON estruturado dos contraexemplos (objetivo 2 do projeto
QuantumVerif-Bench): qual benchmark falhou, qual propriedade foi violada, e
quais valores o contraexemplo atribuiu a cada variável ao longo do rastro.
"""

import argparse
import json
import re
from pathlib import Path

# Reconhece uma linha de cabeçalho "State N file ... line ... column ...
# thread ..." do ESBMC, que precede um bloco de atribuições de variáveis em
# um rastro de contraexemplo. Os grupos capturados não são usados hoje, mas
# são mantidos para uma futura análise ciente do rastro (por exemplo,
# atribuir um valor ao passo que o produziu).
STATE_HEADER_RE = re.compile(r"^State \d+ file (\S+) line (\d+) column (\d+) thread \d+$")
# Reconhece uma linha de atribuição "  nome = valor" dentro de um rastro de
# contraexemplo, opcionalmente seguida de um padrão de bits entre parênteses
# (ex.: "(0 1 1 0 ...)") que o ESBMC acrescenta para alguns tipos -- o
# próprio padrão de bits é descartado.
ASSIGNMENT_RE = re.compile(r"^\s{2}(?P<name>[A-Za-z_][A-Za-z0-9_\[\]]*)\s*=\s*(?P<value>.+?)\s*(\([01 ]+\))?$")
# Marca o início do bloco "Violated property:" em um log de falha do ESBMC.
VIOLATED_PROPERTY_HEADER_RE = re.compile(r"^Violated property:$")
# Dentro do bloco de propriedade violada: o arquivo/linha/coluna de origem
# da asserção que falhou.
PROPERTY_LOCATION_RE = re.compile(r"^\s*file (?P<file>\S+) line (?P<line>\d+) column (?P<column>\d+)$")
# Dentro do bloco de propriedade violada: a expressão da própria asserção.
ASSERTION_RE = re.compile(r"^\s*assertion (?P<expr>.+)$")


def parse_log(path: Path) -> dict:
    """Transforma um arquivo results/<benchmark>.log em um pequeno dicionário
    exportável para JSON: status (SUCCESSFUL/FAILED/UNKNOWN) e, para logs
    FAILED, qual propriedade foi violada e as atribuições de variáveis do
    contraexemplo."""
    text = path.read_text(encoding="utf-8", errors="replace")
    summary = {"log_file": str(path), "benchmark": path.stem}

    if "VERIFICATION SUCCESSFUL" in text:
        summary["status"] = "SUCCESSFUL"
        return summary

    # Nem um sucesso limpo nem um rastro de falha reconhecível (por exemplo,
    # o ESBMC travou, ou o log está incompleto/veio de outra invocação de
    # ferramenta).
    if "[Counterexample]" not in text or "VERIFICATION FAILED" not in text:
        summary["status"] = "UNKNOWN"
        return summary

    summary["status"] = "FAILED"
    violated_property = {}
    counterexample_values = {}

    # Uma única passada pelo log: controla se estamos dentro do bloco
    # "Violated property:", já que o arquivo/linha e o texto da asserção
    # precisam de um parsing diferente das linhas de atribuição que formam
    # o restante do rastro do contraexemplo.
    in_violated_block = False
    for line in text.splitlines():
        if VIOLATED_PROPERTY_HEADER_RE.match(line.strip()):
            in_violated_block = True
            continue

        if in_violated_block:
            match = PROPERTY_LOCATION_RE.match(line)
            if match:
                violated_property["file"] = match.group("file")
                violated_property["line"] = int(match.group("line"))
                continue
            match = ASSERTION_RE.match(line)
            if match and "assertion" not in violated_property:
                violated_property["assertion"] = match.group("expr").strip()
                continue
            if line.strip() == "":
                # Linha em branco encerra o bloco de propriedade violada;
                # volta a tratar as próximas linhas como conteúdo comum do rastro.
                in_violated_block = False
            continue

        # Fora do bloco de propriedade violada: procura atribuições
        # "nome = valor" do rastro do contraexemplo. Atribuições posteriores
        # ao mesmo nome sobrescrevem as anteriores, o que é intencional --
        # queremos o valor final que o ESBMC atribuiu ao longo do rastro.
        match = ASSIGNMENT_RE.match(line)
        if match:
            counterexample_values[match.group("name")] = match.group("value").strip()

    summary["violated_property"] = violated_property
    summary["counterexample_values"] = counterexample_values
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", default=Path("results"), type=Path,
                         help="Diretório com os arquivos .log do ESBMC (padrão: results/)")
    parser.add_argument("--output", default=Path("results/counterexamples.json"), type=Path,
                         help="Onde escrever o resumo JSON (padrão: results/counterexamples.json)")
    args = parser.parse_args()

    # Ordenado para que a ordem de saída do JSON seja estável/determinística entre execuções.
    summaries = [parse_log(log_file) for log_file in sorted(args.results_dir.glob("*.log"))]

    args.output.write_text(json.dumps(summaries, indent=2), encoding="utf-8")
    print(f"Wrote {len(summaries)} log summaries to {args.output}")


if __name__ == "__main__":
    main()

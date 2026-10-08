#!/usr/bin/env bash
# Reproduz os testes ao verificador da skill leitura-academica descritos em
# analise/analise-critica-leitura-e-sinteses.md (secção 2.2, F10, e secção 3.2, E7).
#
# Uso: bash correr.sh /caminho/para/leitura-academica/scripts/verificar.py
set -u
V="${1:?indicar o caminho para verificar.py}"
D="$(cd "$(dirname "$0")" && pwd)"

echo "== 1. Dossiê com vocabulário de História, Religião e Cultura =="
python3 -I "$V" "$D/dossie.md" --fonte F1="$D/fonte.txt"

echo
echo "== 2. Vocabulário religioso técnico tratado como juízo de valor =="
python3 -I "$V" "$D/dossie-religiao.md" --fonte F1="$D/fonte.txt" | sed -n '/NEUTRALIDADE/,/OBJETIVOS/p'

echo
echo "== 3. Sebenta com uma citação inventada (aspas angulares) e outra adulterada (aspas curvas) =="
python3 -I "$V" --sebenta "$D/sebenta.md" --banco "$D/dossie.md" --fonte F1="$D/fonte.txt"

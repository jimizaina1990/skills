"""Testes de regressão do verificador.

Correr a partir da pasta da skill:  python3 -m unittest discover -s scripts/testes -v
Os casos estão em scripts/testes/casos. As fontes são simuladas.
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CASOS = AQUI / "casos"
VERIFICADOR = AQUI.parent / "verificar.py"
ANEXO_A = AQUI.parents[2] / "sinteses-historia" / "references" / "anexo-a-modelo-e-exemplo.md"


def correr(*args):
    r = subprocess.run([sys.executable, "-I", str(VERIFICADOR), *map(str, args)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def escrever(pasta, nome, texto):
    p = Path(pasta) / nome
    p.write_text(texto, encoding="utf-8")
    return p


class Sebenta(unittest.TestCase):

    def test_citacoes_inventadas_em_aspas_angulares_e_curvas_falham(self):
        rc, out = correr("--sebenta", CASOS / "sebenta.md", "--banco", CASOS / "dossie-falhas.md",
                         "--fonte", f"F1={CASOS / 'fonte.txt'}")
        self.assertEqual(rc, 1)
        self.assertIn("Sebenta NÃO apta", out)
        self.assertRegex(out, r"FALHA\s+linha 3 .*\n\s+não existe no banco nem na fonte")
        self.assertRegex(out, r"FALHA\s+linha 5 .*\n\s+não existe no banco nem na fonte")

    def test_negrito_dentro_de_citacao_falha(self):
        _, out = correr("--sebenta", CASOS / "sebenta.md", "--banco", CASOS / "dossie-falhas.md",
                        "--fonte", f"F1={CASOS / 'fonte.txt'}")
        self.assertIn("negrito dentro de uma citação", out)

    def test_falso_titulo_verbo_factivo_juizo_e_arranjo_por_oracao(self):
        _, out = correr("--sebenta", CASOS / "sebenta.md", "--banco", CASOS / "dossie-falhas.md",
                        "--fonte", f"F1={CASOS / 'fonte.txt'}")
        self.assertIn("parágrafo só a negrito", out)
        self.assertIn("\"mostra que\" dá por verdadeiro", out)
        self.assertIn("vocabulário avaliativo na voz da sebenta", out)
        self.assertIn("repete o molde de uma frase da fonte", out)
        self.assertIn("\"Contrarreforma\" (linha 9) não aparece nas fontes", out)

    def test_exemplo_do_anexo_a_passa_sem_falhas_nem_avisos(self):
        texto = ANEXO_A.read_text(encoding="utf-8")
        exemplo = re.search(r"````markdown\n(.*?)````", texto, re.S).group(1)
        with tempfile.TemporaryDirectory() as d:
            seb = escrever(d, "exemplo.md", exemplo)
            rc, out = correr("--sebenta", seb, "--fonte", f"F1={CASOS / 'fonte-homem-simulada.txt'}")
        self.assertEqual(rc, 0, out)
        self.assertIn("Falhas 0, avisos 0.", out)

    def test_ênfase_em_italico_com_indicacao_e_aceite(self):
        with tempfile.TemporaryDirectory() as d:
            seb = escrever(d, "s.md", "# T\n\n## 1. Parte\n\nO autor sustenta que «a Reforma católica "
                                      "não foi *apenas* [ênfase acrescentada] uma reação ao "
                                      "protestantismo» (Autor, 2000, p. 14).\n")
            _, out = correr("--sebenta", seb, "--fonte", f"F1={CASOS / 'fonte.txt'}")
        self.assertNotIn("itálico dentro de uma citação", out)
        self.assertNotIn("negrito dentro", out)
        self.assertRegex(out, r"OK\s+linha 5")


class Dossie(unittest.TestCase):

    def test_sem_falsos_positivos_de_terminologia_e_neutralidade(self):
        _, out = correr(CASOS / "dossie-falhas.md", "--fonte", f"F1={CASOS / 'fonte.txt'}")
        for falso in ('"Cortes"', '"couto"', '"liberalismo"', '"Regeneração"', '"conjuntura"',
                      '"esclarecido"', '"martires"', '"barbaros"'):
            self.assertNotIn(falso, out)
        self.assertIn("OK        nenhum juízo do autor passou para a voz do dossiê", out)

    def test_localizadores_canonicos_e_de_arquivo_aceites(self):
        _, out = correr(CASOS / "dossie-falhas.md", "--fonte", f"F1={CASOS / 'fonte.txt'}")
        self.assertNotIn("não tem localizador", out)

    def test_termo_religioso_ausente_da_fonte_e_assinalado(self):
        _, out = correr(CASOS / "dossie-religiao.md", "--fonte", f"F1={CASOS / 'fonte.txt'}")
        self.assertIn("\"Contrarreforma\" usado no dossiê (linha 9) mas ausente das fontes", out)
        self.assertIn("\"Religiosidade popular\"", out)
        self.assertNotIn("vocabulário avaliativo", out)

    def test_teste_de_compreensao_em_falta_e_falha(self):
        rc, out = correr(CASOS / "dossie-falhas.md", "--fonte", f"F1={CASOS / 'fonte.txt'}")
        self.assertEqual(rc, 1)
        self.assertIn("falta a secção \"Teste de compreensão\"", out)

    def test_era_de_cesar_nao_registada_e_paginas_romanas(self):
        with tempfile.TemporaryDirectory() as d:
            fonte = escrever(d, "f.txt", "Prefácio sobre a carta.\n\ni\n\fFeita a carta em Santarém, "
                                         "Era de mil e quatrocentos e vinte e dois anos.\n\nii\n")
            dossie = escrever(d, "d.md", "# D\n\nEstado. em curso.\n\n## 3. Leitura por unidade\n\n"
                                         "### U1. Prefácio (F1, p. i-ii, pdf 1-2)\n\nTexto.\n\n"
                                         "## 13. Banco de citações\n\n"
                                         "[C01] | F1 | pdf 2 | (Autor, 2000, p. ii)\n"
                                         "\"Feita a carta em Santarém\"\n")
            _, out = correr(dossie, "--fonte", f"F1={fonte}", "--paginas", "F1=1-2:i")
        self.assertIn("a fonte data pela era", out)
        self.assertRegex(out, r"OK\s+C01\s+pdf 2\s+\(Autor, 2000, p\. ii\)")


class Registo(unittest.TestCase):

    def test_registo_da_verificacao_falso_e_assinalado(self):
        with tempfile.TemporaryDirectory() as d:
            fonte = escrever(d, "f.txt", "Texto da página um com uma frase citável aqui.\n\n1\n")
            base = ("# D\n\nEstado. concluído.\n\n## 3. Leitura por unidade\n\n"
                    "### U1. Tudo (F1, p. 1, pdf 1)\n\nTexto.\n\n## 12. Pendências\n\n{reg}\n\n"
                    "## 13. Banco de citações\n\n[C01] | F1 | pdf 1 | (Autor, 2000, p. 1)\n"
                    "\"uma frase citável aqui\"\n")
            falso = escrever(d, "a.md", base.format(reg="Verificação. 99 citações. Falhas 0."))
            rc, out = correr(falso, "--fonte", f"F1={fonte}")
            self.assertEqual(rc, 1)
            self.assertIn("não coincide com esta verificação", out)
            certo = escrever(d, "b.md", base.format(reg="Verificação. 1 citações. Falhas 0."))
            rc, out = correr(certo, "--fonte", f"F1={fonte}")
            self.assertEqual(rc, 0, out)


if __name__ == "__main__":
    unittest.main()

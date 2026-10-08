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


FONTE_APA = ("Texto da primeira página. A forma pela qual são apresentados os fatos pode ser "
             "propaganda realista ex post facto, como alguns eruditos argumentam, mas os próprios "
             "fatos eram bastante claros. Os filisteus avançaram para o interior.\n\n1\n\f"
             "Texto da segunda página. Isaías marca o ponto em que a religião começou a "
             "espiritualizar-se e a passar para o plano universalista. O Servo Sofredor dirige para "
             "uma conclusão triunfal a missão da nação.\n\n2\n\f"
             "Texto da terceira página sobre outro assunto, sem relação com o resto.\n\n3\n")

SEBENTA_APA = """# Tema

## 1. Parte

**Para o autor, Isaías marca a viragem em que a religião se espiritualiza e passa ao plano universalista.** O autor escreve que «Isaías marca o ponto em que a religião começou a espiritualizar-se e a passar para o plano universalista» (Autor, 1980/2000, p. 2).

O autor admite que «pode ser propaganda realista ex post facto [...] mas os próprios fatos eram bastante claros» (Autor, 1980/2000, p. 1).

Na costa, os Povos do Mar combateram as tribos durante muito tempo, segundo esta leitura.

Este objetivo deve ser corrigido porque a fonte não trata da recuperação do reino.

A datação proposta deve ser confirmada antes de ser usada numa avaliação pelo estudante.

> Isaías marca o ponto em que a religião começou a espiritualizar-se (Autor, 2000, p. 2).

O autor diz que «Isaías marca o ponto em que a religião começou a espiritualizar-se \\[sic\\]» (Autor, 1980/2000, p. 2).

## Esquema-síntese

&#91;embedded content: esquema]

## Referências

Autor, A. (2000). *Livro* (B. Tradutor, Trad.). Editora. (Obra original publicada em 1980)
"""


class Apa7EFidelidade(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.TemporaryDirectory()
        cls.fonte = escrever(cls.dir.name, "f.txt", FONTE_APA)
        cls.seb = escrever(cls.dir.name, "s.md", SEBENTA_APA)
        cls.rc, cls.out = correr("--sebenta", cls.seb, "--fonte", f"F1={cls.fonte}")

    @classmethod
    def tearDownClass(cls):
        cls.dir.cleanup()

    def test_obra_traduzida_sem_os_dois_anos_falha(self):
        self.assertEqual(self.rc, 1)
        self.assertIn("só com o ano da edição lida, (Autor, 2000", self.out)
        self.assertIn("(Autor, 1980/2000, p. X)", self.out)

    def test_omissao_que_retira_a_atribuicao(self):
        self.assertIn("a omissão retira texto com atribuição", self.out)
        self.assertIn("como alguns eruditos argumentam", self.out)

    def test_reticencias_entre_parenteses_e_sic_em_redondo(self):
        self.assertIn("omissão entre parênteses retos", self.out)
        self.assertIn("[sic] em redondo", self.out)

    def test_bloco_curto(self):
        self.assertIn("citação em bloco com menos de 40 palavras", self.out)

    def test_tese_a_negrito_que_parafraseia_a_citacao(self):
        self.assertIn("a tese a negrito diz por outras palavras a citação", self.out)

    def test_objetivo_corrigido_e_por_confirmar(self):
        self.assertIn("a sebenta corrige o objetivo", self.out)
        self.assertIn("afirmação dada como por confirmar fora das lacunas", self.out)

    def test_nomes_ausentes_das_fontes(self):
        self.assertRegex(self.out, r"nomes próprios que não aparecem nas fontes: .*Povos do Mar")

    def test_conteudo_embebido_e_esquema_vazio(self):
        self.assertIn("conteúdo embebido que não passou para o texto", self.out)
        self.assertIn("a secção do esquema não tem esquema", self.out)

    def test_sic_em_italico_aceite(self):
        with tempfile.TemporaryDirectory() as d:
            seb = escrever(d, "s.md", "# T\n\n## 1. Parte\n\nO autor escreve que «Isaías marca o "
                                      "ponto em que a religião [*sic*] começou a espiritualizar-se» "
                                      "(Autor, 2000, p. 2).\n")
            _, out = correr("--sebenta", seb, "--fonte", f"F1={self.fonte}")
        self.assertNotIn("[sic] em redondo", out)
        self.assertNotIn("itálico dentro de uma citação", out)

    def test_procurar_devolve_a_pagina_e_o_que_falta_no_banco(self):
        with tempfile.TemporaryDirectory() as d:
            dossie = escrever(d, "d.md", "## 13. Banco de citações\n\n[C01] | F1 | pdf 1 | "
                                         "(Autor, 1980/2000, p. 1)\n\"os próprios fatos eram bastante "
                                         "claros\"\n")
            rc, out = correr("--procurar", "Servo Sofredor missão da nação", "--fonte",
                             f"F1={self.fonte}", "--banco", dossie, "--top", "2")
        self.assertEqual(rc, 0, out)
        primeira = out.split("\n")[1]
        self.assertIn("pdf 2", primeira)
        self.assertIn("SEM citação no banco", primeira)


class BlocoLocalizador(unittest.TestCase):

    def test_bloco_usa_o_seu_proprio_paragrafo_de_referencia(self):
        texto = ("Isaías marca o ponto em que a religião começou a espiritualizar-se e a passar "
                 "para o plano universalista. ")
        bloco = (texto * 3).strip()
        with tempfile.TemporaryDirectory() as d:
            fonte = escrever(d, "f.txt", "Página um.\n\n1\n\f" + bloco + "\n\n2\n")
            seb = escrever(d, "s.md", "# T\n\n## 1. Parte\n\nO autor escreve:\n\n> " + bloco +
                           " (Autor, 2000, p. 2)\n\nNoutro ponto, a matéria segue (Autor, 2000, p. 1).\n")
            _, out = correr("--sebenta", seb, "--fonte", f"F1={fonte}")
        self.assertNotIn("a sebenta diz p. [1]", out)
        self.assertRegex(out, r"OK\s+linha 7")


class DossieVarreduraEAno(unittest.TestCase):

    def test_varredura_em_falta_e_ano_duplo_no_dossie(self):
        with tempfile.TemporaryDirectory() as d:
            fonte = escrever(d, "f.txt", FONTE_APA)
            dossie = escrever(d, "d.md", "# D\n\nEstado. em curso.\n\n## 0. Objetivos\n\n"
                                         "### O1. Explicar\n\n## 1. Fichas\n\n### F1. Livro\n\n"
                                         "- Referência. Autor, A. (2000). *Livro* (B. T., Trad.). "
                                         "Editora. (Obra original publicada em 1980)\n\n"
                                         "## 3. Leitura por unidade\n\n"
                                         "### U1. Tudo (F1, p. 1-3, pdf 1-3)\n\nTexto.\n\n"
                                         "## 11. Mapa dos objetivos\n\n| O1 | U1 | [C01] | coberto | - |\n\n"
                                         "## 13. Banco de citações\n\n[C01] | F1 | pdf 1 | "
                                         "(Autor, 2000, p. 1)\n\"os próprios fatos eram bastante "
                                         "claros\"\n")
            rc, out = correr(dossie, "--fonte", f"F1={fonte}")
        self.assertEqual(rc, 1)
        self.assertIn("falta a \"Varredura por objetivo\"", out)
        self.assertIn("só com o ano da edição lida, (Autor, 2000", out)


if __name__ == "__main__":
    unittest.main()

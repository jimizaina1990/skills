#!/usr/bin/env python3
"""Verificador da leitura académica e da sebenta.

Modos

  Dossiê
    verificar.py DOSSIE.md --fonte F1=obra.pdf [--fonte F2=outra.txt] [--marcar]
                 [--ambito F1=9-120] [--paginas F1=9-120:1] [--max-sem-prova 12]
  Sebenta
    verificar.py --sebenta SEBENTA.md --banco DOSSIE.md [--fonte F1=obra.pdf]
    verificar.py --sebenta SEBENTA.md --fonte F1=obra.pdf        (sem dossiê)
  Procurar uma passagem
    verificar.py --localizar "trecho" --fonte obra.pdf

O que verifica no dossiê

  1. Citações. Cada citação do banco existe no texto da fonte. Tolera hifenização,
     espaçamento, tipo de aspas, chamadas de nota coladas à palavra e a passagem
     de uma página para a seguinte.
  2. Páginas e localizadores. A página PDF declarada e a página impressa da
     referência APA (árabe ou romana) coincidem com as do texto. Aceita também
     localizadores canónicos (Mateus 5:3, Mt 5, 3, 10.27), fólios e colunas.
  3. Cobertura. Todas as páginas do âmbito pertencem a uma unidade do dossiê.
  4. Prova de leitura. Cada unidade tem pelo menos uma citação confirmada nas suas
     páginas e nenhum troço longo do texto fica sem citação.
  5. Arranjo. Frases e orações da leitura, fora de aspas, que copiam a fonte ou lhe
     repetem o molde com outras palavras.
  6. Neutralidade e terminologia. Vocabulário avaliativo do autor na voz do
     dossiê, e termos de alerta sem entrada no quadro de conceitos ou ausentes das
     fontes. As listas vêm de references/terminologia.md, secções 3 e 6.
  7. Teste de compreensão, fichas e datação. Perguntas por objetivo com
     resultado, campos "Data de redação" e "Contexto historiográfico" nas fichas,
     e datas da Era de César não registadas.
  8. Objetivos e articulação. Cada objetivo tem linha no mapa dos objetivos, com
     citações ou com a indicação de que as fontes não o cobrem. Com duas ou mais
     fontes, existe articulação entre obras com citações de mais de uma.
  9. Estado. O dossiê não se declara concluído com falhas ou páginas por ler.

O que verifica na sebenta

  Citações em aspas retas, angulares e curvas e em bloco, contra o banco e as
  fontes, com a página. Negrito dentro de citações e itálico sem [ênfase
  acrescentada]. Títulos estruturados, secções obrigatórias, uma citação por
  parte, chamadas de nota e notas com referência, excesso de negrito. Verbos
  factivos e de adesão, vocabulário avaliativo, arranjo e termos de alerta sem
  nota ou ausentes das fontes (estes dois últimos só com --fonte).

O que não verifica

  A fidelidade do sentido, a qualidade da explicação, a correção do OCR, a
  paráfrase profunda e o arranjo por tradução de uma fonte noutra língua.

Formato da tabela de páginas (--paginas)

  F1=9-40:1,43-200:33      pdf 9 é a p. 1 e pdf 43 é a p. 33 (estampas entre elas)
  F1=5-12:i,13-300:1       pdf 5 a 12 são as pp. i a viii, pdf 13 é a p. 1
  F1=5-90:1x2              digitalização com duas páginas por imagem, pdf 5 = pp. 1-2
"""

import argparse
import bisect
import difflib
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------- normalização

ASPAS = dict.fromkeys(map(ord, "\"“”„«»‘’‚‹›'"), None)
TRAVESSOES = {ord(c): "-" for c in "‐‑‒–—―−"}
# chamada de nota colada a uma palavra ou a pontuação (Nação12, rei,12)
NOTA = re.compile(r"(?:(?<=[^\W\d_])|(?<=[.,;:!?)\]]))\d{1,3}(?=[\s.,;:!?)\]]|$)")
ELIPSE = re.compile(r"\s*(?:\[\s*(?:\.\s?\.\s?\.|…)\s*\]|\.\s?\.\s?\.|…|\[[^\]]*\])\s*")


def base(s):
    s = unicodedata.normalize("NFKC", s).replace("­", "")
    return s.translate(ASPAS).translate(TRAVESSOES)


def n1(s):
    """Literalidade, com tolerância a artefactos de extração e chamadas de nota."""
    s = base(s)
    s = re.sub(r"(?<=\w)-[ \t]*\n[ \t]*(?=[a-zà-ÿ])", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return NOTA.sub("", s)


def n2(s):
    """Sem espaços, hífenes nem maiúsculas. Aceita com ressalva."""
    return re.sub(r"[\s\-]+", "", n1(s).lower())


def sem_acentos(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


# ---------------------------------------------------------------- fontes

def carregar_fonte(caminho):
    p = Path(caminho)
    if not p.exists():
        raise SystemExit(f"Fonte inexistente: {caminho}")
    suf = p.suffix.lower()
    if suf in {".docx", ".doc", ".odt", ".epub", ".rtf"}:
        raise SystemExit(f"{caminho}: converter primeiro em texto simples (.txt, com \\f entre "
                         "páginas se as houver) e passar esse ficheiro.")
    if suf == ".pdf":
        r = subprocess.run(["pdftotext", "-enc", "UTF-8", str(p), "-"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"pdftotext falhou em {caminho}: {r.stderr.strip()}")
        texto = r.stdout
        if len(texto.strip()) < 50:
            raise SystemExit(f"{caminho} não tem camada de texto (digitalizado). Fazer OCR, "
                             "guardar o texto com \\f entre páginas e passar esse ficheiro.")
    else:
        texto = p.read_text(encoding="utf-8", errors="replace")
    paginas = texto.split("\f")
    if len(paginas) > 1 and not paginas[-1].strip():
        paginas.pop()
    return paginas


class Indice:
    """Texto normalizado de todas as páginas e posição onde cada uma começa."""

    def __init__(self, paginas, norm):
        partes = [norm(p) for p in paginas]
        self.sep = " " if norm is n1 else ""
        self.texto = self.sep.join(partes)
        self.inicios, pos = [], 0
        for parte in partes:
            self.inicios.append(pos)
            pos += len(parte) + len(self.sep)
        self.norm = norm
        self.tem_paginas = len(paginas) > 1

    def pagina(self, i):
        return bisect.bisect_right(self.inicios, i)

    def ocorrencias(self, chave, limite=200):
        achados, i = [], self.texto.find(chave)
        while i >= 0 and len(achados) < limite:
            achados.append(i)
            i = self.texto.find(chave, i + 1)
        return achados


class Fonte:
    def __init__(self, caminho):
        self.caminho = caminho
        self.brutas = carregar_fonte(caminho)
        self.i1 = Indice(self.brutas, n1)
        self.i2 = Indice(self.brutas, n2)
        self.pags_n1 = [n1(p) for p in self.brutas]
        self.n = len(self.brutas)
        self.tem_paginas = self.n > 1
        self.impressas = mapa_detetado(numeros_candidatos(self.brutas)) if self.tem_paginas else {}
        self.tabela = None  # dada com --paginas
        self._frases = None
        self._ngramas = None

    def impressa(self, pdf):
        """Devolve (conjunto de páginas impressas, origem) ou (None, None)."""
        if self.tabela is not None:
            return self.tabela.get(pdf, (None, None))
        return self.impressas.get(pdf, (None, None))


_cache = {}


def fonte_para(caminho):
    if caminho not in _cache:
        _cache[caminho] = Fonte(caminho)
    return _cache[caminho]


# ---------------------------------------------------------------- páginas impressas

NUM_LINHA = re.compile(r"^(\d{1,4})$")
NUM_PONTA = re.compile(r"^(\d{1,4})\s+\D.{0,70}$|^.{0,70}\D\s+(\d{1,4})$")


def numeros_candidatos(brutas):
    """Números que podem ser a página impressa, com peso. Linha só com o número pesa 2,
    número na ponta de um cabeçalho curto pesa 1. Linhas de nota de rodapé não contam."""
    cands = []
    for p in brutas:
        linhas = [l.strip() for l in p.split("\n") if l.strip()]
        zona = linhas[:3] + linhas[-3:]
        c = {}
        for l in zona:
            m = NUM_LINHA.match(l)
            if m:
                c[int(m.group(1))] = 2
            elif len(l) <= 80 and not re.search(r"[.,;:]$|\b(?:Cf|Ibid|Idem|Vd|Ver)\b", l):
                m = NUM_PONTA.match(l)
                if m:
                    c.setdefault(int(m.group(1) or m.group(2)), 1)
        cands.append(c)
    return cands


def mapa_detetado(cands, raio=8):
    """Aceita um número só se o mesmo desfasamento se repetir numa página vizinha."""
    n = len(cands)
    aceite = [None] * n
    for i in range(n):
        melhor = None
        for v, peso in cands[i].items():
            d = v - (i + 1)
            apoio = sum(1 for j in range(max(0, i - raio), min(n, i + raio + 1))
                        if (j + 1 + d) in cands[j])
            if apoio >= 2 and (melhor is None or (apoio * peso) > melhor[0]):
                melhor = (apoio * peso, v)
        if melhor:
            aceite[i] = melhor[1]
    mapa = {}
    for i in range(n):
        if aceite[i] is not None:
            mapa[i + 1] = ({aceite[i]}, "lida no PDF")
            continue
        viz = [(abs(j - i), j) for j in range(max(0, i - raio), min(n, i + raio + 1))
               if aceite[j] is not None]
        if viz:
            _, j = min(viz)
            mapa[i + 1] = ({i + 1 + aceite[j] - (j + 1)}, "estimada")
    return mapa


ROMANOS = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}


def romano_para_int(r):
    total, maior = 0, 0
    for ch in reversed(r.lower()):
        v = ROMANOS[ch]
        if v < maior:
            total -= v
        else:
            total += v
            maior = v
    return total


def int_para_romano(n):
    out = ""
    for v, r in ((1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"),
                 (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")):
        while n >= v:
            out, n = out + r, n - v
    return out


def ordenar(paginas):
    """Páginas romanas (texto) antes das árabes (inteiros)."""
    return sorted(paginas, key=lambda p: (0, romano_para_int(p)) if isinstance(p, str) else (1, p))


def texto_paginas(paginas):
    return "-".join(map(str, ordenar(paginas)))


PAG = r"(\d+|[ivxlcdm]+)"


def tabela_paginas(espec):
    """'5-12:i,13-40:1,43-200:33x2' -> {pdf: ({impressas}, 'tabela')}. Páginas romanas em minúsculas."""
    tab = {}
    for parte in espec.split(","):
        m = re.fullmatch(rf"\s*(\d+)\s*-\s*(\d+)\s*:\s*{PAG}\s*(x2)?\s*", parte)
        if not m:
            raise SystemExit(f"--paginas mal formado: {parte!r} (ex. 9-40:1, 5-12:i ou 5-90:1x2)")
        a, b, dupla = int(m.group(1)), int(m.group(2)), bool(m.group(4))
        romana = not m.group(3).isdigit()
        p = romano_para_int(m.group(3)) if romana else int(m.group(3))
        conv = int_para_romano if romana else (lambda x: x)
        for i in range(a, b + 1):
            if dupla:
                k = p + 2 * (i - a)
                tab[i] = ({conv(k), conv(k + 1)}, "tabela")
            else:
                tab[i] = ({conv(p + i - a)}, "tabela")
    return tab


APA_PAG = re.compile(rf"\bpp?\.\s*{PAG}\b(?:\s*[-–]\s*{PAG}\b)?")


def paginas_apa(apa):
    m = APA_PAG.search(apa or "")
    if not m:
        return set()
    a, b = m.group(1), m.group(2) or m.group(1)
    if a.isdigit() and b.isdigit():
        a, b = int(a), int(b)
        return set(range(a, b + 1)) if b >= a else {a}
    if not a.isdigit() and not b.isdigit():
        x, y = romano_para_int(a), romano_para_int(b)
        return {int_para_romano(k) for k in range(x, y + 1)} if y >= x else {a}
    return {int(a) if a.isdigit() else a}


# ---------------------------------------------------------------- procurar citações

def segmentos(citacao):
    return [s for s in ELIPSE.split(citacao) if len(s.strip()) >= 3]


def atravessa(chave, fonte):
    """Procura uma citação partida pela mudança de página (cabeçalhos, notas, número)."""
    w = chave.split(" ")
    if len(w) < 6 or not fonte.tem_paginas:
        return None
    for k in range(3, len(w) - 2):
        pre, suf = " ".join(w[:k]), " ".join(w[k:])
        for i in range(fonte.n - 1):
            if pre in fonte.pags_n1[i]:
                j = fonte.pags_n1[i + 1].find(suf)
                if 0 <= j <= 600:
                    return [i + 1, i + 2]
    return None


def procurar(citacao, fonte, declaradas):
    """Devolve (nivel, paginas, avisos, em_falta). nivel 1 literal, 2 ressalva, 0 falha."""
    paginas, avisos, em_falta, nivel, ultimo = [], [], [], 1, 0
    for seg in segmentos(citacao):
        achado = False
        for idx, nv in ((fonte.i1, 1), (fonte.i2, 2)):
            chave = idx.norm(seg)
            occ = idx.ocorrencias(chave)
            if not occ:
                continue
            if declaradas and idx.tem_paginas:
                occ = [i for i in occ if idx.pagina(i) in declaradas] or occ
            seguintes = [i for i in occ if i >= ultimo] if nv == 1 else occ
            escolhida = seguintes[0] if seguintes else occ[0]
            if nv == 1 and not seguintes and paginas:
                avisos.append("segmentos fora da ordem do texto")
            ultimo = escolhida + len(chave) if nv == 1 else ultimo
            paginas.append(idx.pagina(escolhida))
            nivel = max(nivel, nv)
            achado = True
            break
        if not achado:
            par = atravessa(n1(seg), fonte)
            if par:
                paginas += par
                nivel = 2
                avisos.append(f"atravessa a mudança de página (pdf {par[0]}-{par[1]}), conferir")
                achado = True
        if not achado:
            em_falta.append(seg)
    if em_falta:
        nivel = 0
    return nivel, paginas, avisos, em_falta


def diagnostico(seg, idx):
    palavras = idx.norm(seg).split(" ")
    for n in range(len(palavras), 2, -1):
        pref = " ".join(palavras[:n])
        i = idx.texto.find(pref)
        if i >= 0:
            fonte_seg = idx.texto[i + len(pref): i + len(pref) + 70].strip()
            citado = " ".join(palavras[n: n + 8])
            if n == len(palavras):
                return "o troço existe mas falhou a comparação, conferir manualmente"
            return (f"coincide até à palavra {n}. A citação continua com \"{citado}\" "
                    f"e a fonte tem \"{fonte_seg}\"")
    for n in range(len(palavras) - 1, 2, -1):
        if idx.texto.find(" ".join(palavras[-n:])) >= 0:
            return (f"só o fim coincide (últimas {n} palavras). O início foi alterado "
                    "ou pertence a outra passagem")
    return ("nenhuma sequência de 3 palavras coincide. A citação foi reescrita, vem de outra "
            "fonte ou o texto extraído está corrompido")


# ---------------------------------------------------------------- leitura do dossiê

CAB = re.compile(r"^\[C(\d+)\]\s*\|")
REF = re.compile(r"\[C(\d+)\]")
PDF_CAMPO = re.compile(r"pdf\s*(\d+)(?:\s*[-–]\s*(\d+))?", re.I)
LOCALIZADOR_APA = re.compile(
    r"\b(?:pp?\.|para\.|par\.|cap\.|sec\.|secç?ão|f\.|fl\.|fls\.|fól\.|fols?\.|col\.|cols\.|"
    r"liv\.|n\.º|q\.|art\.|cân\.)|§"
    r"|(?<![\d/])\d{1,3}\s*[:.]\s*\d{1,3}\b"                      # canónico, Mateus 5:3, 10.27
    r"|\b[A-ZÀ-Ý][a-zà-ÿ]{0,10}\.?\s+\d{1,3}\s*,\s*\d{1,3}\b")      # Mt 5, 3 ou Gn 1,1
UNID = re.compile(r"^###\s+U(\d+)\b")
OBJ = re.compile(r"^###\s+O(\d+)\b")
FICHA = re.compile(r"^###\s+(F\d+)\b")
PARENS = re.compile(r"\(([^()]*)\)")


def visiveis(linhas):
    """Linhas com os comentários HTML apagados (mantém a numeração)."""
    out, dentro = [], False
    for l in linhas:
        res, i = "", 0
        while i < len(l):
            if dentro:
                j = l.find("-->", i)
                if j < 0:
                    i = len(l)
                else:
                    dentro, i = False, j + 3
            else:
                j = l.find("<!--", i)
                if j < 0:
                    res += l[i:]
                    i = len(l)
                else:
                    res += l[i:j]
                    dentro, i = True, j + 4
        out.append(res)
    return out


def intervalo(texto):
    m = PDF_CAMPO.search(texto or "")
    if not m:
        return None
    a = int(m.group(1))
    b = int(m.group(2)) if m.group(2) else a
    return (a, b) if b >= a else (b, a)


def ler_banco(linhas):
    entradas, erros, i = [], [], 0
    while i < len(linhas):
        m = CAB.match(linhas[i])
        if not m:
            i += 1
            continue
        campos = [c.strip() for c in linhas[i].split("|")]
        cid = "C" + m.group(1)
        if len(campos) < 4:
            erros.append(f"{cid}: cabeçalho com menos de 4 campos (id | fonte | pdf | (APA))")
            i += 1
            continue
        j = i + 1
        while j < len(linhas) and not linhas[j].strip():
            j += 1
        cit = linhas[j].strip() if j < len(linhas) else ""
        if not (len(cit) >= 2 and cit[0] == '"' and cit[-1] == '"'):
            erros.append(f"{cid}: a linha seguinte ao cabeçalho tem de ser a citação entre "
                         "aspas retas, numa só linha")
            i += 1
            continue
        entradas.append({"id": cid, "fonte": campos[1].upper(), "pdf": campos[2],
                         "apa": campos[3], "estado": campos[4] if len(campos) > 4 else "",
                         "citacao": cit[1:-1], "ln_cab": i})
        i = j + 1
    return entradas, erros


def seccoes(vis):
    """[(titulo, inicio, fim)] das secções de nível 2."""
    marcas = [(n, l[3:].strip()) for n, l in enumerate(vis) if l.startswith("## ")]
    out = []
    for k, (n, t) in enumerate(marcas):
        fim = marcas[k + 1][0] if k + 1 < len(marcas) else len(vis)
        out.append((t, n, fim))
    return out


def seccao(secs, palavra):
    for t, a, b in secs:
        if palavra.lower() in t.lower():
            return a, b
    return None


def ler_unidades(vis):
    unidades = []
    for n, l in enumerate(vis):
        m = UNID.match(l)
        if not m:
            continue
        cand = [g for g in PARENS.findall(l) if re.search(r"\bF\d+\b", g) and "pdf" in g.lower()]
        fim = n + 1
        while fim < len(vis) and not vis[fim].startswith(("### ", "## ")):
            fim += 1
        corpo = "\n".join(vis[n + 1:fim])
        u = {"id": "U" + m.group(1), "ln": n, "titulo": l.strip(), "fonte": None, "pdf": None,
             "sem_cit": bool(re.search(r"Sem passagem citável", corpo, re.I)),
             "interroga": bool(re.search(r"\*\*Interrogação do texto\.\*\*\s*\S", corpo)),
             "ilegivel": "[ilegível]" in l.lower(),
             "objetivos": set(re.findall(r"\bO(\d+)\b", "\n".join(
                 x for x in corpo.split("\n") if "Objetivos servidos" in x)))}
        if cand:
            g = cand[-1]
            u["fonte"] = re.search(r"\b(F\d+)\b", g).group(1).upper()
            u["pdf"] = intervalo(g)
        unidades.append(u)
    return unidades


def ambitos_das_fichas(vis):
    amb, atual = {}, None
    for l in vis:
        m = FICHA.match(l)
        if m:
            atual = m.group(1).upper()
            continue
        if l.startswith(("## ", "### ")):
            atual = None
        if atual and "Âmbito fornecido" in l:
            iv = intervalo(l)
            if iv:
                amb[atual] = iv
    return amb


# ---------------------------------------------------------------- arranjo

PARAGEM = set(sem_acentos("""
a o as os um uma uns umas de do da dos das em no na nos nas num numa por pelo pela pelos
pelas para com sem sob sobre entre até após ante contra desde e ou mas nem que se como
quando porque pois porém contudo todavia então já não sim mais menos muito muita muitos
muitas também só apenas ainda este esta estes estas esse essa esses essas aquele aquela
aqueles aquelas isto isso aquilo ele ela eles elas lhe lhes seu sua seus suas ao aos à às
neste nesta nesse nessa naquele naquela deste desta desse dessa daquele daquela cujo cuja
qual quais onde é ser foi eram era são será seria sido estar está estava ter tem tinha há
havia houve tal tais cada todo toda todos todas outro outra outros outras mesmo mesma assim
lo la los las me te vos nós vós eu tu
""").split())


def tokens(s):
    return re.findall(r"[^\W_]+", sem_acentos(s.lower()))


def raiz(w):
    return w[:5]


def conteudo(toks):
    return [t for t in toks if t not in PARAGEM and len(t) >= 4 and not t.isdigit()]


def molde(toks):
    return [t if t in PARAGEM else "_" for t in toks]


FRASE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý0-9])")


def corpo_das_paginas(fonte):
    """Texto de cada página sem cabeçalhos, rodapés, números de página nem notas finais."""
    if getattr(fonte, "_corpo", None) is None:
        contagem = Counter()
        paginas = [[l.strip() for l in p.split("\n") if l.strip()] for p in fonte.brutas]
        for ls in paginas:
            for l in set(ls[:2] + ls[-2:]):
                contagem[re.sub(r"\d+", "#", l)] += 1
        limiar = max(3, 0.3 * len(paginas))
        repetidas = {k for k, v in contagem.items() if v >= limiar}

        def ruido(l):
            return re.sub(r"\d+", "#", l) in repetidas or NUM_LINHA.match(l)

        corpo = []
        for ls in paginas:
            ls = list(ls)
            while ls and ruido(ls[0]):
                ls.pop(0)
            while ls and (ruido(ls[-1]) or re.match(r"^\d{1,3}\s+\S", ls[-1])):
                ls.pop()
            corpo.append(n1("\n".join(ls)))
        fonte._corpo = corpo
    return fonte._corpo


def frases_da_fonte(fonte):
    if fonte._frases is None:
        frases = []
        for p, txt in enumerate(corpo_das_paginas(fonte), 1):
            for f in FRASE.split(txt):
                toks = tokens(f)
                if len(toks) >= 8:
                    frases.append((p, f.strip(), toks))
        indice = defaultdict(set)
        for k, (_, _, toks) in enumerate(frases):
            for r in {raiz(t) for t in conteudo(toks)}:
                indice[r].add(k)
        fonte._frases = (frases, indice)
    return fonte._frases


def ngramas_da_fonte(fonte, n=7):
    if fonte._ngramas is None:
        mapa = {}
        for p, txt in enumerate(corpo_das_paginas(fonte), 1):
            toks = tokens(txt)
            for k in range(len(toks) - n + 1):
                g = tuple(toks[k:k + n])
                if len(conteudo(g)) >= 3 and g not in mapa:
                    mapa[g] = p
        fonte._ngramas = mapa
    return fonte._ngramas


def prosa_para_arranjo(vis, excluir):
    """Frases do dossiê fora das aspas, com o número da linha."""
    out, em_codigo = [], False
    for n, l in enumerate(vis):
        if l.strip().startswith("```"):
            em_codigo = not em_codigo
            continue
        if em_codigo or any(a <= n < b for a, b in excluir):
            continue
        s = l.strip()
        if not s or s.startswith("#") or re.fullmatch(r"[|\-\s:]+", s):
            continue
        s = re.sub(r'"[^"]*"|“[^”]*”|«[^»]*»', " ", s)
        s = REF.sub(" ", s)
        s = re.sub(r"\([^()]*\b(?:pp?\.|pdf|para\.|par\.)[^()]*\)", " ", s)
        s = re.sub(r"[*_`|]", " ", s)
        for f in FRASE.split(s):
            toks = tokens(f)
            if len(toks) >= 7:
                out.append((n + 1, f.strip(), toks))
    return out


ORACAO = re.compile(r",\s+(?:e|mas|porque|pois|embora|enquanto|que)\s+|;\s*|:\s+")


def com_oracoes(frases):
    """Cada frase e, se for composta, as suas orações com pelo menos dez palavras, para apanhar
    o arranjo de uma só oração dentro de uma frase mais longa."""
    out = []
    for ln, frase, toks in frases:
        out.append((ln, frase, toks, False))
        partes = ORACAO.split(frase)
        if len(partes) > 1:
            for p in partes:
                t = tokens(p)
                if len(t) >= 10:
                    out.append((ln, p.strip(), t, True))
    return out


def verificar_arranjo(frases_dossie, fontes):
    avisos, assinaladas = [], set()
    for ln, frase, toks, oracao in com_oracoes(frases_dossie):
        if ln in assinaladas:
            continue
        achado = None
        for fid, fonte in fontes.items():
            ng = ngramas_da_fonte(fonte)
            for k in range(len(toks) - 6):
                g = tuple(toks[k:k + 7])
                if g in ng:
                    achado = (f"copia a fonte sem aspas ({fid}, pdf {ng[g]})", " ".join(g))
                    break
            if achado:
                break
            if len(toks) < (10 if oracao else 12):
                continue
            frases, indice = frases_da_fonte(fonte)
            raizes = {raiz(t) for t in conteudo(toks)}
            cont = Counter()
            for r in raizes:
                for k in indice.get(r, ()):
                    cont[k] += 1
            sk = molde(toks)
            for k, comuns in cont.most_common(25):
                if comuns < (3 if oracao else 2):
                    break
                p, fr, ftoks = frases[k]
                if not 0.7 <= len(toks) / len(ftoks) <= 1.4:
                    continue
                fr_raizes = {raiz(t) for t in conteudo(ftoks)}
                jac = len(raizes & fr_raizes) / max(1, len(raizes | fr_raizes))
                razao = difflib.SequenceMatcher(None, sk, molde(ftoks), autojunk=False).ratio()
                if razao >= 0.8:
                    achado = (f"repete o molde de uma frase da fonte ({fid}, pdf {p}), "
                              "possível arranjo por troca de palavras", fr[:110])
                elif jac >= 0.6 and len(raizes & fr_raizes) >= 5:
                    achado = (f"usa quase só o vocabulário de uma frase da fonte ({fid}, pdf {p})",
                              fr[:110])
                if achado:
                    break
            if achado:
                break
        if achado:
            assinaladas.add(ln)
            avisos.append((ln, frase, achado))
    return avisos


# ---------------------------------------------------------------- listas de references/terminologia.md

REF_DIR = Path(__file__).resolve().parent.parent / "references"

# usadas só se references/terminologia.md não existir
AVALIATIVOS_RESERVA = ["obscurantis*", "glorios*", "fanatic*", "decadent*", "retrograd*",
                       "reacionari*", "nefast*", "funest*", "infam*", "abominave*", "vergonhos*",
                       "pernicios*", "deplorave*", "lamentave*", "traidor*"]


def norm_termo(s):
    """Sem acentos, com hífenes de prefixo tratados como na grafia do AO 1990
    (Contra-Reforma = Contrarreforma), restantes hífenes como espaços. Mantém a caixa."""
    s = sem_acentos(unicodedata.normalize("NFKC", s)).translate(TRAVESSOES)
    s = re.sub(r"(?<=\w)-(?=[rsRS])", "", s)
    s = s.replace("-", " ")
    s = re.sub(r"rr", "r", s)
    s = re.sub(r"ss", "s", s)
    return re.sub(r"\s+", " ", s).strip()


def padrao_palavra(w):
    w = re.escape(w)
    if w.endswith("ao"):
        return w[:-2] + "(?:ao|oes|aos|aes)"
    if w.endswith("l"):
        return w[:-1] + "(?:l|is)"
    if w.endswith("m"):
        return w[:-1] + "(?:m|ns)"
    if w.endswith("s"):
        return w
    if w.endswith(("r", "z")):
        return w + "(?:es)?"
    return w + "s?"


def padrao_termo(termo, caixa=None):
    corpo = r"\s+".join(padrao_palavra(p) for p in norm_termo(termo).lower().split())
    prefixo = "(?=[A-Z])" if caixa == "maius" else "(?=[a-z])" if caixa == "minus" else ""
    return re.compile(rf"(?<!\w){prefixo}(?i:{corpo})(?!\w)")


def ler_listas():
    p = REF_DIR / "terminologia.md"
    if not p.exists():
        return None
    txt = p.read_text(encoding="utf-8")

    def lista(titulo):
        m = re.search(r"^### " + re.escape(titulo) + r"[^\n]*\n+(.+?)(?=\n#|\Z)", txt, re.S | re.M)
        if not m:
            return []
        return [x.strip() for x in m.group(1).replace("\n", " ").split(",") if x.strip()]

    maius = {norm_termo(t).lower() for t in lista("Termos reconhecidos só com maiúscula inicial")}
    minus = {norm_termo(t).lower() for t in lista("Termos reconhecidos só com minúscula inicial")}
    excl = {norm_termo(t).lower() for t in lista("Termos excluídos da verificação automática")}
    grupos = []
    sec3 = re.search(r"^## 3\..*?(?=^## 4\.)", txt, re.S | re.M)
    for m in re.finditer(r"^- \*\*(.+?)\.\*\*", sec3.group(0) if sec3 else "", re.M):
        grupo = []
        for t in re.split(r",\s*|\s+e\s+", m.group(1)):
            t = t.strip().strip("*")
            chave = norm_termo(t).lower()
            if not t or chave in excl:
                continue
            caixa = "maius" if chave in maius else "minus" if chave in minus else None
            grupo.append((t, padrao_termo(t, caixa)))
        if grupo:
            grupos.append(grupo)
    aval = [sem_acentos(w.lower()) for w in lista("Vocabulário avaliativo")] or AVALIATIVOS_RESERVA
    exc = [norm_termo(e).lower() for e in lista("Exceções ao vocabulário avaliativo")]
    return {"grupos": grupos, "aval": aval, "exc": exc}


LISTAS = ler_listas()


def termos_no_texto(texto):
    """[(termo, índice do grupo)] dos termos de alerta presentes num texto."""
    if not LISTAS:
        return []
    t = norm_termo(texto)
    achados, vistos = [], set()
    for g, grupo in enumerate(LISTAS["grupos"]):
        for nome, pad in grupo:
            chave = norm_termo(nome).lower()
            if chave not in vistos and pad.search(t):
                vistos.add(chave)
                achados.append((nome, g))
    return achados


# ---------------------------------------------------------------- neutralidade

def avaliativos_em(frase):
    lista = LISTAS["aval"] if LISTAS else AVALIATIVOS_RESERVA
    t = norm_termo(frase).lower()
    for e in (LISTAS["exc"] if LISTAS else []):
        t = t.replace(e, " ")
    achados = []
    for w in re.findall(r"[^\W\d_]+", t):
        for item in lista:
            if (item.endswith("*") and w.startswith(item[:-1])) or w == item:
                achados.append((w, item))
                break
    return achados


def vocabulario_do_autor(fontes):
    out = {}
    for fid, fonte in fontes.items():
        toks = set()
        for txt in corpo_das_paginas(fonte):
            toks |= set(re.findall(r"[^\W\d_]+", norm_termo(txt).lower()))
        out[fid] = toks
    return out


def verificar_neutralidade(frases, fontes, exigir_autor=True):
    """Com exigir_autor, só assinala o vocabulário avaliativo que o autor também usa (dossiê).
    Sem ele, assinala todo o vocabulário avaliativo fora de aspas (sebenta)."""
    voc = vocabulario_do_autor(fontes) if exigir_autor else {}
    avisos = []
    for ln, frase, _ in frases:
        palavras, donos = [], set()
        for w, item in avaliativos_em(frase):
            if exigir_autor:
                d = [fid for fid, v in voc.items()
                     if any((x.startswith(item[:-1]) if item.endswith("*") else x == item) for x in v)]
                if not d:
                    continue
                donos |= set(d)
            palavras.append(w)
        if palavras:
            avisos.append((ln, frase, palavras, sorted(donos)))
    return avisos


# ---------------------------------------------------------------- terminologia

def verificar_terminologia(vis, secs, frases, fontes, falhas_lista):
    conc = seccao(secs, "Conceitos")
    linhas_conc = vis[conc[0]:conc[1]] if conc else []
    grupos_registados = set()
    for l in linhas_conc:
        s = l.strip()
        if not s.startswith("|") or re.fullmatch(r"[|\-\s:]+", s):
            continue
        cel = [c.strip() for c in s.strip("|").split("|")]
        if cel and cel[0].lower() == "termo":
            continue
        grupos_registados |= {g for _, g in termos_no_texto(cel[0])}
        vazias = [k for k, c in enumerate(cel[1:], 2) if not c or c.startswith("[")]
        if len(cel) < 6 or vazias:
            falhas_lista.append(f"conceito \"{cel[0]}\" com colunas por preencher no quadro "
                                "(escrever \"não indicado no texto\" se for o caso)")
    nas_fontes = set()
    for fonte in fontes.values():
        texto = " ".join(corpo_das_paginas(fonte))
        nas_fontes |= {n for n, _ in termos_no_texto(texto)}
    usados, grupo_de = {}, {}
    for ln, frase, _ in frases:
        for nome, g in termos_no_texto(frase):
            usados.setdefault(nome, ln)
            grupo_de[nome] = g
    em_falta = sorted(n for n in usados if n in nas_fontes and grupo_de[n] not in grupos_registados)
    alheios = sorted(n for n in usados if n not in nas_fontes)
    return em_falta, alheios, usados


# ---------------------------------------------------------------- outros controlos

ERA = re.compile(r"\b[Ee]ra\s+(?:de\s+)?(?:C[ée]sar\s+|hisp[âa]nica\s+)?(?:de\s+)?(?:\d{3,4}\b|mil\b)")
FACTIVOS = re.compile(
    r"\b(?:mostra|mostram|demonstra|demonstram|prova|provam|revela|revelam|evidencia|evidenciam|"
    r"constata|constatam)\s+(?:já\s+|bem\s+)?que\b|\bcomo\s+(?:bem\s+)?(?:nota|notam|mostra|mostram|"
    r"demonstra|demonstram|revela|revelam|prova|provam)\b|\bcomo\s+bem\b|\bcom\s+razão\b",
    re.I)


def eras_na_fonte(fonte):
    out = []
    for p, txt in enumerate(fonte.brutas, 1):
        m = ERA.search(txt.replace("\n", " "))
        if m:
            out.append((p, m.group(0)))
    return out


# ---------------------------------------------------------------- modo dossiê

def mapa_fontes(lista):
    mapa = {}
    for item in lista:
        if "=" in item:
            k, v = item.split("=", 1)
            mapa[k.strip().upper()] = v.strip()
        else:
            mapa[None] = item
    return mapa


def mapa_chave_valor(lista):
    out = {}
    for item in lista:
        if "=" not in item:
            raise SystemExit(f"esperado ID=valor, recebido {item!r}")
        k, v = item.split("=", 1)
        out[k.strip().upper()] = v.strip()
    return out


def corridas(paginas):
    """[3,4,5,9] -> [(3,5),(9,9)]"""
    out = []
    for p in sorted(paginas):
        if out and p == out[-1][1] + 1:
            out[-1] = (out[-1][0], p)
        else:
            out.append((p, p))
    return out


def fmt(a, b):
    return f"pdf {a}" if a == b else f"pdf {a}-{b}"


def modo_dossie(args, fontes_arg):
    caminho = Path(args.dossie)
    linhas = caminho.read_text(encoding="utf-8").split("\n")
    vis = visiveis(linhas)
    secs = seccoes(vis)
    entradas, erros = ler_banco(linhas)
    falhas, avisos_n, ressalvas = 0, 0, 0

    def fonte_de(fid):
        cam = fontes_arg.get(fid) or (fontes_arg.get(None) if len(fontes_arg) == 1 else None)
        return fonte_para(cam) if cam else None

    for d in sorted({e["id"] for e in entradas if sum(x["id"] == e["id"] for x in entradas) > 1}):
        erros.append(f"{d}: identificador repetido no banco")
    definidos = {e["id"] for e in entradas}
    mencionados = set()
    for n, l in enumerate(vis):
        if not CAB.match(linhas[n]):
            mencionados |= {"C" + x for x in REF.findall(l)}
    for x in sorted(mencionados - definidos, key=lambda c: int(c[1:])):
        erros.append(f"{x}: mencionado no texto mas não definido no banco")

    for fid, espec in mapa_chave_valor(args.paginas).items():
        f = fonte_de(fid)
        if f:
            f.tabela = tabela_paginas(espec)

    # 1 e 2. citações e páginas
    print("CITAÇÕES E PÁGINAS")
    estados, prova = {}, defaultdict(set)
    sem_impressa = set()
    for e in entradas:
        fonte = fonte_de(e["fonte"])
        if not fonte:
            print(f"FALHA     {e['id']}  fonte {e['fonte']!r} sem ficheiro "
                  f"(usar --fonte {e['fonte']}=caminho)")
            estados[e["id"]] = "NÃO confirmada"
            falhas += 1
            continue
        iv = intervalo(e["pdf"])
        decl = set(range(iv[0], iv[1] + 1)) if iv else set()
        extras, aviso, grave = [], False, False
        if not LOCALIZADOR_APA.search(e["apa"]):
            extras.append("a referência APA não tem localizador (p., pp., para., cap. ou sec.)")
            aviso = True
        if len(e["citacao"].split()) >= 40:
            extras.append("40 ou mais palavras, entra em bloco na redação (APA 7)")
        nivel, pgs, av, em_falta = procurar(e["citacao"], fonte, decl)
        if nivel == 0:
            falhas += 1
            estados[e["id"]] = "NÃO confirmada"
            print(f"FALHA     {e['id']}  {e['apa']}")
            for seg in em_falta[:2]:
                print(f"          segmento \"{seg[:90]}{'...' if len(seg) > 90 else ''}\"")
                print(f"          {diagnostico(seg, fonte.i1)}")
            continue
        if nivel == 2:
            ressalvas += 1
            estados[e["id"]] = "confirmada com ressalva"
            if not any("atravessa" in a for a in av):
                extras.insert(0, "diferença de espaçamento, hifenização ou maiúsculas, "
                                 "conferir na página")
        else:
            estados[e["id"]] = "confirmada no texto extraído"
        if fonte.tem_paginas and pgs:
            prova[e["fonte"]] |= set(pgs)
            if decl and not set(pgs) <= decl:
                aviso = True
                extras.append(f"página PDF declarada {sorted(decl)}, o texto está em "
                              f"{sorted(set(pgs))}")
            # página impressa
            apa = paginas_apa(e["apa"])
            impressas, origens = set(), set()
            for p in sorted(set(pgs)):
                imp, orig = fonte.impressa(p)
                if imp:
                    impressas |= imp
                    origens.add(orig)
            if apa and impressas:
                if not apa <= impressas:
                    msg = (f"página impressa declarada {ordenar(apa)}, o texto está na "
                           f"p. {texto_paginas(impressas)} ({', '.join(sorted(origens))})")
                    extras.append(msg)
                    if origens <= {"lida no PDF", "tabela"}:
                        grave = True
                    else:
                        aviso = True
            elif apa and not impressas:
                sem_impressa.add(e["fonte"])
            local = fmt(min(pgs), max(pgs))
        else:
            local = "sem paginação na fonte"
        extras += av
        if av:
            aviso = True
        if grave:
            falhas += 1
            estados[e["id"]] += ", página impressa errada"
            etiqueta = "FALHA     "
        elif aviso:
            avisos_n += 1
            estados[e["id"]] += ", rever aviso"
            etiqueta = "AVISO     " if nivel == 1 else "RESSALVA  "
        else:
            etiqueta = "OK        " if nivel == 1 else "RESSALVA  "
        print(f"{etiqueta}{e['id']}  {local}  {e['apa']}"
              + (f"  [{'; '.join(extras)}]" if extras else ""))
    for fid in sorted(sem_impressa):
        print(f"AVISO     {fid}: números de página impressa não detetados no PDF. Páginas APA "
              f"não verificadas. Indicar a tabela com --paginas {fid}=pdf_inicial-pdf_final:pagina")
        avisos_n += 1

    # 3 e 4. cobertura e prova de leitura
    print("\nCOBERTURA E PROVA DE LEITURA")
    unidades = ler_unidades(vis)
    ambitos = ambitos_das_fichas(vis)
    for fid, espec in mapa_chave_valor(args.ambito).items():
        iv = intervalo("pdf " + espec)
        if iv:
            ambitos[fid] = iv
    por_ler = 0
    fontes_usadas = sorted({u["fonte"] for u in unidades if u["fonte"]} |
                           {e["fonte"] for e in entradas})
    for u in unidades:
        if not u["fonte"] or not u["pdf"]:
            print(f"ERRO      {u['id']}: o título da unidade tem de indicar a fonte e as páginas "
                  f"PDF, por exemplo (F1, p. 1-12, pdf 9-20)")
            erros.append(f"{u['id']}: unidade sem fonte ou páginas PDF")
            continue
        a, b = u["pdf"]
        if u["objetivos"] and not u["interroga"]:
            print(f"FALHA     {u['id']} serve {', '.join('O' + x for x in sorted(u['objetivos']))} e não "
                  "tem \"Interrogação do texto\" (estatuto dos enunciados e porquê da posição do autor)")
            falhas += 1
        if b - a + 1 > 15:
            print(f"AVISO     {u['id']} ({fmt(a, b)}): {b - a + 1} páginas numa só unidade. "
                  "Dividir por mudança de argumento")
            avisos_n += 1
        if u["ilegivel"]:
            print(f"AVISO     {u['id']} ({fmt(a, b)}) declarada ilegível")
            avisos_n += 1
            continue
        tem = bool(prova[u["fonte"]] & set(range(a, b + 1)))
        if not tem:
            if u["sem_cit"]:
                print(f"AVISO     {u['id']} ({fmt(a, b)}) sem citação, justificada como sem "
                      "passagem citável. Confirmar a justificação")
                avisos_n += 1
            else:
                fonte = fonte_de(u["fonte"])
                if fonte and fonte.tem_paginas:
                    print(f"FALHA     {u['id']} ({fmt(a, b)}) sem citação confirmada nas suas "
                          "páginas. Não conta como lida")
                    falhas += 1
    for fid in fontes_usadas:
        fonte = fonte_de(fid)
        if not fonte or not fonte.tem_paginas:
            print(f"INFO      {fid}: fonte sem paginação, cobertura não medida automaticamente")
            continue
        a, b = ambitos.get(fid, (1, fonte.n))
        ambito = set(range(a, min(b, fonte.n) + 1))
        cobertas, justificadas = set(), set()
        for u in unidades:
            if u["fonte"] == fid and u["pdf"]:
                r = set(range(u["pdf"][0], u["pdf"][1] + 1))
                cobertas |= r
                if u["sem_cit"] or u["ilegivel"]:
                    justificadas |= r
        for x, y in corridas(ambito - cobertas):
            print(f"POR LER   {fid} {fmt(x, y)} ({y - x + 1} pág.) sem unidade no dossiê")
            por_ler += y - x + 1
        for x, y in corridas(ambito - prova[fid]):
            if y - x + 1 > args.max_sem_prova:
                trecho = set(range(x, y + 1))
                if trecho <= justificadas | (ambito - cobertas):
                    continue
                print(f"FALHA     {fid} {fmt(x, y)}: {y - x + 1} páginas seguidas sem nenhuma "
                      "citação confirmada. Reler o troço e citar, ou justificar na unidade")
                falhas += 1
        print(f"INFO      {fid}: âmbito {fmt(a, min(b, fonte.n))}, {len(ambito & cobertas)} de "
              f"{len(ambito)} páginas com unidade, {len(prova[fid] & ambito)} com citação")

    # 5. arranjo
    print("\nARRANJO")
    banco = seccao(secs, "Banco de citações")
    excluir = [banco[:2]] if banco else []
    fontes_obj = {fid: fonte_de(fid) for fid in fontes_usadas if fonte_de(fid)}
    arr = [] if args.sem_arranjo else verificar_arranjo(prosa_para_arranjo(vis, excluir), fontes_obj)
    for ln, frase, (motivo, fonte_txt) in arr:
        print(f"AVISO     linha {ln}: {motivo}")
        print(f"          dossiê \"{frase[:110]}{'...' if len(frase) > 110 else ''}\"")
        print(f"          fonte  \"{fonte_txt}\"")
    avisos_n += len(arr)
    if not arr:
        print("OK        nenhuma frase da leitura copia a fonte ou lhe repete o molde")

    print("\nNEUTRALIDADE")
    neu = verificar_neutralidade(prosa_para_arranjo(vis, excluir), fontes_obj)
    for ln, frase, ws, donos in neu:
        print(f"AVISO     linha {ln}: vocabulário avaliativo do autor ({', '.join(donos)}) na voz do "
              f"dossiê, {', '.join(chr(34) + w + chr(34) for w in ws)}. Pôr entre aspas e atribuir, "
              "ou descrever sem o juízo")
        print(f"          \"{frase[:110]}{'...' if len(frase) > 110 else ''}\"")
    avisos_n += len(neu)
    if not neu:
        print("OK        nenhum juízo do autor passou para a voz do dossiê sem aspas")

    # 6. objetivos e articulação
    print("\nTERMINOLOGIA")
    if not LISTAS:
        print(f"INFO      {REF_DIR / 'terminologia.md'} não encontrado. Termos de alerta não verificados")
    falhas_term = []
    excl_conc = excluir + ([seccao(secs, "Conceitos")[:2]] if seccao(secs, "Conceitos") else [])
    em_falta, alheios, usados = verificar_terminologia(vis, secs, prosa_para_arranjo(vis, excl_conc),
                                              fontes_obj, falhas_term)
    for msg in falhas_term:
        print(f"FALHA     {msg}")
    falhas += len(falhas_term)
    for nome in em_falta:
        print(f"AVISO     \"{nome}\" usado no dossiê (linha {usados[nome]}) e presente na fonte, sem "
              "entrada no quadro de conceitos. Registar sentido no autor, época, âmbito e deslize")
    avisos_n += len(em_falta)
    for nome in alheios:
        print(f"AVISO     \"{nome}\" usado no dossiê (linha {usados[nome]}) mas ausente das fontes. "
              "Confirmar que não é anacronismo nem tradução silenciosa de um termo da fonte")
    avisos_n += len(alheios)
    if not falhas_term and not em_falta and not alheios:
        print("OK        termos historicamente situados registados no quadro de conceitos")

    print("\nOBJETIVOS E ARTICULAÇÃO")
    objetivos = ["O" + OBJ.match(l).group(1) for l in vis if OBJ.match(l)]
    if not objetivos:
        print("AVISO     nenhum objetivo definido (### O1. ...). A leitura não está orientada")
        avisos_n += 1
    mapa = seccao(secs, "Mapa dos objetivos")
    if objetivos and not mapa:
        print("FALHA     falta a secção \"Mapa dos objetivos\"")
        falhas += 1
    elif objetivos:
        linhas_mapa = vis[mapa[0]:mapa[1]]
        for o in objetivos:
            row = [l for l in linhas_mapa if re.match(rf"^\|\s*{o}\b", l.strip())]
            if not row:
                print(f"FALHA     {o} não aparece no mapa dos objetivos")
                falhas += 1
            elif not (REF.search(row[0]) or re.search(r"não cobert|não abord", row[0], re.I)):
                print(f"FALHA     {o}: a linha do mapa não tem citações nem diz que as fontes "
                      "não o cobrem")
                falhas += 1
            else:
                print(f"OK        {o} no mapa dos objetivos")
        servidos = set()
        for u in unidades:
            servidos |= {"O" + x for x in u["objetivos"]}
        for o in sorted(servidos - set(objetivos)):
            print(f"AVISO     unidades remetem para {o}, que não está definido")
            avisos_n += 1
    fichas = sorted({FICHA.match(l).group(1).upper() for l in vis if FICHA.match(l)})
    if len(fichas) >= 2:
        art = seccao(secs, "Articulação")
        if not art:
            print("FALHA     há várias obras e falta a secção \"Articulação entre obras\"")
            falhas += 1
        else:
            refs = set()
            for l in vis[art[0]:art[1]]:
                refs |= {"C" + x for x in REF.findall(l)}
            fontes_refs = {e["fonte"] for e in entradas if e["id"] in refs}
            if len(fontes_refs) < 2:
                print("FALHA     a articulação entre obras não cita mais de uma obra")
                falhas += 1
            else:
                print(f"OK        articulação com citações de {', '.join(sorted(fontes_refs))}")
            for f in sorted(set(fichas) - fontes_refs):
                print(f"AVISO     {f} não entra na articulação. Dizer porquê")
                avisos_n += 1

    print("\nTESTE DE COMPREENSÃO")
    if objetivos:
        teste = seccao(secs, "Teste de compreensão")
        if not teste:
            print("FALHA     falta a secção \"Teste de compreensão\" (perguntas feitas a partir do "
                  "texto e respondidas só com o dossiê, protocolo, secção 11)")
            falhas += 1
        else:
            linhas_teste = [l.strip() for l in vis[teste[0]:teste[1]] if l.strip().startswith("|")]
            for o in objetivos:
                rows = [l for l in linhas_teste if re.match(rf"^\|\s*{o}\b", l)]
                if not rows:
                    print(f"FALHA     {o} sem perguntas no teste de compreensão")
                    falhas += 1
                    continue
                if not any(re.search(r"conferida|divergente", r, re.I) for r in rows):
                    print(f"FALHA     {o}: o teste de compreensão não indica o resultado "
                          "(\"conferida\" ou \"divergente\")")
                    falhas += 1
                for r in rows:
                    cel = [c.strip() for c in r.strip("|").split("|")]
                    if re.search(r"divergente", r, re.I) and (len(cel) < 5 or cel[-1] in {"", "-"}):
                        print(f"AVISO     {o}: resposta divergente sem a correção feita na unidade")
                        avisos_n += 1
                if len(rows) < 3:
                    print(f"AVISO     {o}: {len(rows)} pergunta(s) no teste de compreensão, o "
                          "protocolo pede três")
                    avisos_n += 1
            print("OK        teste de compreensão presente")

    print("\nFICHAS E DATAÇÃO")
    fichas_txt, atual = defaultdict(list), None
    for l in vis:
        m = FICHA.match(l)
        if m:
            atual = m.group(1).upper()
            continue
        if l.startswith(("## ", "### ")):
            atual = None
        if atual:
            fichas_txt[atual].append(l)
    for f in sorted(fichas_txt):
        corpo = "\n".join(fichas_txt[f])
        for campo in ("Data de redação", "Contexto historiográfico"):
            if not re.search(rf"{campo}\.\s*\S", corpo):
                print(f"AVISO     {f}: falta o campo \"{campo}.\" na ficha")
                avisos_n += 1
    dossie_txt = "\n".join(vis)
    for fid, fonte in fontes_obj.items():
        eras = eras_na_fonte(fonte)
        if eras and not re.search(r"Era de C[ée]sar|Era hisp[âa]nica", dossie_txt, re.I):
            p, txt = eras[0]
            print(f"AVISO     {fid} pdf {p}: a fonte data pela era (\"{txt}\") e o dossiê não "
                  "regista a Era de César. Registar a data da fonte, o sistema e a data convertida")
            avisos_n += 1

    for msg in erros:
        print(f"ERRO      {msg}")

    # 7. estado
    apto = not (falhas or erros or por_ler)
    est = next((l for l in vis if l.strip().startswith("Estado.")), "")
    print()
    if "concluído" in est.lower() and not apto:
        print("ERRO      o dossiê declara-se concluído mas não está apto")
    if "concluído" in est.lower() and apto:
        reg = next((l for l in vis if l.strip().startswith("Verificação.")), "")
        m = re.search(r"(\d+) citações\. Falhas (\d+)", reg)
        if not m:
            print("AVISO     o dossiê declara-se concluído sem a linha \"Verificação.\" com o resumo do "
                  "verificador. Copiar a linha final desta saída para o dossiê")
            avisos_n += 1
        elif int(m.group(1)) != len(entradas) or int(m.group(2)) != falhas:
            print(f"ERRO      a linha \"Verificação.\" do dossiê ({m.group(0)}) não coincide com esta "
                  f"verificação ({len(entradas)} citações, falhas {falhas}). Voltar a correr e copiar")
            apto = False
    print(f"{len(entradas)} citações. Falhas {falhas}, ressalvas {ressalvas}, avisos {avisos_n}, "
          f"erros de estrutura {len(erros)}, páginas por ler {por_ler}.")
    print("Dossiê apto para a sebenta. Rever ainda os avisos." if apto else
          "Dossiê NÃO apto. Resolver falhas, erros e páginas por ler antes de o declarar concluído.")

    if args.marcar and entradas:
        for e in entradas:
            campos = [c.strip() for c in linhas[e["ln_cab"]].split("|")]
            sufixo = ""
            if len(campos) > 4 and ";" in campos[4]:
                sufixo = ";" + campos[4].split(";", 1)[1]
            linhas[e["ln_cab"]] = " | ".join(campos[:4] + [estados.get(e["id"], "?") + sufixo])
        caminho.write_text("\n".join(linhas), encoding="utf-8")
        print(f"Estados escritos em {caminho}.")
    return 0 if apto else 1


# ---------------------------------------------------------------- modo sebenta

# citações em aspas retas (4 ou mais palavras, porque as retas também marcam termos),
# angulares e curvas (3 ou mais palavras)
CIT_SEB = [(re.compile(r'"([^"\n]+)"'), 4), (re.compile(r"«([^»\n]+)»"), 3),
           (re.compile(r"“([^”\n]+)”"), 3)]
PAREN_LOC = re.compile(r"\(([^()]*?(?:\b(?:pp?\.|para\.|par\.|f\.|fl\.|fls\.|col\.|n\.º|secç?ão)|"
                       r"\d{1,3}\s*[:.,]\s*\d{1,3})[^()]*)\)")
SOBRESCRITOS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
NOTA_LINHA = re.compile(rf"^\s*[{SOBRESCRITOS}]+\s")
ENFASE = re.compile(r"\[ênfase acrescentada\]|\(ênfase no original\)", re.I)
SECCOES_SEBENTA = ("Esquema", "Essencial a reter", "Glossário", "Perguntas de autoavaliação",
                   "Referências")


def blocos_de_codigo(texto):
    return re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), texto, flags=re.S)


def citacoes_da_sebenta(bruto):
    """[(citação sem marcas, início, fim, texto em bruto)] no texto e nos blocos de citação."""
    out = []
    for rx, minimo in CIT_SEB:
        for m in rx.finditer(bruto):
            limpo = re.sub(r"\*\*|__|(?<!\w)[*_]|[*_](?!\w)", "", m.group(1))
            limpo = re.sub(rf"[{SOBRESCRITOS}]+", "", limpo)
            if len(limpo.split()) >= minimo:
                out.append((limpo, m.start(), m.end(), m.group(1)))
    for m in re.finditer(r"(?:^>.*\n?)+", bruto, flags=re.M):
        bloco = re.sub(r"^>\s?", "", m.group(0), flags=re.M).strip()
        if re.match(r"\**Atenção", bloco):
            continue
        locs = list(PAREN_LOC.finditer(bloco))
        if locs and locs[-1].end() >= len(bloco) - 3 and len(bloco.split()) >= 40:
            corpo = bloco[:locs[-1].start()].strip()
            out.append((re.sub(r"\*\*|__", "", corpo), m.start(), m.end(), corpo))
    return sorted(out, key=lambda c: c[1])


def modo_sebenta(args, fontes_arg):
    bruto = blocos_de_codigo(Path(args.sebenta).read_text(encoding="utf-8"))
    linhas = bruto.split("\n")
    entradas = []
    if args.banco:
        entradas, _ = ler_banco(Path(args.banco).read_text(encoding="utf-8").split("\n"))
    banco = [(e, n1(e["citacao"])) for e in entradas if "NÃO" not in e["estado"]]
    if not banco and not fontes_arg:
        raise SystemExit("o modo sebenta precisa de --banco dossie.md, de --fonte, ou de ambos")
    falhas, avisos = 0, 0

    def linha_de(pos):
        return bruto.count("\n", 0, pos) + 1

    print("CITAÇÕES")
    citacoes = citacoes_da_sebenta(bruto)
    for cit, ini, fim, cru in citacoes:
        linha = linha_de(ini)
        rot = f"linha {linha}  \"{cit[:70]}{'...' if len(cit) > 70 else ''}\""
        if "**" in cru or "__" in cru:
            print(f"FALHA     {rot}\n          negrito dentro de uma citação. A APA 7 só admite ênfase "
                  "em itálico seguida de [ênfase acrescentada]")
            falhas += 1
        elif re.search(r"(?<!\w)[*_]\w", cru) and not ENFASE.search(bruto[ini: fim + 120]):
            print(f"AVISO     {rot}\n          itálico dentro de uma citação sem [ênfase acrescentada] "
                  "nem (ênfase no original)")
            avisos += 1
        segs = [n1(s) for s in segmentos(cit)]
        if not segs:
            continue
        no_banco = next((e for e, t in banco if all(s in t for s in segs)), None)
        loc = PAREN_LOC.search(bruto[fim: fim + 200]) or PAREN_LOC.search(bruto[max(0, ini - 200): ini])
        if not no_banco:
            achado = None
            pg_seb = paginas_apa(loc.group(1)) if loc else set()
            for fid, cam in fontes_arg.items():
                fonte = fonte_para(cam)
                decl = {p for p in range(1, fonte.n + 1)
                        if (fonte.impressa(p)[0] or set()) & pg_seb}
                nv, pgs, _, _ = procurar(cit, fonte, decl)
                if nv:
                    achado = (fid, pgs, fonte)
                    break
            if achado and not args.banco:
                fid, pgs, fonte = achado
                imp, orig = set(), set()
                for p in set(pgs):
                    i, o = fonte.impressa(p)
                    if i:
                        imp |= i
                        orig.add(o)
                if not loc:
                    print(f"AVISO     {rot}\n          sem localizador junto da citação")
                    avisos += 1
                elif pg_seb and imp and not pg_seb <= imp and orig <= {"lida no PDF", "tabela"}:
                    print(f"FALHA     {rot}\n          a sebenta diz p. {ordenar(pg_seb)} e o texto "
                          f"está na p. {texto_paginas(imp)}")
                    falhas += 1
                else:
                    print(f"OK        {rot} [fonte {fid or ''}, pdf {min(pgs) if pgs else '-'}]")
            elif achado:
                print(f"AVISO     {rot}\n          fora do banco, mas existe na fonte "
                      f"{achado[0] or ''} (pdf {min(achado[1]) if achado[1] else '-'}). "
                      "Acrescentar ao banco do dossiê")
                avisos += 1
            else:
                print(f"FALHA     {rot}\n          não existe no banco nem na fonte")
                falhas += 1
            continue
        if not loc:
            print(f"AVISO     {rot} [{no_banco['id']}]\n          sem localizador junto da citação")
            avisos += 1
            continue
        pg_seb, pg_banco = paginas_apa(loc.group(1)), paginas_apa(no_banco["apa"])
        if pg_seb and pg_banco and not pg_seb <= pg_banco:
            print(f"FALHA     {rot} [{no_banco['id']}]\n          a sebenta diz p. "
                  f"{ordenar(pg_seb)} e o banco diz {no_banco['apa']}")
            falhas += 1
        else:
            print(f"OK        {rot} [{no_banco['id']}]")
        if len(cit.split()) >= 40 and bruto[ini] in "\"«“":
            print("          40 ou mais palavras entre aspas. Em APA 7 vai em bloco, sem aspas")
            avisos += 1

    # estrutura
    print("\nESTRUTURA")
    n_estrutura = avisos
    titulos = [(n, l) for n, l in enumerate(linhas) if re.match(r"^#{1,4}\s+\S", l)]
    falsos = [n for n, l in enumerate(linhas) if re.fullmatch(r"\s*\*\*[^*]{2,90}\*\*\s*", l)]
    for n in falsos:
        print(f"AVISO     linha {n + 1}: parágrafo só a negrito, \"{linhas[n].strip()[:60]}\". "
              "Usar um título estruturado (#, ##, ###)")
    avisos += len(falsos)
    if len(titulos) < 3:
        print("AVISO     menos de três títulos estruturados. As rubricas e as partes são títulos")
        avisos += 1
    for nome in SECCOES_SEBENTA:
        if not any(nome.lower() in l.lower() for _, l in titulos):
            print(f"AVISO     falta a secção \"{nome}\"")
            avisos += 1
    partes = [(n, l) for n, l in titulos if re.match(r"^#{2,3}\s+\d+\.", l)]
    for k, (n, l) in enumerate(partes):
        seguinte = next((m for m, _ in titulos if m > n), len(linhas))
        a, b = len("\n".join(linhas[:n])), len("\n".join(linhas[:seguinte]))
        if not any(a <= c[1] < b for c in citacoes):
            print(f"AVISO     linha {n + 1}: a parte \"{l.strip('# ')[:50]}\" não tem citação direta")
            avisos += 1
    sem_marcas = re.sub(r"\s+", " ", bruto)
    em_negrito = sum(len(m) for m in re.findall(r"\*\*([^*]+)\*\*", sem_marcas))
    if sem_marcas and em_negrito / len(sem_marcas) > 0.10:
        print(f"AVISO     {em_negrito / len(sem_marcas):.0%} do texto a negrito. O negrito deixa de "
              "destacar acima de um décimo")
        avisos += 1
    for n, l in enumerate(linhas):
        sem_cit = re.sub(r'"[^"]*"|«[^»]*»|“[^”]*”', " ", l)
        if re.search(r"(?<![\w\[])\[\d{1,3}\](?!\()", sem_cit):
            print(f"AVISO     linha {n + 1}: chamada de nota entre parênteses retos. Usar algarismo "
                  "sobrescrito (¹, ², ³), porque os parênteses retos são das interpolações")
            avisos += 1
        if NOTA_LINHA.match(l) and not (re.search(r"\([^()]*(?:\d{4}|s\.d\.)[^()]*\)", l)
                                         or re.search(r"não (?:é )?definido", l, re.I)):
            print(f"AVISO     linha {n + 1}: nota sem referência. Indicar a fonte do sentido, ou "
                  "dizer que a fonte não define o termo e registá-lo nas lacunas")
            avisos += 1

    if avisos == n_estrutura:
        print("OK        títulos, secções, notas e citações por parte")

    # prosa
    refs = next((n for n, l in titulos if "referências" in l.lower()), None)
    fim_refs = next((n for n, _ in titulos if refs is not None and n > refs), len(linhas))
    excluir = [(refs, fim_refs)] if refs is not None else []
    vis = [l if not re.match(r"^>", l) or re.match(r"^>\s*\**Atenção", l) else "" for l in linhas]
    frases = prosa_para_arranjo(vis, excluir)

    print("\nVOZ E NEUTRALIDADE")
    n_voz = 0
    for ln, frase, _ in frases:
        m = FACTIVOS.search(frase)
        if m:
            print(f"AVISO     linha {ln}: \"{m.group(0)}\" dá por verdadeiro o que introduz ou adere ao "
                  "autor. Usar só para factos afirmados, e um verbo neutro para interpretações")
            print(f"          \"{frase[:110]}{'...' if len(frase) > 110 else ''}\"")
            n_voz += 1
    for ln, frase, ws, _ in verificar_neutralidade(frases, {}, exigir_autor=False):
        print(f"AVISO     linha {ln}: vocabulário avaliativo na voz da sebenta, "
              f"{', '.join(chr(34) + w + chr(34) for w in ws)}. Pôr entre aspas e atribuir, ou "
              "descrever sem o juízo")
        n_voz += 1
    avisos += n_voz
    if not n_voz:
        print("OK        sem verbos factivos nem vocabulário avaliativo na voz da sebenta")

    fontes_obj = {fid: fonte_para(cam) for fid, cam in fontes_arg.items()}
    print("\nARRANJO E TERMINOLOGIA")
    if not fontes_obj:
        print("INFO      sem --fonte, o arranjo e os termos ausentes das fontes não são verificados")
    else:
        arr = [] if args.sem_arranjo else verificar_arranjo(frases, fontes_obj)
        for ln, frase, (motivo, fonte_txt) in arr:
            print(f"AVISO     linha {ln}: {motivo}")
            print(f"          sebenta \"{frase[:110]}{'...' if len(frase) > 110 else ''}\"")
            print(f"          fonte   \"{fonte_txt}\"")
        avisos += len(arr)
        if LISTAS:
            nas_fontes = set()
            for fonte in fontes_obj.values():
                nas_fontes |= {n for n, _ in termos_no_texto(" ".join(corpo_das_paginas(fonte)))}
            # o termo da nota é o que vem antes dos dois pontos (nota ou linha do glossário)
            cabecas = [re.sub(r"\*\*", "", l.strip()).split(":", 1)[0]
                       for l in linhas if NOTA_LINHA.match(l) or re.match(r"\s*- \*\*[^*]+:\*\*", l)]
            com_nota = {g for _, g in termos_no_texto("\n".join(cabecas))}
            # o termo que dá nome ao tema (título de nível 1) explica-se na sebenta inteira
            com_nota |= {g for _, g in termos_no_texto(" ".join(l for _, l in titulos if l.startswith("# ")))}
            vistos = {}
            for ln, frase, _ in frases:
                for nome, g in termos_no_texto(frase):
                    vistos.setdefault(nome, (ln, g))
            for nome, (ln, g) in sorted(vistos.items()):
                if nome not in nas_fontes:
                    print(f"AVISO     \"{nome}\" (linha {ln}) não aparece nas fontes. Confirmar que não é "
                          "anacronismo nem tradução silenciosa de um termo da fonte")
                    avisos += 1
                elif g not in com_nota:
                    print(f"AVISO     \"{nome}\" (linha {ln}) é termo de alerta e não tem nota nem "
                          "entrada no glossário")
                    avisos += 1
        if not arr:
            print("OK        nenhuma frase da sebenta copia a fonte ou lhe repete o molde")

    print(f"\n{len(citacoes)} citações na sebenta. Falhas {falhas}, avisos {avisos}.")
    print("Sebenta apta. Rever ainda os avisos." if not falhas else
          "Sebenta NÃO apta. Corrigir as falhas antes de entregar.")
    return 1 if falhas else 0


# ---------------------------------------------------------------- modo localizar

def modo_localizar(trecho, fontes_arg):
    for chave, caminho in fontes_arg.items():
        fonte = fonte_para(caminho)
        nome = chave or Path(caminho).name
        nv, pgs, av, _ = procurar(trecho, fonte, set())
        if nv:
            ress = "" if nv == 1 else " (com ressalva, conferir na página)"
            imp = []
            for p in sorted(set(pgs)):
                i, o = fonte.impressa(p)
                if i:
                    imp.append(f"p. {texto_paginas(i)} ({o})")
            local = ", ".join(map(str, sorted(set(pgs)))) if fonte.tem_paginas else "(sem paginação)"
            print(f"{nome}: encontrado em pdf {local}{ress}" + (f", {'; '.join(imp)}" if imp else ""))
        else:
            print(f"{nome}: não encontrado. " + diagnostico(trecho, fonte.i1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dossie", nargs="?", help="dossiê de leitura (.md)")
    ap.add_argument("--fonte", action="append", default=[], help="ID=caminho, ex. F1=obra.pdf")
    ap.add_argument("--marcar", action="store_true", help="escrever o estado de cada citação no banco")
    ap.add_argument("--ambito", action="append", default=[], help="ID=a-b, páginas PDF fornecidas")
    ap.add_argument("--paginas", action="append", default=[], help="ID=tabela de páginas impressas")
    ap.add_argument("--max-sem-prova", type=int, default=12,
                    help="máximo de páginas seguidas sem citação confirmada (12)")
    ap.add_argument("--sem-arranjo", action="store_true", help="não procurar arranjos")
    ap.add_argument("--sebenta", help="verificar as citações de uma sebenta contra o banco")
    ap.add_argument("--banco", help="dossiê com o banco de citações (modo sebenta)")
    ap.add_argument("--localizar", help="procurar um trecho nas fontes")
    args = ap.parse_args()
    fontes = mapa_fontes(args.fonte)

    if args.localizar:
        if not fontes:
            ap.error("indicar pelo menos uma --fonte")
        modo_localizar(args.localizar, fontes)
        return 0
    if args.sebenta:
        return modo_sebenta(args, fontes)
    if not args.dossie:
        ap.error("indicar o dossiê, ou usar --sebenta ou --localizar")
    if not fontes:
        ap.error("indicar pelo menos uma --fonte")
    return modo_dossie(args, fontes)


if __name__ == "__main__":
    sys.exit(main())

---
name: leitura-academica
description: Leitura integral, fiel e verificável das fontes de estudo de uma unidade curricular de História (obras, capítulos, artigos, resenhas, sebentas, manuais, fontes primárias, textos teóricos, quadros e mapas), orientada pelos objetivos da unidade e com prova de leitura em cada troço do texto. Produz o dossiê de leitura (objetivos decompostos, unidades, citações diretas confirmadas e localizadas, conceitos, cronologia, articulação entre obras e mapa dos objetivos) a partir do qual a skill sinteses-historia faz depois a sebenta. Usar quando o utilizador pedir para ler, analisar, estudar, fichar ou comparar documentos carregados, ou para preparar a leitura de um tema antes da sebenta. Não redige a sebenta.
---

# Leitura académica

Esta skill lê as fontes de um tema como as leria um estudante especialista em leitura, que não salta páginas, sabe o que procura e prova o que afirma. O resultado é o dossiê de leitura, que é a base da sebenta escrita depois com a skill sinteses-historia. Tudo o que esta leitura errar, omitir ou inventar passa para a sebenta, por isso o seu valor está na cobertura integral, na fidelidade e na verificação, e não no volume. Escrever em português europeu (AO 1990).

## Cinco compromissos

1. **Ler tudo o que foi fornecido.** Do princípio ao fim, sem amostragem. Os objetivos decidem a profundidade com que cada unidade é tratada, nunca se ela é lida. Uma unidade alheia aos objetivos lê-se na mesma e regista-se em poucas linhas, com a sua prova, porque pode definir um termo ou fixar uma ressalva de que outra parte depende.
2. **Dizer só o que o texto mostra.** Sobre a fonte há duas formas legítimas de afirmar. Ou a citação direta, registada no banco e confirmada pelo verificador, ou a leitura própria, que acrescenta o mecanismo, a ligação ou a distinção que a frase do autor não torna explícita. Reordenar, condensar ou trocar palavras da frase da fonte é arranjo e está proibido, e nesse caso cita-se ou desdobra-se o raciocínio. Conservar quem fala, com que certeza, em que âmbito e com que ressalvas. O conhecimento exterior só entra quando um passo não se compreende sem ele, verificado e rotulado como contexto externo.
3. **Ler com distância.** O leitor é perspicaz e neutro. Compreende o autor por dentro sem se deixar convencer por ele. Separa o facto afirmado da interpretação e do juízo de valor, capta as nuances que fixam a certeza e o âmbito (modalizadores, concessões, restrições, ironia, silêncios), não adota o vocabulário avaliativo do autor e pergunta, para cada tese central, contra quem o autor escreve, com que provas, a partir de que pressupostos, para quê e o que fica de fora. Interrogar não é refutar, e a resposta procura-se no texto. O método está no protocolo, secção 6.
4. **Respeitar a terminologia de cada época.** Cada termo que muda de sentido com o tempo (foral, concelho, cortes, ordens, Antigo Regime, liberalismo, cidadão, comunismo, fascismo, colónia) regista-se com o sentido que o autor lhe dá, a indicação de termo de época ou conceito do historiador, o âmbito e o deslize a evitar. Nunca se dá a um termo o sentido de outro tempo, nem se substitui o termo da fonte por um moderno sem o dizer. Os alertas estão em `references/terminologia.md`.
5. **Provar a leitura.** Cada unidade tem pelo menos uma citação confirmada nas suas páginas e nenhum troço longo do texto fica sem citação. Quem decide que o dossiê está concluído é o verificador, e não a impressão de quem leu.

## A tentação a vencer

Perante um texto longo, um modelo tende a ler o princípio com atenção, a passar depressa pelo meio e a completar o fim com o que já sabe do tema, e o resultado parece sólido porque está bem escrito. Esta skill está desenhada contra esse vício, e as regras seguintes não admitem exceção.

- **Plano antes da leitura.** Antes de ler o corpo, dividir todo o âmbito fornecido em unidades de cerca de doze páginas no máximo, por mudança de tema ou de argumento, e escrever esse plano no dossiê. Nenhuma página fica fora do plano.
- **Uma unidade de cada vez, a partir do texto.** Cada unidade lê-se no texto extraído, pelas suas páginas, numa leitura própria, mesmo que o anexo pareça estar todo no contexto, porque os anexos longos podem chegar truncados e uma leitura única dispersa a atenção. Nunca escrever uma unidade a partir da memória de uma leitura anterior.
- **Registo imediato.** A análise e as citações de cada unidade entram no dossiê logo que a unidade é lida, antes de passar à seguinte.
- **O meio vale o mesmo que as pontas.** As unidades centrais recebem a mesma atenção que a introdução e a conclusão, porque é nelas que o argumento se constrói. Uma conclusão do autor só se regista como tal depois de lido o desenvolvimento que a sustenta.
- **Visão de conjunto no fim.** A visão global, a articulação entre obras e o mapa dos objetivos só se escrevem depois de lida a última unidade.

## Fluxo

**1. Compreender os objetivos.** Pedir os objetivos do tema ou da unidade curricular (guia de estudo, plano da unidade curricular, enunciado do docente), se não vierem com as fontes. Decompor cada objetivo segundo `references/objetivos.md`, isto é, a operação pedida pelo verbo, o objeto, a delimitação, os conceitos que pressupõe, as perguntas de leitura e o que a sebenta terá de conseguir mostrar. Apresentar a decomposição no chat em poucas linhas. Se um objetivo for ambíguo ou exceder as fontes, perguntar antes de ler, porque um objetivo mal compreendido desorienta a leitura toda. Se não houver objetivos, propor objetivos provisórios a partir do que as fontes declaram fazer e marcá-los como provisórios.

**2. Aceder ao texto.** Extrair o texto de cada fonte para um ficheiro de trabalho, com uma quebra de página (`\f`) entre páginas, por exemplo com `pdftotext -enc UTF-8 obra.pdf obra.txt`. Se `pdffonts` mostrar que não há camada de texto, fazer OCR página a página e conferir na imagem as passagens citadas. O verificador lê os números de página impressos no PDF e avisa quando não os encontra. Em digitalizações com duas páginas por imagem, ou com estampas intercaladas, preparar a tabela de páginas (`--paginas`). Converter DOCX e EPUB em texto antes de os usar.

**3. Reconhecer e planear.** Percorrer o paratexto (ficha técnica, índice, introdução, conclusão, notas, bibliografia, quadros e mapas). Preencher a ficha documental de cada fonte e escrever o plano de unidades na tabela de cobertura, com o intervalo de páginas PDF de cada unidade e os objetivos que se espera servir. Identificar o género e a disciplina e carregar `references/generos-e-disciplinas.md`.

**4. Ler unidade a unidade.** Para cada unidade, ler as suas páginas e as notas de rodapé, responder às perguntas do protocolo (`references/protocolo.md`, secções 4 e 6), registar as citações no banco, com localizador, no momento em que são identificadas, e escrever a entrada da unidade, que indica os objetivos que serve, ou "nenhum". Ao terminar cada fonte, correr o verificador e resolver as falhas antes de passar à seguinte.

**5. Ler o conjunto.** Consolidar os conceitos (sentido no autor, termo de época ou conceito do historiador, âmbito), os factos e a cronologia, e os limites do documento. Com duas ou mais obras, escrever a articulação entre obras, objetivo a objetivo, segundo o protocolo, secção 9, depois de cada obra ter sido lida por si.

**6. Mapa dos objetivos.** Para cada objetivo, registar as unidades e as citações que o servem, o grau de cobertura (coberto, parcial, não coberto pelas fontes), as tensões entre o objetivo e o que as fontes dizem, e o que falta. O mapa é a passagem para a sebenta, e é a partir dele que a síntese constrói os núcleos.

**7. Verificar.** Correr o verificador (comandos abaixo). O dossiê só se declara concluído quando o verificador termina com "Dossiê apto para a sebenta", isto é, sem falhas, sem erros e sem páginas por ler. Os avisos resolvem-se um a um, e um aviso de arranjo resolve-se citando ou reescrevendo a partir do sentido. Depois, conferir por amostragem cinco afirmações da leitura própria contra a página indicada, escolhidas em unidades diferentes e incluindo unidades do meio. Em cada uma, confirmar também a neutralidade, isto é, que um juízo do autor não passou a facto nem ficou na voz do leitor, e que nenhuma ressalva se perdeu. Numa obra inteira ou em várias obras, se houver ferramenta para lançar um revisor separado, entregar-lhe o dossiê e as fontes para fazer esta conferência sem ver o raciocínio que produziu o dossiê.

**8. Entregar.** Entregar o dossiê como ficheiro `.md`, porque vai ser anexado na conversa da sebenta. No chat, dizer em poucas frases o estado de cobertura, o mapa dos objetivos em síntese e as pendências. Para um excerto curto ou uma pergunta pontual, responder no chat com o mesmo método, sem dossiê. Em obras longas, escrever o dossiê por partes e, se o trabalho for interrompido, deixar o localizador exato de retoma.

## Verificador

O verificador está em `scripts/verificar.py`, na pasta desta skill, e tem três modos.

```
python3 scripts/verificar.py dossie.md --fonte F1=obra.pdf --fonte F2=artigo.txt --marcar
python3 scripts/verificar.py --localizar "trecho a procurar" --fonte obra.pdf
python3 scripts/verificar.py --sebenta sebenta.md --banco dossie.md --fonte F1=obra.pdf
```

No dossiê, confirma cada citação no texto da fonte (tolerando hifenização, chamadas de nota e passagem de página), a página PDF e a página impressa da referência APA, a cobertura de todas as páginas do âmbito, a prova de leitura por unidade e por troço (por omissão, doze páginas seguidas sem citação confirmada dão falha), os arranjos, o mapa dos objetivos e a articulação entre obras. Para isso, o dossiê segue as convenções de `references/dossie-modelo.md`, sobretudo os títulos das unidades, que indicam a fonte e as páginas PDF. Uma unidade feita só de quadros ou mapas, sem passagem citável, leva a linha "**Sem passagem citável.**" seguida da razão, e o verificador mostra-a como aviso a confirmar. Uma unidade ilegível leva "[ilegível]" no título.

## Formato

Prosa encadeada com conectores, em frases completas e simples, nunca telegráfica. Antes de cada lista ou quadro, uma frase que diga para que serve. Aspas retas, citações nunca em itálico, sem travessões nem ponto e vírgula na prosa, e rótulos de campo terminados em ponto. Os rótulos de estatuto (leitura própria, inferência, contexto externo, juízo do leitor) são instrumento de trabalho do dossiê e não passam para a sebenta como rótulos. Se o utilizador fixar outro regime, prevalece o dele.

## Recursos

Os ficheiros seguintes carregam-se quando são precisos, e não por rotina.

- `references/objetivos.md` no passo 1.
- `references/protocolo.md` antes da primeira unidade.
- `references/generos-e-disciplinas.md` depois de identificar o género e a disciplina.
- `references/terminologia.md` antes da primeira unidade e sempre que surgir um termo de alerta.
- `references/citacoes-apa7.md` ao abrir o banco de citações.
- `references/dossie-modelo.md` ao criar o dossiê.
- `references/exemplos.md` perante passagens densas, dúvidas de fidelidade, objetivos difíceis ou articulação entre obras. Todos os excertos são simulados.

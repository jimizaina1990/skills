# Alterações às skills `leitura-academica` e `sinteses-historia`

As correções seguintes respondem aos pontos da análise em `analise/analise-critica-leitura-e-sinteses.md` (F1 a F11 para a leitura, E1 a E7 para a sebenta). As versões originais estão no commit "Importa as versões originais", para comparação.

## `sinteses-historia`

| Ponto | Correção | Ficheiros |
| --- | --- | --- |
| E1 | Novo modo "Sebenta da unidade curricular", que monta as sebentas de tema num só documento com índice, introdução, capítulos, cronologia, glossário e autoavaliação gerais. A extensão passa a seguir os objetivos (cerca de meia página a uma página por objetivo), em vez de duas a três páginas fixas. | SKILL.md |
| E2 | Eliminada a fórmula "Como bem a definia X". Regra única para a paráfrase, igual à da leitura (citação direta ou explicação própria, nunca arranjo, e nenhuma tese atribuída sem citação confirmada). Notas sempre com fonte, ou com a indicação de que a fonte não define o termo. Lista fechada de rótulos para as setas, alinhada com o protocolo, com "manifesta-se em" para a prova. | SKILL.md, anexos A, C e D |
| E3 | Negrito proibido dentro de citações. Ênfase em itálico com "[ênfase acrescentada]" ou "(ênfase no original)", como a APA 7 exige. Chamadas de nota em algarismo sobrescrito, para não colidir com os parênteses retos das interpolações. Remissão para os modelos completos de referência APA. | SKILL.md, anexo A |
| E4 | Exemplo-modelo reescrito. Títulos estruturados, uma citação confirmada por parte, citações gramaticais na frase, verbos neutros, ato de fala conservado, notas com fonte, esquema com rótulos da lista, revisão completa, e o objetivo sem citação confirmada passado para as lacunas em vez de tratado por citação indireta. O exemplo passa no verificador sem falhas nem avisos (teste de regressão). | anexo A |
| E5 | Títulos estruturados obrigatórios. Negrito seletivo (alarme acima de um décimo do texto). Notas de atenção em bloco de destaque, sem itálico, podendo levar citação. Citações em aspas angulares na sebenta. Frase de orientação sem fórmula fixa. Limite de quatro frases por parágrafo como alarme e não como regra. Glossário consolidado na revisão. | SKILL.md, anexos A e C |
| E6 | Nova secção de revisão com essencial, glossário utilizável como cartões e perguntas de autoavaliação por objetivo, sem resposta e com remissão para a parte, mais orientação de revisão espaçada. Formas de pergunta por verbo no anexo B. Guião de comentário de documento no anexo E. | SKILL.md, anexos A, B e E |
| E7 | O verificador passa a verificar a sebenta a sério (ver abaixo). | SKILL.md, verificar.py |
| Novo | Anexo E, sobre fontes primárias, datação (Era de César, estilos do ano, calendários, Hégira, numeração dos Salmos), documentos religiosos, imagens e guião de comentário. Regra para relatos religiosos e sobrenaturais. Tabela de verbos introdutores e de integração gramatical das citações no anexo D. | anexos D e E |

## `leitura-academica`

| Ponto | Correção | Ficheiros |
| --- | --- | --- |
| F1 | Campos "Data de redação" e "Contexto historiográfico" na ficha, com regras de origem e rotulagem, e proibição de usar o contexto para refutar. Exemplo E18. | SKILL.md, protocolo §2, modelo do dossiê, exemplos |
| F2 | Novo ficheiro de crítica de fontes (crítica externa e interna, tradição do texto, datação, unidades). Tabela de factos com data na fonte, sistema e data convertida. Exemplo E15. | critica-de-fontes.md, protocolo §7, modelo do dossiê |
| F3 | Terminologia religiosa (Igreja, heresia, Reforma e Contrarreforma, religiosidade popular, paganismo, mouro e muçulmano, santo e mártir, Inquisição, secularização). Géneros religiosos e regra para relatos sobrenaturais. Historiografia confessional e académica. Exemplo E16. | terminologia.md, generos-e-disciplinas.md, critica-de-fontes.md §4 |
| F4 | Protocolo de leitura de imagens e objetos. Lente de história da cultura e da arte. Termos de cultura e periodização. | critica-de-fontes.md §5, generos-e-disciplinas.md, terminologia.md |
| F5 | Termos de Antiguidade e de história extraeuropeia e colonial. Lente de história antiga. | terminologia.md, generos-e-disciplinas.md |
| F6 | Teste de compreensão obrigatório por objetivo, feito às cegas sobre o texto, e revisor separado obrigatório numa obra inteira quando houver ferramenta. O verificador falha sem ele. | SKILL.md passo 7, protocolo §11, modelo do dossiê |
| F7 | Mapa argumentativo da obra antes do plano de unidades. | SKILL.md passo 3, protocolo §3, modelo do dossiê |
| F8 | Novos géneros (capítulo de obra coletiva, entrada de dicionário, catálogo de exposição, edição de fontes, obra traduzida). Modelos APA para capítulo, vários volumes, artigo, entrada de dicionário, obra traduzida e reeditada, texto sagrado e clássico, documento pontifício, legislação, arquivo. Localizadores canónicos, de fólio e de coluna. | generos-e-disciplinas.md, citacoes-apa7.md |
| F9 | Regra para traduções (termo original quando a tradução decide o sentido) e proibição do arranjo por tradução. Exemplo E17. | SKILL.md, protocolo §5, exemplos |
| F10 | Verificador corrigido (ver abaixo). | verificar.py, terminologia.md §6 |
| F11 | Parcialmente. A sebenta da unidade curricular junta os temas, mas não há ainda um caderno persistente nem um modo de pergunta e resposta sobre o corpus. | SKILL.md da sinteses-historia |

## Verificador (`leitura-academica/scripts/verificar.py`)

- **Listas fora do código.** Os termos de alerta, as listas de caixa, os termos excluídos, o vocabulário avaliativo e as exceções são lidos de `references/terminologia.md` (secções 3 e 6), e um docente pode revê-los sem tocar no código.
- **Terminologia sem falsos positivos.** Palavra inteira ("liberal" já não apanha "liberalidade"), plurais regulares, grafias com e sem hífen tratadas como iguais (Contra-Reforma e Contrarreforma), caixa obrigatória para os termos que são também palavras correntes ou apelidos (Cortes, couto). Registo no quadro de conceitos por família de termos.
- **Neutralidade sem vocabulário técnico.** Mártir, Redentor, bárbaro, tirano, virtuoso e messiânico saem da lista, "despotismo esclarecido" e "virtude heroica" são exceções, e são assinaladas todas as palavras avaliativas de uma frase, e não só a primeira.
- **Localizadores.** Aceita versículos, divisões canónicas, fólios, colunas, números de secção e páginas em numeração romana (`--paginas F1=5-12:i`).
- **Dossiê.** Falha sem teste de compreensão por objetivo. Avisa quando a ficha não tem data de redação ou contexto historiográfico e quando a fonte data pela Era de César e o dossiê não o regista. Arranjo detetado também por oração dentro de frases compostas.
- **Sebenta.** Citações em aspas angulares, curvas e retas e em bloco, conferidas contra o banco e as fontes. Falha com negrito dentro de citações. Avisa sobre itálico sem indicação de ênfase, parágrafos só a negrito no lugar de títulos, secções obrigatórias em falta, partes sem citação direta, notas sem referência, chamadas de nota entre parênteses retos, excesso de negrito, verbos factivos e de adesão, vocabulário avaliativo, arranjo e termos de alerta sem nota ou ausentes das fontes.
- **Testes de regressão.** `python3 -m unittest discover -s scripts/testes -v`, a correr a partir da pasta da skill.

## Limites que ficam

- O detetor de arranjo é lexical. Não apanha a paráfrase profunda nem o arranjo por tradução de uma fonte noutra língua, que ficam a cargo das regras e do teste de compreensão.
- O teste de compreensão é verificado na forma (existe, tem resultado por objetivo), não na qualidade das perguntas.
- Não há caderno persistente da unidade curricular nem modo de pergunta e resposta sobre o corpus, que exigem uma arquitetura de ficheiros partilhada entre conversas.

## Depois do primeiro teste real (Tema 1, Johnson)

O primeiro dossiê real foi entregue como "apto" sem o estar: faltavam a interrogação do texto nas dezanove unidades, a coluna "Deslize a evitar" e um teste de compreensão segundo o protocolo (saiu um questionário com respostas-modelo). As citações estavam todas certas. Para que a declaração de "apto" deixe de depender da palavra do modelo:

- **leitura-academica.** A linha final da saída do verificador copia-se para o dossiê ("Verificação."), e nunca se declara apto sem ter corrido o verificador na conversa. O modelo do dossiê diz agora explicitamente que o teste de compreensão não é um questionário nem leva respostas-modelo.
- **verificar.py.** Num dossiê concluído, avisa se falta a linha "Verificação." e dá erro se os números dela não coincidirem com a verificação atual. Teste de regressão novo.
- **sinteses-historia.** Antes de escrever, corre o verificador sobre o dossiê e não confia no estado escrito no próprio dossiê.

## Depois da revisão da primeira sebenta real (Tema 1, Johnson)

A sebenta passou no verificador com 0 falhas, mas tinha erros graves que ele não via. O objetivo 14 era "corrigido", com base numa leitura estreita e na omissão de passagens da fonte. As teses a negrito diziam por outras palavras a citação seguinte (arranjo). As 145 citações de uma obra traduzida davam só o ano da tradução. Afirmavam-se dados exteriores e, na mesma frase, davam-se como "por confirmar". Uma omissão retirava a atribuição ("como alguns eruditos argumentam"). Havia relatos bíblicos na voz da sebenta, nomes exteriores às fontes, e o esquema não passou na exportação. Mudanças:

- **sinteses-historia, fluxo.** Cinco etapas: compreender os objetivos; dossiê verificado; leitura do dossiê objetivo a objetivo, com regresso à fonte e plano de síntese; redação; revisão separada. Entrega em Markdown; o documento final só depois de validada, num passo à parte que pode correr noutra conversa e com outro modelo.
- **sinteses-historia, princípios.** Especialista que explica e argumenta. Citar com a extensão que o sentido exige, incluindo citações em bloco, sem mínimo nem máximo por parte. A tese enuncia-se com a própria citação. Os objetivos interpretam-se, não se corrigem. Afirmar ou pôr nas lacunas, nunca as duas coisas. Conhecimento exterior só perante falha flagrante, numa caixa "Fora das fontes" com referência.
- **sinteses-historia, quadros e extensão.** Quadros de contraposição e de conceitos. Extensão pela profundidade do objetivo, sem quota de páginas, e aviso obrigatório de cortes.
- **sinteses-historia, anexos.** Anexo A com modelos de bloco, quadros e caixa, e exemplo corrigido (tese pela citação). Anexo B com "Ler o enunciado" e "Profundidade". Anexo C distingue nota de atenção e caixa "Fora das fontes". Anexo D com citações longas, omissões e o vício da tese anunciada por paráfrase.
- **APA 7 confirmada nas páginas oficiais da APA** (a 7.ª edição continua em vigor):
  - reticências sem parênteses retos e quatro pontos entre frases;
  - [*sic*] em itálico;
  - alterações que não se indicam;
  - blocos;
  - obras traduzidas com os dois anos;
  - fontes secundárias com parcimónia;
  - tradução própria como paráfrase;
  - textos religiosos tratados como livros.

  As fontes estão listadas no fim de `citacoes-apa7.md`.
- **leitura-academica, perda do meio.** Varredura por objetivo depois da última unidade, com a nova procura por tema, registada no dossiê. O verificador compara a densidade de citações do terço central com a das pontas.
- **verificar.py.**
  - Novo modo `--procurar`: BM25 lexical sobre raízes; com `--banco`, diz o que já está citado e em que unidade.
  - Na sebenta: falha para obras traduzidas sem os dois anos.
  - Na sebenta, avisos para:
    - omissões que retiram atribuição, modalizador, negação ou restrição;
    - reticências entre parênteses retos;
    - [sic] em redondo;
    - blocos curtos, com aspas ou com ponto depois do parêntese;
    - tese a negrito parafraseada das citações da parte;
    - objetivo corrigido;
    - "por confirmar" fora das lacunas;
    - nomes próprios ausentes das fontes;
    - conteúdo embebido e esquema vazio.
  - Aceita os `\[ \]` da exportação de documentos.
  - No dossiê: ano duplo, varredura por objetivo e densidade do meio.
  - Onze testes de regressão novos (22 no total).
- **Resultado no material real.**
  - Sebenta do Tema 1: de "0 falhas, 1 aviso" para 1 falha (as citações sem o ano original) e 21 avisos, entre os quais o objetivo corrigido, quatro teses parafraseadas, a omissão da atribuição, as afirmações por confirmar e "Povos do Mar".
  - Dossiê: 1 falha (o ano duplo nas 231 citações) e o aviso da varredura em falta.

Limites que ficam: a deteção da tese parafraseada e dos nomes exteriores é lexical; a primeira não apanha paráfrases com sinónimos e a segunda assinala também grafias portuguesas de nomes da fonte. A procura por tema não é semântica. A revisão separada contra as fontes continua a ser indispensável.

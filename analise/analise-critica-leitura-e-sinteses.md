# Análise crítica das skills `leitura-academica` e `sinteses-historia`

Data da análise. 2026-10-07. Objeto. As versões entregues em `leitura-academica_2.zip` e `sinteses-historia_2.zip`. Finalidade declarada pelo utilizador. Uma ferramenta do tipo Gemini Notebook (antigo NotebookLM) para Ciências Sociais, sobretudo História, Cultura e Religião, destinada a estudantes do ensino superior português.

Estado. As correções foram aplicadas às skills em `skills/`, e a correspondência entre cada ponto desta análise e a alteração feita está em `skills/CHANGELOG.md`.

## 0. Método, convenções e limites

Li integralmente os catorze ficheiros das duas skills, incluindo o verificador (`scripts/verificar.py`, 1200 linhas), e corri o verificador sobre casos sintéticos construídos para História, Religião e Cultura. Os casos e o guião de reprodução estão em `analise/testes-verificador/`.

As citações das skills indicam o ficheiro e a linha, por exemplo (sinteses-historia/SKILL.md, l. 129). As citações de literatura seguem a APA 7. Só cito diretamente frases cuja formulação confirmei por pesquisa de expressão exata. A rede desta sessão bloqueou o acesso direto a `apastyle.apa.org`, `w3.org`, `aclanthology.org` e `imprensanacional.pt`, pelo que não abri os PDF originais. Onde a frase ficou confirmada mas a página não, escrevo "[página por confirmar]" em vez de a inventar. Autores que pensei citar (Bloch, Febvre, Panofsky, Williams, Delehaye, Howard) ficaram de fora, porque não consegui confirmar a formulação exata, e não os substituí por paráfrases.

## 1. Veredicto

As duas skills formam um circuito sério contra a alucinação, com uma ambição rara de fidelidade (banco de citações verificado, prova de leitura, distinção de vozes, modalizadores, termo de época e conceito do historiador). Isto é uma vantagem real sobre o Gemini Notebook, que cita passagens mas não verifica páginas impressas nem proíbe o arranjo.

Mas o conjunto não é, nem de perto, uma ferramenta do tipo Gemini Notebook. É uma linha de montagem para um único produto, a ficha de tema, e tem quatro defeitos de fundo.

1. **A leitura está calibrada para a história política portuguesa dos séculos XII a XX.** Religião, Cultura, Antiguidade e história não portuguesa ficam sem terminologia, sem géneros e com um verificador que gera falsos positivos (vocabulário religioso técnico tratado como juízo de valor) e falsos negativos (anacronismos religiosos que passam sem aviso).
2. **A leitura desliga a obra do seu tempo historiográfico.** A proibição de conhecimento exterior, correta contra a invenção, impede o dossiê de assinalar que uma obra está datada, é confessional ou foi superada, que é o erro mais grave que um estudante pode aprender.
3. **A síntese contradiz-se e o exemplo-modelo viola as suas próprias regras e a APA 7.** Como o modelo é o que o sistema imita, os erros reproduzem-se em todas as sebentas.
4. **O produto final, a sebenta, não é verificado naquilo que mais importa.** O verificador em modo sebenta só confere citações entre aspas retas. Uma citação inventada em aspas angulares e outra adulterada em aspas curvas passaram, e o resultado foi "Sebenta apta." (secção 3.2, E7).

## 2. `leitura-academica`, do ponto de vista de um leitor especialista de livros e manuais de História

### 2.1 O que está bem e deve ficar

A regra contra a leitura desigual tem fundamento empírico. Liu et al. (2024) mostraram que, nos modelos de linguagem, "performance is often highest when relevant information occurs at the beginning or end of the input context" (p. 157). A skill responde a isso com uma regra explícita, "O meio vale o mesmo que as pontas." (leitura-academica/SKILL.md, l. 25), e com a contagem de páginas sem citação no verificador. A proibição do arranjo, "Reordenar, condensar ou trocar palavras da frase da fonte é arranjo e está proibido" (leitura-academica/SKILL.md, l. 13), a separação entre facto, interpretação e juízo (protocolo.md, secção 6) e a pergunta "Contra quem escreve?" (protocolo.md, l. 106) são o que um bom orientador exige a um estudante de licenciatura. Nada disto deve ser enfraquecido.

### 2.2 Fragilidades

**F1. A obra fica fora do seu tempo historiográfico.** A ficha documental pede "Autor, título, edição e ano disponíveis" (protocolo.md, l. 15), mas não pede a data da primeira edição nem a da redação, e o ficheiro de APA não prevê a dupla data das obras reeditadas (ano original/ano da edição lida). Ao mesmo tempo, a skill proíbe o que permitiria situar a obra: "Afirmações sem nota nem fonte indicada registam-se como afirmações do autor, sem as reforçar nem as corrigir de memória" (generos-e-disciplinas.md, l. 11), e "Não confrontar com literatura que não foi carregada" (protocolo.md, l. 153). O resultado é que uma história eclesiástica confessional do início do século XX, ou um manual escolar do Estado Novo sobre os "Descobrimentos", entra no dossiê com o mesmo estatuto de atualidade que uma monografia de 2020. A neutralidade de leitura protege contra o juízo, mas não substitui a historicização da própria historiografia, que é a primeira competência que um docente de História avalia. Proposta. Uma camada "contexto historiográfico" com campos obrigatórios (data de redação, edição lida, corrente ou escola, receção conhecida), alimentada apenas pelos materiais da unidade curricular ou por obras de referência carregadas, e rotulada como tal.

**F2. A crítica de fontes primárias não chega para o comentário de documento.** O parágrafo dedicado à fonte primária (generos-e-disciplinas.md, l. 25) é correto mas genérico. Falta tudo o que é técnico, isto é, crítica externa e interna, tradição documental (original, cópia, traslado, pública-forma), data crónica e data tópica, eras e calendários, estilos de início do ano, metrologia e moeda, abreviaturas e língua do documento. O risco é concreto. Os diplomas portugueses foram datados pela Era de César até à reforma de D. João I (Arquivo Nacional Torre do Tombo, s.d.), e um documento datado "Era de 1422" é de 1384. A regra "Não completar datas nem nomes de memória" (protocolo.md, l. 119) é boa, mas, sem uma coluna para o sistema de datação, o modelo regista 1422 como ano e o erro passa intacto para a sebenta. O mesmo vale para a numeração dos Salmos (a da Vulgata e a hebraica diferem numa unidade em grande parte do Saltério) e para as datas da Hégira. Proposta. Um módulo de crítica de fontes, com a tabela de factos alargada a "data na fonte, sistema, data convertida, fonte da conversão".

**F3. Religião sem instrumentos.** O ficheiro de terminologia tem quatro secções, "Idade Média portuguesa", "Época Moderna", "Época Contemporânea" e "Historiografia e teoria" (terminologia.md, l. 24, 35, 45 e 57), e o único termo religioso da lista é o grupo "Cristão-novo, converso, marrano" (l. 41). Faltam os pares que mais se leem com o sentido errado, como heresia e ortodoxia, Reforma católica e Contrarreforma, religiosidade popular, superstição, paganismo (termo polémico cristão), cristandade e cristianismo, padroado, secularização e laicidade, Igreja como instituição e igreja como edifício. Faltam os géneros religiosos (hagiografia, sermão, catecismo, constituições sinodais, visitações, processos inquisitoriais, cartas missionárias edificantes, apologética). Falta uma regra para os relatos sobrenaturais, que nunca podem passar à voz do dossiê como facto nem ser desqualificados, e falta a distinção entre história eclesiástica confessional e história religiosa. A lente de teologia e estudos de religião (generos-e-disciplinas.md, l. 35) tem três frases para tudo isto.

O verificador agrava o problema, porque a lista de "vocabulário avaliativo" (verificar.py, l. 617-622) inclui raízes como "martir", "redentor", "messianic", "heroi", "barbar", "tiran", "virtuos" e "esclarecid". No teste, "mártires de Marrocos", "Redentor", "bárbaros" e o conceito historiográfico "despotismo esclarecido" foram assinalados como juízos de valor a pôr entre aspas. Em sentido inverso, "Contrarreforma" e "religiosidade popular" foram usados no dossiê sem existirem na fonte e o verificador respondeu "OK termos historicamente situados registados no quadro de conceitos", porque a lista de termos (verificar.py, l. 653-670) não tem um único termo religioso.

**F4. Cultura sem protocolo para imagem, objeto e obra.** O protocolo lê "Quadros, gráficos e mapas" (protocolo.md, secção 8), mas não lê pinturas, gravuras, iconografia religiosa, arquitetura, ex-votos, fotografia, literatura ou música como fontes. Para História da Cultura e da Arte e para História Religiosa, isto deixa de fora o tipo de fonte que os programas mais usam. Faltam também os conceitos culturais de alerta (Renascimento, Humanismo, Barroco, Luzes, Romantismo, cultura popular e cultura erudita, civilização, e a própria designação "Idade Média", cunhada depois).

**F5. Terminologia portuguesa e sem Antiguidade.** Não há secção de Antiguidade (pólis, cidadania antiga, democracia ateniense, escravatura, *religio* e *superstitio*, romanização) nem de história europeia ou extraeuropeia não portuguesa. A "democracia" só aparece com o sentido oitocentista (terminologia.md, l. 50). Um estudante de História Antiga, de História do Islão ou de História de África não recebe alertas nenhuns.

**F6. A prova de leitura mede presença, não compreensão.** O verificador confessa-o, "O que não verifica / A fidelidade do sentido, a qualidade da explicação e a correção do OCR" (verificar.py, l. 33-35). Com uma falha automática acima de doze páginas sem citação, o incentivo é encontrar uma frase citável por troço, e isso faz-se sem compreender o argumento. A própria skill descreve o vício no exemplo E11, mas a única defesa forte, o revisor separado, é condicional, "se houver ferramenta para lançar um revisor separado" (leitura-academica/SKILL.md, l. 42). Proposta. Tornar obrigatória uma prova cega por unidade, em que se geram perguntas a partir do texto, se responde só com o dossiê e se relê a unidade quando as respostas divergem.

**F7. O plano por páginas ignora a arquitetura da obra.** A regra de "cerca de doze páginas no máximo" (leitura-academica/SKILL.md, l. 22) é um bom limite operativo, mas a leitura especializada começa por um mapa funcional da obra, que diz que capítulos formulam a tese, quais apresentam a prova, quais são digressão ou síntese. A ficha regista "O que o documento declara sobre si" (dossie-modelo.md, l. 50), mas não há mapa argumentativo antes das unidades, e é ele que permite distribuir a profundidade com critério.

**F8. Manuais universitários coletivos e APA reduzida ao livro.** O ficheiro de APA dá uma única estrutura de referência, "Estrutura de um livro, Apelido, I. (ano). *Título da obra* (edição). Editora." (citacoes-apa7.md, l. 35). Os textos que um estudante português mais lê são capítulos de obras coletivas dirigidas (a *História de Portugal* dirigida por José Mattoso, a *História Religiosa de Portugal* dirigida por Carlos Moreira Azevedo), artigos de revista, entradas de dicionário, obras traduzidas e reeditadas, legislação e documentos de arquivo. Nenhum destes modelos existe. Para Religião falta ainda a regra da APA para obras de numeração canónica, que se citam por livro, capítulo e versículo, por exemplo (King James Bible, 1769/2017, Matthew 22:39), e não por página (American Psychological Association [APA], 2020, secção 8.28). O verificador só aceita como localizador "p.", "pp.", "para.", "cap." e "sec." (verificar.py, l. 330), e por isso dá aviso a qualquer citação por versículo, fólio ("fl. 23v") ou coluna (como na *Patrologia Latina*), como o teste confirmou.

**F9. Traduções e arranjo entre línguas.** Grande parte da bibliografia de História lê-se em francês, inglês e espanhol, ou em tradução portuguesa com escolhas terminológicas que importam (*mentalités*, *longue durée*, *Entzauberung der Welt*). A skill não manda registar o termo original quando a tradução decide o sentido. E o detetor de arranjo compara palavras e moldes na mesma língua (verificar.py, l. 569-612), pelo que a tradução quase literal de uma frase francesa apresentada como leitura própria, que é a forma mais comum de arranjo com fontes estrangeiras, passa sem aviso.

**F10. Defeitos técnicos do verificador.** Os testes de `analise/testes-verificador/` mostraram o seguinte.

| Defeito | Caso de teste | Resultado |
| --- | --- | --- |
| Termo por prefixo, sem fronteira de palavra | "liberalidade régia" | aviso de "liberalismo" |
| Homografia | "os cortes de pessoal" | aviso de "Cortes" |
| Apelido lido como instituição | "Diogo do Couto" | aviso de "couto" |
| Sentido teológico | "regeneração batismal" | aviso de "Regeneração" |
| Palavra corrente | "conjuntura de tensão" | aviso de "conjuntura" |
| Conceito historiográfico como juízo | "despotismo esclarecido" | aviso de neutralidade |
| Vocabulário religioso técnico como juízo | "mártires", "Redentor", "bárbaros" | aviso de neutralidade |
| Localizador canónico ou de arquivo | "Mt 5, 3", "fl. 23v" | aviso de localizador em falta |
| Anacronismo religioso | "Contrarreforma" ausente da fonte | nenhum aviso |
| Um só juízo por frase | "esclarecido" e "mártires" na mesma frase | só o primeiro é assinalado |

Há ainda limites de desenho, como a tabela de páginas (`--paginas`) aceitar apenas algarismos árabes, o que deixa sem mapeamento os prefácios em numeração romana, e as listas de termos e de juízos estarem escritas no código, em vez de virem dos ficheiros de referência por disciplina, onde um docente as poderia rever.

**F11. Não há caderno.** Cada tema relê as mesmas obras, o dossiê viaja como anexo `.md` para outra conversa e não existe registo persistente de fontes, texto extraído, banco de citações e glossário da unidade curricular. É aqui que a distância para o Gemini Notebook é maior (secção 4).

## 3. `sinteses-historia`, do ponto de vista da produção textual e editorial de sebentas universitárias

### 3.1 O que está bem e deve ficar

A pergunta-filtro "Isto ajuda o estudante a compreender e a recordar o essencial deste tema?" (sinteses-historia/SKILL.md, l. 10), a recusa da escrita telegráfica, as notas de atenção sobre confusões típicas (anexo C), o alinhamento das partes com os objetivos e a secção de lacunas são decisões editoriais certas. O anexo C, em particular, é material didático de qualidade.

### 3.2 Fragilidades

**E1. O género está mal definido.** O que a skill produz é uma ficha de tema, "um tema completo com vários textos dá cerca de duas a três páginas" (sinteses-historia/SKILL.md, l. 183), entregue em documentos separados, "Fazer um documento por tema." (l. 177). Uma sebenta universitária é um objeto editorial da unidade curricular, com índice, introdução, capítulos, glossário geral, cronologia geral, bibliografia geral e, idealmente, autoavaliação. Falta um modo de montagem da sebenta da unidade curricular que junte as fichas, normalize as notas e consolide glossário, cronologia e referências.

**E2. Contradições internas.** O sistema dá ordens incompatíveis, e um modelo resolve-as ao acaso.

- **Neutralidade contra adesão.** A skill determina que "A síntese expõe as posições dos autores como posições, e não como factos, e não adere a nenhuma nem a combate." (sinteses-historia/SKILL.md, l. 26), mas dá como fórmula-modelo de integração "Como bem a definia X, ..." (l. 110; também anexo-d-registo-academico.md, l. 11). O advérbio "bem" é adesão.
- **Só as fontes, ou definições próprias.** "Só o que está nas fontes" (sinteses-historia/SKILL.md, l. 14) e "As definições vêm sempre dos autores estudados." (anexo-c-notas-e-confusoes.md, l. 3), com a regra "Se o autor pressupõe um conceito sem o definir, não inventar uma definição." (anexo-c, l. 15), chocam com "Quando a fonte não define o termo, a nota dá uma explicação curta e simples, sem a atribuir ao autor." (anexo-a-modelo-e-exemplo.md, l. 19). O exemplo segue o anexo A, e cinco das suas oito notas ([1], [2], [4], [6] e [8]) são definições sem fonte.
- **Brevidade contra profundidade.** "Duas a três páginas" para vários textos (l. 183) não cabem num modelo que exige, por parte, frase de orientação, parágrafo, lista, parágrafo de retoma, nota de atenção e notas de rodapé, e que exige ainda o porquê de cada tese central, "contra que interpretação escreve, em que provas se apoia e o que deixa por explicar" (l. 26). Um objetivo com o verbo "problematizar" não se cumpre em dez frases.
- **Paráfrase.** A leitura proíbe "condensar" a frase da fonte (leitura-academica/SKILL.md, l. 13), mas a síntese só pede que "A paráfrase não é apenas o texto original com sinónimos ou frases reordenadas." (sinteses-historia/SKILL.md, l. 163). A regra da síntese é mais fraca precisamente no produto que o estudante lê.
- **Rótulos das setas.** O anexo A fixa os rótulos (anexo-a, l. 31), e o próprio esquema do exemplo usa "implica" e "cede perante", que não constam da lista (anexo-a, l. 144-147).

**E3. APA 7 violada por regra.** A skill manda pôr a negrito, "dentro das citações, as palavras que o estudante deve reter" (sinteses-historia/SKILL.md, l. 129), e repete que as citações "podem ter a negrito as palavras decisivas" (l. 130). Na APA 7, a ênfase acrescentada a uma citação faz-se em itálico e assinala-se logo a seguir com "[emphasis added]", em português "[ênfase acrescentada]" (APA, 2020, secção 8.31). O negrito sem indicação altera a citação sem o dizer, e o exemplo fá-lo em duas citações (anexo-a, l. 86 e 102). Como as regras da própria skill proíbem o itálico nas citações, a forma correta é impossível dentro dela. Outros desvios do exemplo são o título da obra na referência sem itálico, contra a regra da leitura, "O itálico existe só no título, como a norma exige." (citacoes-apa7.md, l. 35), e a numeração das notas entre parênteses retos ([1], [2]), que colide com a convenção das interpolações dentro de citações ([sic], [...], [O]) e com os identificadores do dossiê ([C01]).

**E4. O exemplo-modelo ensina os erros que a skill quer impedir.** O anexo A diz que o exemplo "serve de modelo de forma, de extensão e de registo" (anexo-a, l. 47). Por isso, cada defeito dele multiplica-se.

- **Citação mal integrada.** A citação é introduzida por "Como nota o autor," e continua com "isto é, que não se admitia o veto (art. 112.º, I)" (anexo-a, l. 86). O "que" depois de "isto é" pertence a uma oração regente que a citação cortou, e a frase resultante é agramatical.
- **Verbos factivos.** "Homem mostra que esta deslocação se manifesta em dois planos" (anexo-a, l. 83), "Como nota o autor" (l. 86), "revela já, segundo o autor" (l. 85). "Mostrar", "notar" e "revelar" pressupõem a verdade do que introduzem e transformam a interpretação do autor em facto, contra a regra da linha 26. O registo académico precisa de uma tabela de verbos introdutores (afirma, sustenta, interpreta, admite, nega, matiza) e de uma regra para os factivos.
- **Mudança do ato de fala.** No anexo A, a citação do deputado começa por "acordou em" (anexo-a, l. 102), isto é, o deputado relata um acordo. O anexo D introduz a mesma passagem com "defendia que importava" (anexo-d, l. 25), o que a transforma na defesa de uma posição. Relatar um acordo e defender uma posição não são o mesmo ato.
- **Parte sem citação direta.** A parte 3 é inteiramente citação indireta, "**Segundo Homem, o vocabulário dos procuradores cede lugar ao dos deputados**" (anexo-a, l. 121), e as lacunas admitem que a página está incerta, "A passagem sobre a representação política situa-se entre as pp. 42 e 43, sem confirmação da página exata." (l. 168). Apesar disso, "pp. 42-43" aparece seis vezes no exemplo, no texto, nas notas, no esquema e no essencial a reter, como se estivesse confirmado (anexo-a, l. 121, 126, 130, 134, 146 e 156).
- **Prova transformada em consequência.** Na parte 1, a ausência de sanção real é uma manifestação da deslocação da soberania, isto é, prova. No esquema passa a ser uma implicação dela ("N -->|implica| S", anexo-a, l. 147). É exatamente o erro que a skill manda evitar, "As setas do esquema dizem o que o texto sustenta" (sinteses-historia/SKILL.md, l. 162).
- **Termo de alerta sem nota.** A síntese escreve na sua própria voz "no quadro da monarquia absoluta" (anexo-a, l. 81), quando a terminologia avisa, a propósito de absolutismo e monarquia absoluta, que são "Termos sobretudo posteriores, e cujo alcance real é discutido pelos historiadores" (terminologia.md, l. 38), e o controlo final exige nota de rodapé na primeira ocorrência de cada termo historicamente situado (sinteses-historia/SKILL.md, l. 159).

**E5. Formatação e acessibilidade.** No exemplo, todos os títulos, do título do tema às secções e partes, são parágrafos a negrito e não títulos estruturados (anexo-a, l. 61, 65, 79, 100, 119, 138, 150, 159 e 163). Isso impede o índice automático, a navegação por secções, a exportação para Word com estilos de título e a leitura por tecnologias de apoio. O critério de sucesso 1.3.1 das WCAG 2.1 é taxativo: "Information, structure, and relationships conveyed through presentation can be programmatically determined or are available in text" (World Wide Web Consortium [W3C], 2018, critério de sucesso 1.3.1). Há outros problemas de tipografia e de estilo.

- **Negrito em excesso.** Com "Uma pessoa que leia só o negrito deve ficar com o esqueleto do tema." (sinteses-historia/SKILL.md, l. 129), negrito nos rótulos dos tópicos, nas ideias principais de cada parte, nas datas, nos nomes e dentro das citações, o negrito deixa de hierarquizar.
- **Notas de atenção em itálico corrido** (l. 127). Blocos inteiros em itálico leem-se pior e, por causa disso, ficam sem citações diretas. Um bloco de destaque resolve as duas coisas.
- **Aspas retas** (l. 130; leitura-academica/SKILL.md, l. 60). Servem o verificador, mas são um resíduo de máquina de escrever num texto editado. A tradição tipográfica portuguesa usa as aspas angulares, com as curvas no segundo nível. A solução é escrever com aspas retas para verificar e converter na exportação, e pôr o verificador a reconhecer as três formas.
- **Metadiscurso em fórmula.** "Nesta primeira parte, importa esclarecer que [...]", "Nesta segunda parte, importa perceber por que razão...", "Nesta terceira parte, importa mostrar que..." (l. 119), repetido em todas as partes de todas as sebentas, torna-se o enchimento que a linha 112 proíbe.
- **Limite rígido de quatro frases** por parágrafo (l. 121). É bom como alarme, mas mau como regra, porque parte raciocínios que precisam de cinco ou seis frases encadeadas.
- **Pseudonotas de rodapé** no fim de cada parte (l. 128). Num documento sem páginas são notas de fim de secção. Para rever, o estudante precisa também de um glossário consolidado, que a skill proíbe, "Os conceitos-chave não ficam num quadro à parte" (l. 88).

**E6. Didática contrária à evidência sobre aprendizagem.** A skill exclui o instrumento de estudo com melhor evidência, "Também não inclui perguntas de exame, a menos que o estudante as peça expressamente." (sinteses-historia/SKILL.md, l. 189). Roediger e Karpicke (2006) mostraram que "Taking a memory test not only assesses what one knows, but also enhances later retention" (p. 249). Na revisão de Dunlosky et al. (2013), "Practice testing and distributed practice received high utility assessments because they benefit learners of different ages and abilities and have been shown to boost students' performance across many criterion tasks and even in educational contexts" [página por confirmar]. Sobre o sublinhado, a mesma revisão conclui: "On the basis of the available evidence, we rate highlighting and underlining as having low utility" [página por confirmar]. Note-se que esta última avaliação diz respeito ao sublinhado feito pelo estudante e não ao destaque tipográfico feito pelo autor. A objeção pertinente à sebenta é outra: ela foi desenhada para ser relida através do negrito, e não para ser recuperada de memória. A preocupação de integridade que motiva a exclusão das perguntas é legítima, mas resolve-se com perguntas de autoavaliação por objetivo, que remetem para as partes da sebenta sem darem respostas-modelo. Faltam também um plano de revisão espaçada, uma versão em cartões de memória do "Essencial a reter" e um guião de comentário de documento, que é uma forma de avaliação frequente em História. A "revisão de última hora" (l. 185) é a única modalidade temporal prevista, e é o contrário da prática distribuída que a mesma revisão classifica como de alta utilidade.

**E7. O produto final não é verificado.** O passo 6 apresenta o verificador como garantia (sinteses-historia/SKILL.md, l. 146-152). O modo sebenta só procura citações entre aspas retas com quatro ou mais palavras (verificar.py, l. 1056 e 1074). Numa sebenta de teste com cinco frases problemáticas, o resultado foi o seguinte.

| Frase da sebenta de teste | Problema | Resultado do verificador |
| --- | --- | --- |
| «a Reforma católica foi somente uma resposta ao protestantismo e nada mais» | citação inventada, em aspas angulares | não detetada |
| “os mártires de Marrocos foram venerados como exemplo de virtude dominicana” | citação adulterada, em aspas curvas | não detetada |
| Frase que reproduz o molde da fonte com sinónimos | arranjo | não detetada |
| "O autor mostra que a Contrarreforma foi obscurantista e fanática." | juízo de valor sem aspas, verbo factivo e termo ausente da fonte | não detetada |
| "a Reforma católica não foi **apenas** uma reação ao protestantismo" | ênfase acrescentada sem indicação | aceite |
| Saldo final | | "Sebenta apta." |

A verificação de arranjo, de neutralidade e de terminologia existe para o dossiê e falta precisamente no texto que o estudante vai ler e reproduzir.

## 4. A distância para um Gemini Notebook de Ciências Sociais

O NotebookLM passou a chamar-se Gemini Notebook em julho de 2026 e continua a ser uma aplicação autónoma (Woodward, 2026). O quadro seguinte compara as capacidades que definem esse tipo de ferramenta com o que as duas skills fazem.

| Capacidade | Gemini Notebook | Estas skills | O que falta |
| --- | --- | --- | --- |
| Caderno persistente de fontes | sim | não, cada conversa recomeça | registo F1, F2... da unidade curricular, com texto extraído, banco de citações e glossário partilhados entre temas |
| Perguntas ao corpus com citações | sim | só "uma pergunta pontual" no chat (leitura-academica/SKILL.md, l. 44) | modo de pergunta e resposta que só responde com o banco e com `--localizar` |
| Verificação das citações e páginas | liga a resposta à passagem, sem conferir página impressa nem forma APA | sim, e é a maior vantagem destas skills | estender à sebenta (E7) |
| Produtos de estudo | resumos, mapas mentais, cartões, questionários, vídeo e áudio | ficha de tema e esquema | autoavaliação, cartões, cronologia, glossário, quadro historiográfico, comentário de documento guiado |
| Domínios | genérico | História política portuguesa | Religião, Cultura, Antiguidade, história não portuguesa (F3 a F5) |

## 5. Prioridades

As correções seguintes estão ordenadas pelo dano que evitam.

1. **Corrigir o modelo e as contradições** (E2, E3, E4). Reescrever o exemplo do anexo A com títulos estruturados, citações diretas em todas as partes, verbos introdutores não factivos, notas com fonte ou assinaladas como lacuna, ênfase em itálico com "[ênfase acrescentada]" e setas com rótulos da lista. Eliminar "Como bem a definia X". Alinhar a regra da paráfrase da síntese com a da leitura.
2. **Verificar a sebenta como se verifica o dossiê** (E7). Reconhecer « », “ ” e " ", aplicar à sebenta os controlos de arranjo, neutralidade e terminologia, assinalar negrito dentro de citações e títulos falsos.
3. **Recalibrar o verificador** (F3, F10). Usar fronteira de palavra, listas de exceções por disciplina, termos e juízos lidos dos ficheiros de referência, localizadores canónicos, fólios e colunas, e numeração romana.
4. **Abrir a leitura a Religião, Cultura e Antiguidade** (F3 a F5). Terminologia e géneros por domínio, regra para relatos sobrenaturais e protocolo de leitura de imagens.
5. **Crítica de fontes e historicização** (F1, F2). Módulo de datação e tradição documental e camada de contexto historiográfico rotulada.
6. **APA completa** (F8). Capítulo em obra coletiva, obra em vários volumes, artigo de revista, entrada de dicionário, obra traduzida e reeditada, legislação, documento de arquivo e obra de numeração canónica.
7. **Didática** (E6). Perguntas de autoavaliação por objetivo, cartões gerados a partir do banco e dos conceitos, plano de revisão espaçada e glossário consolidado.
8. **Arquitetura de caderno** (E1, F11). Sebenta da unidade curricular montada a partir das fichas de tema e modo de pergunta e resposta sobre o caderno.

## Referências

American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.). https://doi.org/10.1037/0000165-000

Arquivo Nacional Torre do Tombo. (s.d.). [Documento sobre a mudança da Era de César para o Ano de Cristo]. https://antt.dglab.gov.pt/wp-content/uploads/sites/17/2022/08/Mudanca-Era-Ano-Cristo.pdf

Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques: Promising directions from cognitive and educational psychology. *Psychological Science in the Public Interest, 14*(1), 4–58. https://doi.org/10.1177/1529100612453266

Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the middle: How language models use long contexts. *Transactions of the Association for Computational Linguistics, 12*, 157–173. https://doi.org/10.1162/tacl_a_00638

Roediger, H. L., III, & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science, 17*(3), 249–255. https://doi.org/10.1111/j.1467-9280.2006.01693.x

Woodward, J. (2026, 16 de julho). *NotebookLM is now Gemini Notebook*. Google. https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/

World Wide Web Consortium. (2018). *Web Content Accessibility Guidelines (WCAG) 2.1*. https://www.w3.org/TR/WCAG21/

### Notas sobre a confirmação das citações

- As frases de Dunlosky et al. (2013) foram confirmadas em reproduções do texto, mas não consegui abrir o PDF para confirmar a página. Conferir antes de reutilizar.
- A regra da ênfase acrescentada (APA, 2020, secção 8.31) foi confirmada em guias universitários que remetem para a p. 275 do manual. Não abri o manual.
- O documento do Arquivo Nacional Torre do Tombo vem descrito entre parênteses retos porque só confirmei, por pesquisa, a existência do ficheiro e o seu tema, e não o título formal.
- Ao verificar o exemplo da skill, confirmei que a designação da assembleia de 1821 na própria Constituição inclui a palavra "Constituintes". Por isso, a nota [1] do exemplo não comete anacronismo e não a incluí nas críticas. O defeito dessa nota é outro, a ausência de fonte.

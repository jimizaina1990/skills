# Anexo H. Do dossiê ao plano de síntese

Este anexo desenvolve as etapas 2 e 3: como se usa o dossiê de leitura e como se lê, objetivo a objetivo, para planear cada parte.

## 1. Sem dossiê

Só para um capítulo curto ou um artigo se lê diretamente, sem dossiê, registando para cada fonte o problema que trata, as ideias principais, os conceitos e as passagens a citar, com a página, e confirmando cada passagem com o verificador (`--localizar`). Para tudo o resto, aplicar primeiro a skill `leitura-academica`.

## 2. Destino de cada secção do dossiê

| Secção do dossiê | Uso na sebenta |
| --- | --- |
| 0. Objetivos | Leitura dos objetivos, partes e perguntas de autoavaliação. |
| 1. Fichas, contexto historiográfico | Situação de cada obra no seu tempo, quando o estudante precisa de saber que uma obra está datada, é confessional ou foi discutida. |
| 11. Mapa dos objetivos e varredura | Partes, em regra uma por objetivo e pela mesma ordem, e as passagens que cada parte tem de usar. As tensões entre objetivo e fonte dão notas de atenção, e o que as fontes não cobrem vai para as lacunas. |
| 13. Banco de citações | Origem das citações diretas, só com as entradas confirmadas. |
| 4. Conceitos | Notas, quadros de conceitos e glossário, com o sentido no autor, a indicação de termo de época ou conceito do historiador, o âmbito e o deslize a evitar. |
| Confusões prováveis, nas unidades | Notas de atenção. |
| Relações, nas unidades | Setas do esquema-síntese, com os rótulos aí registados. |
| Interrogação do texto, nas unidades | Porquê de cada tese central, separação entre facto, interpretação e juízo, e nuances a conservar. |
| 5. Factos e cronologia | Cronologia, quando o tema a justificar, com a data convertida e o sistema de datação da fonte quando difere do atual. |
| 6. Articulação entre obras | Quadros de contraposição e prosa das partes com mais de um autor, com cada posição atribuída a quem a defende. |
| 8. Visão global | Eixo da sebenta. |
| 7. Limites e 12. Pendências | Lacunas e limite final do essencial a reter. |

## 3. Quatro regras de uso do dossiê

- **Citações do banco ou confirmadas na fonte.** Copiam-se do banco as entradas confirmadas, com a sua referência APA. Uma passagem que não esteja no banco só entra depois de localizada na fonte com o verificador (`--localizar`), e acrescenta-se ao banco.
- **A leitura própria é matéria, não texto.** A análise do dossiê diz o que explicar, mas a sebenta escreve-o de novo no seu registo (anexo D). Não se copiam frases do dossiê.
- **Rótulos não passam.** Os rótulos de estatuto do dossiê (leitura própria, inferência, contexto externo, juízo do leitor) transformam-se em formulações ("daqui pode inferir-se...", "segundo o autor..."), nunca em marcas no texto.
- **Conferir o que ficou com ressalva.** As citações marcadas no banco como "confirmada com ressalva", e as de fontes digitalizadas sem a indicação "conferida na imagem", conferem-se no original antes de entrar.

## 4. Ler o dossiê objetivo a objetivo

Um dossiê de uma obra inteira é longo, e um modelo que o lê de uma vez tende a reter o princípio e o fim e a perder o meio, tal como acontece com a própria obra. Por isso o dossiê lê-se objetivo a objetivo, e cada parte da sebenta planeia-se a partir do que foi lido para ela, e não da impressão geral.

1. **Ler por objetivo.** Para cada objetivo, ler a sua linha no mapa dos objetivos, depois cada unidade aí indicada (leitura, interrogação do texto, confusões, relações), as entradas do banco que essas unidades citam, os conceitos que usam e as respostas divergentes do teste de compreensão. As unidades do meio da obra leem-se com a mesma atenção que as primeiras e as últimas.
2. **Voltar à fonte.** Para cada objetivo, correr a procura por tema com duas ou três consultas feitas com os termos do objetivo e os do autor, e com o dossiê, para ver o que ele já cita.

   ```
   python3 <pasta da leitura-academica>/scripts/verificar.py --procurar "termos do objetivo" --procurar "termos do autor" --fonte F1=obra.txt --banco dossie.md
   ```

   Cada passagem devolvida com "SEM citação no banco nesta página" lê-se na fonte. Se servir o objetivo, confirma-se com `--localizar` e entra no plano. Faz-se o mesmo sempre que surge uma dúvida sobre a matéria, ou quando a leitura do dossiê não chega para explicar. Se o dossiê já tiver a varredura por objetivo, parte-se dela e repete-se a procura só onde a parte o pedir.
3. **Escrever o plano de síntese.** Num ficheiro de trabalho (`plano-sintese.md`), uma entrada por objetivo com a leitura do objetivo (etapa 1), o problema a que a parte responde, as teses com as citações que as enunciam (Cnn ou página), as provas, as posições em confronto, os conceitos, as confusões a prevenir, o que fica de fora e a forma prevista (prosa, quadro de contraposição, quadro de conceitos, citação em bloco). Para cada tese, uma nota de compreensão escrita de raiz, sem copiar a passagem: a ideia, a sua função no argumento, porque é que o autor a defende, o seu limite e a sua ligação com o resto (anexo F, secção 4). Se a nota não sai sem repetir a frase do autor, a passagem ainda não foi compreendida e relê-se o contexto na fonte. O plano não passa para a sebenta, mas é o que impede que uma parte do meio seja escrita de memória e que o texto próprio seja paráfrase.
4. **Fixar o eixo e a ordem.** O eixo é a pergunta a que a sebenta responde. As partes seguem, em regra, a ordem dos objetivos, com o contexto antes dos acontecimentos e os conceitos antes dos argumentos que os usam. Conserva-se a ordem cronológica ou causal das fontes quando ela faz parte do sentido.

Numa obra longa, escreve-se cada parte logo a seguir ao seu plano, em vez de planear tudo e escrever tudo depois.

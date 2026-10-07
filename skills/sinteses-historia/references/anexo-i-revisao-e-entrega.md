# Anexo I. Revisão e entrega

Este anexo desenvolve a etapa 5: o verificador, a revisão contra as fontes, a revisão de integridade, a entrega, o documento final e a sebenta da unidade curricular.

## 1. Verificador

Correr o verificador da `leitura-academica` em modo sebenta sobre o ficheiro Markdown, com o dossiê e as fontes, e corrigir todas as falhas. O verificador está na pasta da skill `leitura-academica`, no ficheiro `scripts/verificar.py`.

```
python3 <pasta da leitura-academica>/scripts/verificar.py --sebenta sebenta.md --banco dossie.md --fonte F1=obra.txt
```

Sem dossiê, omite-se `--banco`. As fontes indicam-se sempre que existirem, porque sem `--fonte` o arranjo, as omissões, os nomes e os termos não são verificados.

O verificador confere as citações (curtas e em bloco) contra o banco e as fontes, com a página, a forma APA 7 (reticências, [*sic*], ênfase, blocos, os dois anos das obras traduzidas), as omissões que retiram atribuição, modalizador, negação ou restrição, as teses a negrito que dizem por outras palavras a citação seguinte, as frases que corrigem um objetivo ou deixam afirmações por confirmar fora das lacunas, os nomes próprios ausentes das fontes, o arranjo, o vocabulário avaliativo e os verbos factivos na voz da sebenta, os termos historicamente situados, a estrutura, as notas e o esquema. Os avisos resolvem-se um a um, e os que ficam explicam-se na entrega.

## 2. Revisão contra as fontes

O verificador não vê o sentido. Por isso a sebenta é revista parte a parte contra o dossiê e as fontes. Se houver ferramenta para lançar um revisor separado (um subagente, outra conversa), é ele que faz a revisão, sem ver o raciocínio que produziu a sebenta, com a sebenta, o dossiê, as fontes, os objetivos e a lista seguinte. Sem essa ferramenta, faz-se uma passagem de revisão própria, depois de terminada a sebenta, parte a parte e com a fonte aberta.

- **Objetivos.** Cada parte responde ao objetivo tal como foi lido na etapa 1, com a profundidade que ele pede, e nenhum objetivo foi dado como errado.
- **Teses.** Cada tese de autor está nas palavras do autor, nenhuma frase a antecipa por paráfrase, e cada citação é bastante longa para conservar o sentido, os modalizadores, as concessões e a indicação de quem fala.
- **Texto próprio.** Em cada parágrafo de explicação, os quatro testes do anexo F: a formulação é independente da fonte ou é um decalque com sinónimos e a mesma sequência (patchwriting, que uma referência não desculpa)? A origem de cada ideia está clara, e as inferências da sebenta estão separadas do autor? O sentido, o aspeto ("começou a" não é "é"), a certeza e o âmbito ficaram fiéis? O parágrafo acrescenta compreensão, ou só repete por outras palavras a citação que tem ao lado? Um problema só se dá por demonstrado com a passagem da fonte ao lado.
- **Omissões.** Em cada citação com reticências, o trecho omitido foi lido na fonte e não muda o sentido.
- **Voz.** Nenhuma interpretação ou juízo de autor aparece como facto, e nenhum relato bíblico, hagiográfico ou de tradição aparece na voz da sebenta.
- **Completude.** Para cada objetivo, as passagens do plano de síntese e da procura por tema estão tratadas, incluindo as das unidades do meio. Uma passagem relevante deixada de fora é tão grave como uma citação errada.
- **Fontes exteriores.** Nenhum nome, data ou facto exterior às fontes fora da caixa "Fora das fontes", e nada afirmado e ao mesmo tempo dado como por confirmar.
- **Termos.** Cada termo historicamente situado é usado no sentido da sua época e do autor, tem nota na primeira ocorrência e nunca foi substituído por um termo moderno sem o dizer.
- **Esquema.** As setas dizem o que o texto sustenta, com os rótulos do anexo A (uma sucessão não é uma causa, e uma prova não é uma consequência).
- **APA 7.** As regras do anexo G em todas as citações e referências.
- **Pedagogia.** Um estudante que não leu as fontes percebe o tema com esta sebenta, responde às perguntas de autoavaliação a partir dela e encontra em quadro o que se compara ou se define. O essencial a reter condensa a sebenta sem acrescentar nada de novo.

## 3. Revisão de integridade

A revisão de integridade é obrigatória e cobre a sebenta inteira. Se a skill `rever-integridade-academica` estiver instalada, o revisor aplica-a uma vez, com as fontes e a saída do verificador, segundo a secção dessa skill "Uso com as skills leitura-academica e sinteses-historia", que fixa as precedências (as teses vão em citação direta, o conhecimento comum não dispensa a caixa "Fora das fontes", a norma é a APA 7 desta skill) e acrescenta o teste do acrescento. Sem ela instalada, o revisor aplica os quatro testes do anexo F, parágrafo a parágrafo, com a fonte aberta. Cada achado leva o excerto da sebenta, o excerto da fonte e o estado da evidência (demonstrado, a confirmar, não verificável), e um parágrafo que falha reescreve-se a partir da nota de compreensão, e não trocando palavras.

As correções feitas na revisão voltam a passar pelo verificador.

## 4. Entregar

A sebenta entrega-se como ficheiro Markdown (`sebenta-tema-N.md`), e não como documento Claude, Word ou PDF. No chat, em poucas linhas:

- a linha final do verificador, tal como saiu;
- o resultado da revisão de integridade (achados encontrados, corrigidos e por confirmar), sem nunca declarar a sebenta "livre de plágio" ou "original";
- o que a revisão contra as fontes corrigiu;
- as lacunas importantes;
- os avisos que ficaram e porquê;
- qualquer parte em que tenha havido corte ou que tenha ficado mais curta do que o objetivo pede.

## 5. Documento final

O documento final só se faz depois de o estudante validar a sebenta, e num passo à parte, que pode ser feito noutra conversa e com outro modelo, porque é só transcrição. Nesse passo, o Markdown validado passa para documento (skill de documentos, ou `docx` para Word) sem reescrever nada: os títulos passam a estilos de título, as chamadas a notas de rodapé, os blocos de citação a parágrafos recuados, as caixas a blocos de destaque e o esquema a diagrama. Depois, exporta-se de novo para Markdown e corre-se o verificador, para confirmar que a transcrição não perdeu nem alterou nada (um esquema que não passou para o ficheiro, um parêntese reto escapado).

## 6. Sebenta da unidade curricular

Quando o estudante já tem várias sebentas de tema da mesma unidade curricular, ou pede a sebenta completa, montar um único documento com a estrutura seguinte, sem reescrever o que já está verificado.

1. Capa com a unidade curricular, o ano letivo e as fontes de base.
2. Índice gerado a partir dos títulos.
3. Introdução à unidade curricular, com os objetivos gerais e o percurso entre os temas.
4. Um capítulo por tema, com a sebenta de tema, renumerando as notas de forma seguida.
5. Cronologia geral, reunindo as cronologias dos temas.
6. Glossário geral, reunindo os glossários e assinalando quando o mesmo termo tem sentidos diferentes em autores diferentes.
7. Perguntas de autoavaliação, reunidas por tema, mais duas ou três perguntas transversais que liguem temas.
8. Referências gerais e lacunas gerais.

Correr o verificador sobre o documento montado antes de o entregar, e entregar em Markdown, como as sebentas de tema.

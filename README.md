# skills

Skills de estudo para Ciências Sociais (História, Cultura e Religião), para estudantes do ensino superior português.

- `skills/leitura-academica`. Leitura integral, fiel e verificável das fontes, que produz o dossiê de leitura.
- `skills/sinteses-historia`. Sebenta de estudo a partir do dossiê, com revisão e autoavaliação.
- `skills/CHANGELOG.md`. Alterações face às versões originais.
- `analise/`. Análise crítica das versões originais e casos de teste do verificador.

Para correr os testes do verificador, a partir de `skills/leitura-academica`:

```
python3 -m unittest discover -s scripts/testes -v
```

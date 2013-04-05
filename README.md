A ideia original era coletar apenas os dados da minha cidade, mas ao longo do projeto fui vendo que com um pequeno esfor�o era poss�vel tornar o script mais flex�vel e assim us�-lo para coletar dados de qualquer cidade do pa�s.

## Como usar
```
$ git clone https://github.com/Bonifacio2/transparencia.git
$ python main.py
$ python main.py <UF> # lista os codigos da cidade do UF especificado
$ python main.py <UF> <codigo da cidade> # baixa os dados da cidade especificada
```

## TODO:

- Dar um nome mais adequado a TParser
- Delegar algumas das responsabilidades de TParser
- tratar casos onde o codigo da cidade nao eh valido

- trocar virgulas por pontos na coluna de valor
- separar codigo da descricao da coluna acao governamental
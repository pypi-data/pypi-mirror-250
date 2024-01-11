# Módulo de Manipulação de Arquivos e Diretórios em Python

Este módulo em Python foi desenvolvido para facilitar a manipulação de arquivos e diretórios no sistema operacional.

## Uso

Para utilizar este módulo, importe-o em seu código Python:

```python
from pytezerio.directory import Directory
from pytezerio.file import File

# Exemplo de uso: Listar as extensões de todos os arquivos de uma dado diretório
dir = Directory('/caminho/diretorio')

for filename in dir.list(Directory.FILES):
    file = File(filename)
    print(file.extension())

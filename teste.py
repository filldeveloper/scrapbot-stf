from typing import TextIO


caminho_arquivo = f'C:/sei-dj/stfsite/STFSITE-2022.02.25-NumProcessos.txt'
txt = open(caminho_arquivo, 'r+')
texto = txt.read()

print(texto)


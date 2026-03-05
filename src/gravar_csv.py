import csv
from pathlib import Path
"""obtem o caminho do projeto"""
BASE_DIR = Path(__file__).resolve().parent.parent
""""""
def gravar_arquivo(arquivo,cabecalho, linhas):
    caminho = BASE_DIR / "data" / arquivo #trata o caminho com o nome do arquivo
    print(caminho)
    with open(caminho,"w",encoding="utf-8-sig",newline="") as f:
        writer = csv.DictWriter(f,fieldnames=cabecalho, delimiter=";")
        writer.writeheader()
        writer.writerows(linhas)


        #return list(leitor)
    
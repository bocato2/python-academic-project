import csv
from pathlib import Path
"""obtem o caminho do projeto"""
BASE_DIR = Path(__file__).resolve().parent.parent
""""""
def ler_arquivo(arquivo):
    caminho = BASE_DIR / "data" / arquivo #trata o caminho com o nome do arquivo
    print(caminho)
    with open(caminho,"r",encoding="utf-8-sig",newline="") as f:
        leitor = csv.DictReader(f,delimiter=";")
        return list(leitor)
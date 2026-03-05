from ler_csv import ler_arquivo
from gravar_csv import gravar_arquivo

ds_alunos = ler_arquivo("alunos.csv")
ds_cursos = ler_arquivo("cursos.csv")
ds_notas = ler_arquivo("notas.csv")
ds_disciplinas = ler_arquivo("disciplinas.csv")
ds_financeiro = ler_arquivo("financeiro.csv")

#cria um Dictionary Comprehension, o id do curso passa a ser a chave e o nome o valor
indice_cursos = {c["id_curso"]: c for c in ds_cursos}

indice_alunos = {}
for aluno in ds_alunos:
    ra = aluno.get("ra")
    indice_alunos[ra] = indice_alunos.get(ra,{})
    indice_alunos[ra]= aluno


indice_notas ={}
for nota in ds_notas:
    ra = nota.get("ra")
    nome_disc=nota.get("nome_disciplina")
    media = nota.get("media")
    situacao = nota.get("situacao")
    indice_notas[ra]=indice_notas.get(ra,{})
    ###se o importante é mostrar apenas uma vez a disciplina com a nota atualizada, descomente aqui:
    #indice_notas[ra][nome_disc]=indice_notas[ra].get(nome_disc,{"media":media, "situacao":situacao})
    
    ###para mostrar todas as vezes que a disciplina aparece para o aluno, use o codigo abaixo:
    indice_notas[ra][nome_disc]={"media":media, "situacao":situacao}

indice_financeiro={}
for receber in ds_financeiro:
    ra = receber.get("ra")
    ano = receber.get("ano")
    mes = receber.get("mes")
    ano_mes =f"{ano}_{mes}"#crio essa chave unica para a referencia e usar dicionario
    situacao = receber.get("status_pagamento").strip()
    valor_msl = float(receber.get("valor_mensalidade") or 0)
    valor_pago = float((receber.get("valor_pago") or 0))
    
    indice_financeiro[ra]=indice_financeiro.get(ra,{})
    indice_financeiro[ra][ano_mes]=indice_financeiro[ra].get(ano_mes,{})#agrupo por ano_mes, para agrupar por situacao, deve usar lista[]
    indice_financeiro[ra][ano_mes]={"ano_ref":ano, "mes_ref":mes, "valor":valor_msl,"valor_pago":valor_pago, "situacao":situacao}


dados_aluno={
    "ra":None,
    "curso":None,
    "situacao":None,
    "boletim":{},
    "financeiro":{}
    }
for aluno in ds_alunos:
    nome = (aluno.get("nome") or "").strip()
    curso = indice_cursos.get(aluno["id_curso"])#aqui pega o id do curso do aluno e procura a chave em cursos_por_id que possui o id
    ra = aluno.get("ra")

    cd_curso = aluno.get("id_curso")
    situacao = aluno.get("status")
    notas = indice_notas.get(ra) #filtra as notas pelo ra do aluno
    extrato = indice_financeiro.get(ra)

    dados_aluno[nome]=dados_aluno.get(nome,{})
    dados_aluno[nome]={
        "ra":ra,
        "curso":curso.get("nome_curso"),
        "situacao":situacao,
        }
    
    dados_aluno[nome]["boletim"]=notas
    dados_aluno[nome]["financeiro"]=extrato

diario=[]#cria uma lista para receber os dicts
for linha in ds_notas:
    
    ra = linha.get("ra")
    nm_aluno = indice_alunos[ra].get("nome")
    id_curso = linha.get("id_curso")
    nm_curso = indice_cursos[id_curso].get("nome_curso")
    nova_linha = {**linha, "nome_aluno": nm_aluno, "nome_curso": nm_curso}#concatena a linha com os novos campos

    diario.append(nova_linha)

colunas = diario[0].keys()
gravar_arquivo("diario.csv",colunas,diario)

matriz_curso=[]
for linha in ds_disciplinas:
    id_curso = linha.get("id_curso")
    nm_curso = indice_cursos[id_curso].get("nome_curso")
    nova_linha = {"nome_curso":nm_curso,**linha}
    matriz_curso.append(nova_linha)

colunas = matriz_curso[0].keys()

gravar_arquivo("matrizes.csv",colunas,matriz_curso)
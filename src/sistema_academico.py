from ler_csv import ler_arquivo

ds_alunos = ler_arquivo("alunos.csv")
ds_cursos = ler_arquivo("cursos.csv")
ds_notas = ler_arquivo("notas.csv")
ds_disciplinas = ler_arquivo("disciplinas.csv")
ds_financeiro = ler_arquivo("financeiro.csv")

#cria um Dictionary Comprehension, o id do curso passa a ser a chave e o nome o valor
cursos_por_id = {c["id_curso"]: c for c in ds_cursos}
#notas_por_aluno = {n["ra"]: n for n in ds_notas}
#dividas_por_aluno = {p["ra"]:  p for p in ds_financeiro}
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


        #indice_financeiro[ra][situacao].append(receber)
        #indice_financeiro[ra][situacao].append("ano_ref":ano, "mes_ref":mes, "valor":valor_msl, "valor_pago":valor_pago))
        #indice_financeiro[ra][situacao]={"ano_ref":ano, "mes_ref":mes, "valor":valor_msl}
        
        #indice_financeiro["total_divida"]=indice_financeiro.get[]
    
    

#print(indice_financeiro)


dados_aluno={
    "ra":None,
    "curso":None,
    "situacao":None,
    "boletim":{},
    "financeiro":{}
    }
for aluno in ds_alunos:
    nome = (aluno.get("nome") or "").strip()
    curso = cursos_por_id.get(aluno["id_curso"])#aqui pega o id do curso do aluno e procura a chave em cursos_por_id que possui o id
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
                
    
    
    #if nome not in dados_aluno:
        #dados_aluno[nome]={"curso":curso}
   
    #dados_aluno["curso"]=curso
    #dados_aluno["ra"]=ra
    #dados_aluno["situacao"]=situacao

print(dados_aluno)
import streamlit as st
import datetime
import pandas as pd
from database import create_table, inserir_remedio, listar_remedios

def exibir_cadastro():
    st.subheader("Cadastrar Remédio")

    nome = st.text_input("Nome do remédio")
    quantidade = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
    frequencia = st.text_input("Frequência (ex: a cada 8 horas)")
    telefone = st.text_input("WhatsApp (ex: +5521981664493)")
    data_inicio = st.date_input("Data de início", datetime.date.today())
    data_fim = st.date_input("Data de término", datetime.date.today())

    if st.button("Salvar"):
        if not nome or not quantidade or not frequencia or not telefone:
            st.error("Por favor, preencha todos os campos.")
        else:
            inserir_remedio(
                nome=nome,
                quantidade=quantidade,
                frequencia=frequencia,
                telefone=telefone,
                data_inicio=data_inicio.strftime("%Y-%m-%d"),
                data_fim=data_fim.strftime("%Y-%m-%d")
            )
            st.success(f"Remédio '{nome}' cadastrado com sucesso!")

def exibir_lista():
    st.subheader("Lista de Remédios Cadastrados")
    dados = listar_remedios()
    if not dados:
        st.info("Não há remédios cadastrados.")
        return

    # Converte a lista de tuplas em DataFrame
    colunas = ["ID", "Nome", "Quantidade", "Frequência", "Telefone", "Início", "Término"]
    registros = []
    for row in dados:
        registros.append({
            "ID": row[0],
            "Nome": row[1],
            "Quantidade": row[2],
            "Frequência": row[3],
            "Telefone": row[4],
            "Início": row[5],
            "Término": row[6]
        })
    df = pd.DataFrame(registros, columns=colunas)

    # Exibe tabela simples
    st.dataframe(df, use_container_width=True)

def main():
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios")

    menu = st.sidebar.radio("Selecione a página:", ("Cadastro", "Lista"))

    if menu == "Cadastro":
        exibir_cadastro()
    else:
        exibir_lista()

if __name__ == "__main__":
    create_table()
    main()

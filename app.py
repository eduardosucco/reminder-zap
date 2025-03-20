import streamlit as st
import datetime
import pandas as pd

from supabase import create_table, inserir_remedio, listar_remedios, remover_remedio

def exibir_cadastro():
    st.subheader("Cadastrar Remédio")

    nome = st.text_input("Nome do remédio")
    quantidade = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
    frequencia = st.text_input("Frequência (ex: a cada 8 horas)")
    telefone = st.text_input("WhatsApp (ex: +5521981664493)")
    data_inicio = st.date_input("Data de início", datetime.date.today())
    data_fim = st.date_input("Data de término", datetime.date.today())

    if st.button("Salvar"):
        if not (nome and quantidade and frequencia and telefone):
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

    # Converte para DataFrame
    colunas = ["ID", "Nome", "Quantidade", "Frequência", "Telefone", "Início", "Término"]
    registros = []
    for row in dados:
        # row no formato (id, nome, quantidade, frequencia, telefone, data_inicio, data_fim)
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

    st.dataframe(df, use_container_width=True)

    # Botões de Remover para cada registro
    st.markdown("### Remover um Remédio pelo ID")
    id_para_remover = st.number_input("Digite o ID do remédio para remover", min_value=1, value=1, step=1)
    if st.button("Remover Remédio"):
        remover_remedio(int(id_para_remover))
        st.warning(f"Remédio ID {id_para_remover} removido.")
        st.experimental_rerun()

def main():
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios (Supabase)")

    # Chama a função create_table() (aqui é no-op, mas deixamos por convenção)
    create_table()

    menu = st.sidebar.radio("Selecione a página:", ("Cadastro", "Lista"))

    if menu == "Cadastro":
        exibir_cadastro()
    else:
        exibir_lista()

if __name__ == "__main__":
    main()

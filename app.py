"""
Aplicação web em Streamlit para gerenciar remédios no banco de dados.
"""
import streamlit as st
from database import create_table, inserir_remedio, listar_remedios, remover_remedio
import datetime

def main():
    st.title("Gerenciador de Remédios")
    st.sidebar.title("Menu")

    # Opções de menu
    opcoes = ["Adicionar Remédio", "Listar/Remover Remédios"]
    escolha = st.sidebar.selectbox("Escolha uma opção", opcoes)

    if escolha == "Adicionar Remédio":
        st.subheader("Adicionar novo remédio")

        nome = st.text_input("Nome do remédio")
        quantidade = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
        frequencia = st.text_input("Frequência (ex: a cada 8 horas)")
        data_inicio = st.date_input("Data de início", datetime.date.today())
        data_fim = st.date_input("Data de término", datetime.date.today())

        if st.button("Salvar Remédio"):
            if nome and quantidade and frequencia:
                inserir_remedio(
                    nome,
                    quantidade,
                    frequencia,
                    data_inicio.strftime("%Y-%m-%d"),
                    data_fim.strftime("%Y-%m-%d")
                )
                st.success("Remédio salvo com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

    elif escolha == "Listar/Remover Remédios":
        st.subheader("Lista de Remédios Cadastrados")
        dados = listar_remedios()
        if dados:
            for item in dados:
                remedio_id, nome, quantidade, frequencia, data_inicio, data_fim = item
                st.write(f"**ID**: {remedio_id}")
                st.write(f"**Nome**: {nome}")
                st.write(f"**Quantidade**: {quantidade}")
                st.write(f"**Frequência**: {frequencia}")
                st.write(f"**Início**: {data_inicio}")
                st.write(f"**Término**: {data_fim}")
                if st.button(f"Remover Remédio ID {remedio_id}"):
                    remover_remedio(remedio_id)
                    st.warning(f"Remédio ID {remedio_id} removido.")
                    st.experimental_rerun()
                st.write("---")
        else:
            st.info("Nenhum remédio cadastrado.")

if __name__ == "__main__":
    create_table()
    main()

import streamlit as st
import datetime
import pandas as pd

# Importe as funções do seu módulo supabase_db (renomeado para evitar conflito)
from supabase_db import create_table, inserir_remedio, listar_remedios, remover_remedio

def exibir_cadastro():
    st.subheader("Cadastrar Remédio")

    nome = st.text_input("Nome do remédio")
    quantidade = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
    frequencia = st.text_input("Frequência (ex: a cada 8 horas)")
    telefone = st.text_input("WhatsApp (ex: +5521981664493)")
    data_inicio = st.date_input("Data de início", datetime.date.today())
    data_fim = st.date_input("Data de término", datetime.date.today())

    if st.button("Salvar Novo Remédio"):
        if not (nome and quantidade and frequencia and telefone):
            st.error("Preencha todos os campos obrigatórios.")
            return

        inserir_remedio(
            nome=nome,
            quantidade=quantidade,
            frequencia=frequencia,
            telefone=telefone,
            data_inicio=data_inicio.strftime("%Y-%m-%d"),
            data_fim=data_fim.strftime("%Y-%m-%d")
        )
        st.success(f"Remédio '{nome}' cadastrado com sucesso!")


def exibir_gerenciamento():
    st.subheader("Gerenciamento de Remédios")
    dados = listar_remedios()

    if not dados:
        st.info("Não há remédios cadastrados.")
        return

    # Cabeçalho da "tabela"
    # layout: 1 col (ID) + 2 col (Nome) + 2 col (Qtd) + 2 col (Freq) + 2 col (Tel)
    #         + 2 col (Início) + 2 col (Término) + 2 col (Ações)
    # Você pode ajustar os tamanhos se quiser
    cab = st.columns([1, 2, 2, 2, 2, 2, 2, 3])
    cab[0].markdown("**ID**")
    cab[1].markdown("**Nome**")
    cab[2].markdown("**Qtd**")
    cab[3].markdown("**Frequência**")
    cab[4].markdown("**Telefone**")
    cab[5].markdown("**Início**")
    cab[6].markdown("**Término**")
    cab[7].markdown("**Ações**")

    for row in dados:
        r_id, r_nome, r_qtd, r_freq, r_tel, r_inicio, r_fim = row

        cols = st.columns([1, 2, 2, 2, 2, 2, 2, 3])
        cols[0].write(r_id)
        cols[1].write(r_nome)
        cols[2].write(r_qtd)
        cols[3].write(r_freq)
        cols[4].write(r_tel)
        cols[5].write(r_inicio)
        cols[6].write(r_fim)

        # Na última coluna, criamos 2 sub-colunas para botões Editar e Remover
        with cols[7]:
            col_a, col_b = st.columns([1,1])
            with col_a:
                editar_btn = st.button("Editar", key=f"edit_{r_id}")
            with col_b:
                remover_btn = st.button("Remover", key=f"del_{r_id}")

            # Lógica dos botões
            if editar_btn:
                st.info(f"[Mock] Editar remédio ID {r_id}. Implemente a lógica aqui.")
            
            if remover_btn:
                remover_remedio(r_id)
                st.warning(f"Remédio ID {r_id} removido!")
                st.experimental_rerun()


def main():
    # Define layout "centered" para não ocupar toda a largura
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios (Supabase)")

    create_table()  # Se já existe, não faz nada

    # Tabs para separar Cadastro e Gerenciamento
    tab_cadastro, tab_gerencia = st.tabs(["Cadastro", "Gerenciamento"])

    with tab_cadastro:
        exibir_cadastro()

    with tab_gerencia:
        exibir_gerenciamento()


if __name__ == "__main__":
    main()

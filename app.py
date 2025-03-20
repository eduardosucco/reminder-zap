import streamlit as st
import datetime
import pandas as pd

# Importe as funções do seu arquivo local (renomeado para 'supabase_db.py')
from supabase_db import create_table, inserir_remedio, listar_remedios, remover_remedio


def exibir_cadastro():
    st.subheader("Cadastrar Remédio")

    # Campos do formulário
    nome = st.text_input("Nome do remédio")
    quantidade = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
    frequencia = st.text_input("Frequência (ex: a cada 8 horas)")
    telefone = st.text_input("Telefone (WhatsApp) - Ex: +5521981664493")
    data_inicio = st.date_input("Data de início", datetime.date.today())
    data_fim = st.date_input("Data de término", datetime.date.today())

    # Botão para salvar
    if st.button("Salvar Novo Remédio"):
        # Validação simples
        if not (nome and quantidade and frequencia and telefone):
            st.error("Por favor, preencha todos os campos obrigatórios.")
            return

        # Inserindo via Supabase
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

    # Layout em colunas simulando um cabeçalho de tabela
    # Ajuste as proporções (list) para deixar mais ou menos espaço
    cab1, cab2, cab3, cab4, cab5, cab6, cab7, cab8 = st.columns([1, 2, 2, 2, 2, 2, 2, 2])
    cab1.markdown("**ID**")
    cab2.markdown("**Nome**")
    cab3.markdown("**Qtd**")
    cab4.markdown("**Frequência**")
    cab5.markdown("**Telefone**")
    cab6.markdown("**Início**")
    cab7.markdown("**Término**")
    cab8.markdown("**Ações**")

    # Para cada remédio, criamos uma "linha" com colunas
    for row in dados:
        r_id, r_nome, r_qtd, r_freq, r_tel, r_inicio, r_fim = row  # 7 colunas do Supabase

        c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([1, 2, 2, 2, 2, 2, 2, 2])

        c1.write(r_id)
        c2.write(r_nome)
        c3.write(r_qtd)
        c4.write(r_freq)
        c5.write(r_tel)
        c6.write(r_inicio)
        c7.write(r_fim)

        # Na última coluna, colocamos botões "Editar" e "Remover"
        with c8:
            editar_btn = st.button("Editar", key=f"editar_{r_id}")
            remover_btn = st.button("Remover", key=f"remover_{r_id}")

            # Lógica dos botões
            if editar_btn:
                # Exemplo simples: mensagem.
                # Você pode criar um modal/formulário para editar efetivamente o remédio.
                st.info(f"Editar remédio '{r_nome}' (ID={r_id}). Implementar lógica de edição.")
            
            if remover_btn:
                remover_remedio(r_id)
                st.warning(f"Remédio ID {r_id} removido!")
                st.experimental_rerun()  # Atualiza a página para sumir com a linha removida.


def main():
    # Configura título e layout
    st.set_page_config(page_title="Gerenciador de Remédios", layout="wide")
    st.title("Gerenciador de Remédios (Supabase)")

    # Garante que a função exista, mesmo que não crie a tabela (já criada no painel do Supabase)
    create_table()

    # Usamos aba (tabs) para melhorar visual do "menu"
    tab_cadastro, tab_gerencia = st.tabs(["Cadastro", "Gerenciamento"])

    with tab_cadastro:
        exibir_cadastro()

    with tab_gerencia:
        exibir_gerenciamento()


if __name__ == "__main__":
    main()

import streamlit as st
import datetime
import pandas as pd

from supabase_db import (
    create_table,
    inserir_remedio,
    listar_remedios,
    remover_remedio,
    atualizar_remedio
)

# ================== Conversões de datas ==================
def data_br(iso: str) -> str:
    """YYYY-MM-DD -> DD/MM/AAAA"""
    try:
        dt = datetime.datetime.strptime(iso, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except:
        return iso

def data_iso(br: str) -> str:
    """DD/MM/AAAA -> YYYY-MM-DD"""
    try:
        dt = datetime.datetime.strptime(br, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except:
        return br

# ================== Telas ==================
def tela_gerenciamento():
    """Exibe a tabela de remédios (sem telefone) e botões de Editar/Remover."""
    st.subheader("Gerenciamento de Remédios")

    dados = listar_remedios()
    if not dados:
        st.info("Nenhum remédio cadastrado.")
        return

    # Cabeçalho manual sem telefone
    # Colunas: ID, Nome, Qtd, Freq, Período, [Editar], [Remover]
    col_header = st.columns([1, 2, 2, 2, 2, 1, 1])
    col_header[0].write("**ID**")
    col_header[1].write("**Nome**")
    col_header[2].write("**Qtd**")
    col_header[3].write("**Freq**")
    col_header[4].write("**Período**")
    col_header[5].write("**✏**")
    col_header[6].write("**❌**")

    for row in dados:
        # row => (id, nome, qtd, freq, tel, inicio, fim)
        r_id, r_nome, r_qtd, r_freq, r_tel, r_ini, r_fim = row

        cols = st.columns([1, 2, 2, 2, 2, 1, 1])
        cols[0].write(r_id)
        cols[1].write(r_nome)
        cols[2].write(r_qtd)
        cols[3].write(r_freq)
        cols[4].write(f"{data_br(r_ini)} → {data_br(r_fim)}")

        editar = cols[5].button("✏", key=f"edit_{r_id}")
        remover = cols[6].button("❌", key=f"del_{r_id}")

        if editar:
            # Salva dados no session_state para editar na outra aba
            st.session_state["edit_id"] = r_id
            st.session_state["edit_nome"] = r_nome
            st.session_state["edit_qtd"] = r_qtd
            st.session_state["edit_freq"] = r_freq
            st.session_state["edit_tel"] = r_tel
            st.session_state["edit_ini"] = data_br(r_ini)
            st.session_state["edit_fim"] = data_br(r_fim)
            st.info("Vá para a aba 'Cadastro/Edição' para editar este remédio.")

        if remover:
            remover_remedio(r_id)
            st.warning(f"Remédio ID {r_id} removido.")

def tela_cadastro_edicao():
    """
    Se existir st.session_state["edit_id"], abrimos formulário de edição;
    caso contrário, exibimos formulário de cadastro de novo remédio.
    """
    # Está em modo edição?
    editing_id = st.session_state.get("edit_id", None)
    if editing_id is not None:
        # Editando
        st.subheader("Edição de Remédio")
        nome = st.text_input("Nome", st.session_state["edit_nome"])
        qtd = st.text_input("Quantidade", st.session_state["edit_qtd"])
        freq = st.text_input("Frequência", st.session_state["edit_freq"])
        tel = st.text_input("Telefone (WhatsApp)", st.session_state["edit_tel"])
        inicio_br = st.text_input("Data Início (DD/MM/AAAA)", st.session_state["edit_ini"])
        fim_br = st.text_input("Data Fim (DD/MM/AAAA)", st.session_state["edit_fim"])

        if st.button("Salvar Alterações"):
            atualizar_remedio(
                remedio_id=editing_id,
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone=tel,
                data_inicio=data_iso(inicio_br),
                data_fim=data_iso(fim_br)
            )
            st.success("Remédio atualizado com sucesso!")
            # Limpa o ID de edição
            st.session_state["edit_id"] = None

        if st.button("Cancelar"):
            st.session_state["edit_id"] = None
            st.info("Edição cancelada.")
    else:
        # Cadastro de novo remédio
        st.subheader("Cadastro de Novo Remédio")
        nome = st.text_input("Nome")
        qtd = st.text_input("Quantidade (ex: 5ml)")
        freq = st.text_input("Frequência (ex: a cada 8h)")
        tel = st.text_input("Telefone (WhatsApp)")
        data_i = st.date_input("Data Início", datetime.date.today())
        data_f = st.date_input("Data Fim", datetime.date.today())

        if st.button("Salvar"):
            if not (nome and qtd and freq and tel):
                st.warning("Preencha todos os campos obrigatórios.")
                return
            inserir_remedio(
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone=tel,
                data_inicio=data_i.strftime("%Y-%m-%d"),
                data_fim=data_f.strftime("%Y-%m-%d")
            )
            st.success("Remédio cadastrado com sucesso!")

def main():
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios")

    create_table()

    # Duas abas: 1) Gerenciamento (padrão), 2) Cadastro/Edição
    abas = st.tabs(["Gerenciamento", "Cadastro/Edição"])

    # Primeira aba: Gerenciamento
    with abas[0]:
        tela_gerenciamento()

    # Segunda aba: Cadastro/Edição (para novo ou edição)
    with abas[1]:
        tela_cadastro_edicao()

if __name__ == "__main__":
    main()

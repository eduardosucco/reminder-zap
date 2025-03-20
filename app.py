import streamlit as st
import datetime
import pandas as pd

from supabase_db import (
    create_table,
    inserir_remedio,
    listar_remedios,
    remover_remedio,
    atualizar_remedio  # agora usamos a função de update
)

def formatar_data_br(data_iso: str) -> str:
    """
    Converte 'YYYY-MM-DD' para 'DD/MM/AAAA'.
    Se não for válido, retorna original.
    """
    if not data_iso:
        return ""
    try:
        dt = datetime.datetime.strptime(data_iso, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return data_iso

def formatar_data_iso(data_str: str) -> str:
    """
    Converte 'DD/MM/AAAA' (string) para 'YYYY-MM-DD'.
    Se der erro, retorna a data_str original.
    """
    try:
        dt = datetime.datetime.strptime(data_str, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return data_str


def exibir_cadastro():
    st.subheader("Cadastrar Remédio")

    nome = st.text_input("Nome do remédio")
    quantidade = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
    frequencia = st.text_input("Frequência (ex: a cada 8 horas)")
    telefone = st.text_input("WhatsApp (ex: +5521981664493)")
    data_inicio = st.date_input("Data de início (DD/MM/AAAA)", datetime.date.today())
    data_fim = st.date_input("Data de término (DD/MM/AAAA)", datetime.date.today())

    if st.button("Salvar Novo Remédio"):
        if not (nome and quantidade and frequencia and telefone):
            st.error("Preencha todos os campos obrigatórios.")
            return

        # Armazena no banco em formato ISO (YYYY-MM-DD)
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

    # Cabeçalho manual da "tabela"
    cab = st.columns([1, 2, 2, 2, 3, 2, 2, 1, 1])
    cab[0].markdown("**ID**")
    cab[1].markdown("**Nome**")
    cab[2].markdown("**Qtd**")
    cab[3].markdown("**Frequência**")
    cab[4].markdown("**Telefone**")
    cab[5].markdown("**Início**")
    cab[6].markdown("**Término**")
    cab[7].markdown("**Editar**")
    cab[8].markdown("**Remover**")

    for row in dados:
        r_id, r_nome, r_qtd, r_freq, r_tel, r_inicio_iso, r_fim_iso = row
        r_inicio_br = formatar_data_br(r_inicio_iso)
        r_fim_br = formatar_data_br(r_fim_iso)

        cols = st.columns([1, 2, 2, 2, 3, 2, 2, 1, 1])
        cols[0].write(r_id)
        cols[1].write(r_nome)
        cols[2].write(r_qtd)
        cols[3].write(r_freq)
        cols[4].write(r_tel)
        cols[5].write(r_inicio_br)
        cols[6].write(r_fim_br)

        # Botões de ícone (em colunas separadas)
        editar_btn = cols[7].button("✏️", key=f"edit_{r_id}", help="Editar este remédio")
        remover_btn = cols[8].button("❌", key=f"del_{r_id}", help="Remover este remédio")

        if editar_btn:
            # Guardamos no session_state o ID em edição
            st.session_state["edit_id"] = r_id
            st.session_state["edit_nome"] = r_nome
            st.session_state["edit_qtd"] = r_qtd
            st.session_state["edit_freq"] = r_freq
            st.session_state["edit_tel"] = r_tel
            # Convertendo datas para dd/mm/aaaa
            st.session_state["edit_inicio"] = r_inicio_br
            st.session_state["edit_fim"] = r_fim_br

        if remover_btn:
            remover_remedio(r_id)
            st.warning(f"Remédio ID {r_id} removido!")
            st.experimental_rerun()

    # Se o usuário clicou em EDITAR, exibimos o "formulário de edição"
    if "edit_id" in st.session_state and st.session_state["edit_id"] is not None:
        exibir_form_edicao()


def exibir_form_edicao():
    """Exibe um formulário para editar o remédio selecionado."""
    st.markdown("---")
    st.markdown("## Editar Remédio")
    r_id = st.session_state["edit_id"]

    # Lê dados do session_state
    nome = st.text_input("Nome", st.session_state["edit_nome"])
    qtd = st.text_input("Quantidade", st.session_state["edit_qtd"])
    freq = st.text_input("Frequência", st.session_state["edit_freq"])
    tel = st.text_input("Telefone (WhatsApp)", st.session_state["edit_tel"])
    data_inicio_br = st.text_input("Data Início (DD/MM/AAAA)", st.session_state["edit_inicio"])
    data_fim_br = st.text_input("Data Fim (DD/MM/AAAA)", st.session_state["edit_fim"])

    if st.button("Salvar Alterações"):
        # Converte datas PT-BR para ISO
        data_inicio_iso = formatar_data_iso(data_inicio_br)
        data_fim_iso = formatar_data_iso(data_fim_br)

        atualizar_remedio(
            remedio_id=r_id,
            nome=nome,
            quantidade=qtd,
            frequencia=freq,
            telefone=tel,
            data_inicio=data_inicio_iso,
            data_fim=data_fim_iso
        )
        st.success(f"Remédio ID {r_id} atualizado com sucesso!")
        # Limpa estado de edição
        st.session_state["edit_id"] = None
        st.experimental_rerun()

    if st.button("Cancelar"):
        st.session_state["edit_id"] = None
        st.info("Edição cancelada.")
        st.experimental_rerun()


def main():
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios (Supabase)")

    create_table()  # Normalmente não faz nada, pois tabela já existe

    tabs = st.tabs(["Cadastro", "Gerenciamento"])
    with tabs[0]:
        exibir_cadastro()
    with tabs[1]:
        exibir_gerenciamento()


if __name__ == "__main__":
    main()

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

def formatar_data_br(data_iso: str) -> str:
    """
    Converte 'YYYY-MM-DD' para 'DD/MM/AAAA'.
    Se der erro, retorna o valor original.
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
    Converte 'DD/MM/AAAA' para 'YYYY-MM-DD'.
    Se der erro, retorna o valor original.
    """
    try:
        dt = datetime.datetime.strptime(data_str, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return data_str

def exibir_cadastro():
    st.subheader("Cadastrar Remédio")

    nome = st.text_input("Nome")
    qtd = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
    freq = st.text_input("Freq (ex: a cada 8 horas)")
    tel = st.text_input("Tel (WhatsApp, ex: +5521981664493)")
    data_inicio = st.date_input("Início (DD/MM/AAAA)", datetime.date.today())
    data_fim = st.date_input("Fim (DD/MM/AAAA)", datetime.date.today())

    if st.button("Salvar Novo Remédio"):
        if not (nome and qtd and freq and tel):
            st.error("Preencha todos os campos obrigatórios.")
            return

        inserir_remedio(
            nome=nome,
            quantidade=qtd,
            frequencia=freq,
            telefone=tel,
            # Armazenamos no banco em formato ISO
            data_inicio=data_inicio.strftime("%Y-%m-%d"),
            data_fim=data_fim.strftime("%Y-%m-%d")
        )
        st.success(f"Remédio '{nome}' cadastrado com sucesso!")

def exibir_gerenciamento():
    st.subheader("Gerenciamento")

    dados = listar_remedios()
    if not dados:
        st.info("Não há remédios cadastrados.")
        return

    # Definimos colunas com rótulos curtos para evitar quebras de linha
    # Ajuste as proporções se quiser
    cab = st.columns([1, 2, 1, 1, 2, 1, 1, 1, 1])
    cab[0].markdown("**ID**")
    cab[1].markdown("**Nome**")
    cab[2].markdown("**Qtd**")
    cab[3].markdown("**Freq**")
    cab[4].markdown("**Tel**")
    cab[5].markdown("**Início**")
    cab[6].markdown("**Fim**")
    cab[7].markdown("**✏**")
    cab[8].markdown("**❌**")

    # Renderiza cada registro em colunas alinhadas
    for row in dados:
        r_id, r_nome, r_qtd, r_freq, r_tel, r_inicio_iso, r_fim_iso = row
        r_inicio_br = formatar_data_br(r_inicio_iso)
        r_fim_br = formatar_data_br(r_fim_iso)

        linha = st.columns([1, 2, 1, 1, 2, 1, 1, 1, 1])
        linha[0].write(r_id)
        linha[1].write(r_nome)
        linha[2].write(r_qtd)
        linha[3].write(r_freq)
        linha[4].write(r_tel)
        linha[5].write(r_inicio_br)
        linha[6].write(r_fim_br)

        editar_btn = linha[7].button("✏", key=f"edit_{r_id}", help="Editar este remédio")
        remover_btn = linha[8].button("❌", key=f"del_{r_id}", help="Remover este remédio")

        if editar_btn:
            st.session_state["edit_id"] = r_id
            st.session_state["edit_nome"] = r_nome
            st.session_state["edit_qtd"] = r_qtd
            st.session_state["edit_freq"] = r_freq
            st.session_state["edit_tel"] = r_tel
            st.session_state["edit_inicio_br"] = r_inicio_br
            st.session_state["edit_fim_br"] = r_fim_br

        if remover_btn:
            remover_remedio(r_id)
            st.warning(f"Remédio ID {r_id} removido!")

    # Se clicou em Editar, exibe o formulário no final
    if "edit_id" in st.session_state and st.session_state["edit_id"] is not None:
        exibir_form_edicao()

def exibir_form_edicao():
    """
    Formulário que aparece quando o usuário clica em editar (✏).
    Fica no final da página, sem popup (modal).
    """
    st.markdown("---")
    st.markdown("## Editar Remédio")

    r_id = st.session_state["edit_id"]
    nome = st.text_input("Nome", st.session_state["edit_nome"])
    qtd = st.text_input("Quantidade", st.session_state["edit_qtd"])
    freq = st.text_input("Frequência", st.session_state["edit_freq"])
    tel = st.text_input("Telefone (WhatsApp)", st.session_state["edit_tel"])

    data_inicio_br = st.text_input("Data Início (DD/MM/AAAA)", st.session_state["edit_inicio_br"])
    data_fim_br = st.text_input("Data Fim (DD/MM/AAAA)", st.session_state["edit_fim_br"])

    if st.button("Salvar Alterações"):
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
        st.session_state["edit_id"] = None  # limpa estado de edição

    if st.button("Cancelar"):
        st.session_state["edit_id"] = None
        st.info("Edição cancelada.")

def main():
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios (Supabase)")

    create_table()

    tabs = st.tabs(["Cadastro", "Gerenciamento"])
    with tabs[0]:
        exibir_cadastro()
    with tabs[1]:
        exibir_gerenciamento()

if __name__ == "__main__":
    # Inicializa estado de edição, se não existir
    if "edit_id" not in st.session_state:
        st.session_state["edit_id"] = None

    main()

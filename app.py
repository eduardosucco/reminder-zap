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
    """ Converte 'YYYY-MM-DD' para 'DD/MM/AAAA'. """
    if not data_iso:
        return ""
    try:
        dt = datetime.datetime.strptime(data_iso, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return data_iso

def formatar_data_iso(data_str: str) -> str:
    """ Converte 'DD/MM/AAAA' para 'YYYY-MM-DD'. """
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

        inserir_remedio(
            nome=nome,
            quantidade=quantidade,
            frequencia=frequencia,
            telefone=telefone,
            data_inicio=data_inicio.strftime("%Y-%m-%d"),  # Armazenamos em ISO
            data_fim=data_fim.strftime("%Y-%m-%d")
        )
        st.success(f"Remédio '{nome}' cadastrado com sucesso!")

def exibir_gerenciamento():
    st.subheader("Gerenciamento de Remédios")
    dados = listar_remedios()

    if not dados:
        st.info("Não há remédios cadastrados.")
        return

    # Cabeçalhos
    # 1 col p/ ID
    # 2 col p/ Nome
    # 2 col p/ Qtd
    # 2 col p/ Freq
    # 3 col p/ Telefone
    # 2 col p/ Início
    # 2 col p/ Término
    # 1 col p/ Editar
    # 1 col p/ Remover
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

        linha = st.columns([1, 2, 2, 2, 3, 2, 2, 1, 1])
        linha[0].write(r_id)
        linha[1].write(r_nome)
        linha[2].write(r_qtd)
        linha[3].write(r_freq)
        linha[4].write(r_tel)
        linha[5].write(r_inicio_br)
        linha[6].write(r_fim_br)

        editar_btn = linha[7].button("✏️", key=f"edit_{r_id}", help="Editar este remédio")
        remover_btn = linha[8].button("❌", key=f"del_{r_id}", help="Remover este remédio")

        if editar_btn:
            # Salvar dados no session_state p/ exibir formulário de edição
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
            # Ao invés de chamar experimental_rerun diretamente, seta um flag
            st.session_state["need_rerun"] = True

    # Se o usuário clicou em EDITAR, exibir o formulário
    if "edit_id" in st.session_state and st.session_state["edit_id"] is not None:
        exibir_form_edicao()

def exibir_form_edicao():
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

        # Limpa ID de edição
        st.session_state["edit_id"] = None
        st.session_state["need_rerun"] = True  # avisa que precisamos rerodar a tela

    if st.button("Cancelar"):
        st.session_state["edit_id"] = None
        st.session_state["need_rerun"] = True
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

    # Ao final do script, checa se need_rerun foi setado
    if st.session_state.get("need_rerun"):
        # Zera o flag
        st.session_state["need_rerun"] = False
        # Agora sim forçamos o rerun
        st.experimental_rerun()

if __name__ == "__main__":
    # Inicializa se não existir:
    if "need_rerun" not in st.session_state:
        st.session_state["need_rerun"] = False
    main()

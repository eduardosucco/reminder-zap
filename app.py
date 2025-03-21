import streamlit as st
import datetime
import pandas as pd

from supabase_db import (
    create_table,
    listar_remedios,
    inserir_remedio,
    atualizar_remedio,
    marcar_excluido
)

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

def tela_gerenciamento():
    st.subheader("Gerenciamento de Remédios (excluído='N')")

    dados = listar_remedios()  # (id, nome, qtd, freq, tel, ini, fim, excluido)
    if not dados:
        st.info("Não há remédios cadastrados.")
        return

    # Cabeçalho manual: ID, Nome, Qtd, Freq, Período, Editar, Excluir
    cab = st.columns([1, 2, 2, 2, 2, 1, 1])
    cab[0].write("**ID**")
    cab[1].write("**Nome**")
    cab[2].write("**Qtd**")
    cab[3].write("**Freq**")
    cab[4].write("**Período**")
    cab[5].write("**✏**")
    cab[6].write("**❌**")

    for row in dados:
        # row => (id, nome, qtd, freq, telefone, data_inicio, data_fim, excluido)
        r_id, r_nome, r_qtd, r_freq, _tel, r_ini, r_fim, _exc = row

        linha = st.columns([1, 2, 2, 2, 2, 1, 1])
        linha[0].write(r_id)
        linha[1].write(r_nome)
        linha[2].write(r_qtd)
        linha[3].write(r_freq)
        linha[4].write(f"{data_br(r_ini)} → {data_br(r_fim)}")

        editar_btn = linha[5].button("✏", key=f"edit_{r_id}")
        excluir_btn = linha[6].button("❌", key=f"del_{r_id}")

        if editar_btn:
            st.session_state["edit_id"] = r_id
            st.session_state["edit_nome"] = r_nome
            st.session_state["edit_qtd"] = r_qtd
            st.session_state["edit_freq"] = r_freq
            # Se quiser editar telefone, salve em session_state["edit_tel"] = _tel
            st.session_state["edit_ini"] = data_br(r_ini)
            st.session_state["edit_fim"] = data_br(r_fim)

            # Redireciona para a aba "Cadastro/Edição"
            st.session_state["aba_ativa"] = 1

        if excluir_btn:
            marcar_excluido(r_id)  # Muda 'excluido' para 'S'
            st.warning(f"Remédio ID {r_id} marcado como excluído.")

def tela_cadastro_edicao():
    # Verifica se estamos editando algo
    edit_id = st.session_state.get("edit_id", None)
    if edit_id is not None:
        st.subheader("Editar Remédio")

        nome = st.text_input("Nome", st.session_state.get("edit_nome", ""))
        qtd = st.text_input("Quantidade", st.session_state.get("edit_qtd", ""))
        freq = st.text_input("Frequência", st.session_state.get("edit_freq", ""))
        di_br = st.text_input("Data Início (DD/MM/AAAA)", st.session_state.get("edit_ini", ""))
        df_br = st.text_input("Data Fim (DD/MM/AAAA)", st.session_state.get("edit_fim", ""))

        if st.button("Salvar Alterações"):
            atualizar_remedio(
                remedio_id=edit_id,
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone="",  # se quiser manipular 
                data_inicio=data_iso(di_br),
                data_fim=data_iso(df_br)
            )
            st.success(f"Remédio ID {edit_id} atualizado com sucesso!")
            # Limpa session_state para não mostrar os dados mais
            st.session_state["edit_id"] = None
            st.session_state["aba_ativa"] = 0  # Volta para aba Gerenciamento

        if st.button("Cancelar"):
            st.session_state["edit_id"] = None
            st.session_state["aba_ativa"] = 0
            st.info("Edição cancelada.")
    else:
        st.subheader("Cadastrar Novo Remédio")

        nome = st.text_input("Nome")
        qtd = st.text_input("Quantidade (ex: 5ml)")
        freq = st.text_input("Frequência (ex: a cada 8 horas)")
        d_ini = st.date_input("Data Início", datetime.date.today())
        d_fim = st.date_input("Data Fim", datetime.date.today())
        # Telefone se quiser
        # tel = st.text_input("Telefone (WhatsApp)")

        if st.button("Salvar"):
            if not (nome and qtd and freq):
                st.warning("Preencha os campos obrigatórios.")
                return
            inserir_remedio(
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone="",  # Se quiser
                data_inicio=d_ini.strftime("%Y-%m-%d"),
                data_fim=d_fim.strftime("%Y-%m-%d")
            )
            st.success("Remédio cadastrado!")
            # Não é obrigatório voltar para aba 0. Se quiser, faça:
            # st.session_state["aba_ativa"] = 0

def main():
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios - Excluído Lógico")

    create_table()

    if "aba_ativa" not in st.session_state:
        st.session_state["aba_ativa"] = 0  # 0 => Gerenciamento, 1 => Cadastro/Edição

    abas = st.tabs(["Gerenciamento", "Cadastro/Edição"])

    with abas[0]:
        if st.session_state["aba_ativa"] == 0:
            tela_gerenciamento()
    with abas[1]:
        if st.session_state["aba_ativa"] == 1:
            tela_cadastro_edicao()

if __name__ == "__main__":
    main()

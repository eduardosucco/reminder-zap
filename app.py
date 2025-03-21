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
    """Converte 'YYYY-MM-DD' -> 'DD/MM/AAAA'."""
    try:
        dt = datetime.datetime.strptime(iso, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return iso

def data_iso(br: str) -> str:
    """Converte 'DD/MM/AAAA' -> 'YYYY-MM-DD'."""
    try:
        dt = datetime.datetime.strptime(br, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return br

def tela_gerenciamento():
    """Aba de Gerenciamento:
       - Exibe tabela (excluido='N'),
       - Botão 'Cadastrar Novo',
       - Em cada linha: Editar e Excluir (com st.rerun() após clique).
    """
    st.subheader("Gerenciamento de Remédios")

    # Botão para cadastrar novo remédio
    if st.button("Cadastrar Novo"):
        # Limpa qualquer ID em edição
        st.session_state["edit_id"] = None
        st.session_state["aba_ativa"] = 1
        st.experimental_rerun()  # Redireciona imediatamente para a outra aba

    dados = listar_remedios()  # itens excluido='N'
    if not dados:
        st.info("Não há remédios cadastrados.")
        return

    # Cabeçalhos manual: ID, Nome, Qtd, Freq, Período, [Editar], [Excluir]
    c1, c2, c3, c4, c5, c6, c7 = st.columns([1, 2, 2, 2, 2, 1, 1])
    c1.write("**ID**")
    c2.write("**Nome**")
    c3.write("**Qtd**")
    c4.write("**Freq**")
    c5.write("**Período**")
    c6.write("**✏**")
    c7.write("**❌**")

    for (rid, nome, qtd, freq, _tel, di, df, _exc) in dados:
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 2, 2, 2, 1, 1])
        col1.write(rid)
        col2.write(nome)
        col3.write(qtd)
        col4.write(freq)
        col5.write(f"{data_br(di)} → {data_br(df)}")

        editar = col6.button("✏", key=f"edit_{rid}")
        excluir = col7.button("❌", key=f"del_{rid}")

        if editar:
            st.session_state["edit_id"] = rid
            st.session_state["edit_nome"] = nome
            st.session_state["edit_qtd"] = qtd
            st.session_state["edit_freq"] = freq
            st.session_state["edit_ini"] = data_br(di)
            st.session_state["edit_fim"] = data_br(df)

            st.session_state["aba_ativa"] = 1
            st.experimental_rerun()  # Força recarregar, indo para aba de cadastro/edição

        if excluir:
            marcar_excluido(rid)  # excluido='S'
            st.warning(f"Remédio ID {rid} foi excluído.")
            st.experimental_rerun()  # Atualiza a listagem (item some)

def tela_cadastro_edicao():
    """
    Aba de Cadastro/Edição:
      - Se 'edit_id' estiver definido, entramos em modo edição
      - Caso contrário, novo cadastro
      - Após Salvar/Cancelar, chamamos st.experimental_rerun() para atualizar
    """
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
                telefone="",  # se quiser manipular depois
                data_inicio=data_iso(di_br),
                data_fim=data_iso(df_br)
            )
            st.success(f"Remédio ID {edit_id} atualizado!")
            # Limpa e volta p/ Gerenciamento
            st.session_state["edit_id"] = None
            st.session_state["aba_ativa"] = 0
            st.experimental_rerun()

        if st.button("Cancelar"):
            st.session_state["edit_id"] = None
            st.session_state["aba_ativa"] = 0
            st.info("Edição cancelada.")
            st.experimental_rerun()

    else:
        st.subheader("Cadastrar Novo Remédio")
        nome = st.text_input("Nome")
        qtd = st.text_input("Quantidade (ex: 5ml)")
        freq = st.text_input("Frequência (ex: a cada 8 horas)")
        dt_i = st.date_input("Data Início", datetime.date.today())
        dt_f = st.date_input("Data Fim", datetime.date.today())

        if st.button("Salvar"):
            if not (nome and qtd and freq):
                st.warning("Preencha todos os campos.")
                return
            inserir_remedio(
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone="",
                data_inicio=dt_i.strftime("%Y-%m-%d"),
                data_fim=dt_f.strftime("%Y-%m-%d")
            )
            st.success("Remédio cadastrado!")
            # Retorna para Gerenciamento
            st.session_state["aba_ativa"] = 0
            st.experimental_rerun()

def main():
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios")

    create_table()

    # Definimos a aba inicial se não existir
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

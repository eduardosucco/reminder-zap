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
    """Aba inicial: exibe tabela e botões para Cadastrar Novo, Editar e Excluir."""
    st.subheader("Gerenciamento de Remédios")

    # Botão para cadastrar novo
    if st.button("Cadastrar Novo"):
        st.session_state["edit_id"] = None  # garantia de que não estamos editando
        st.session_state["aba_ativa"] = 1   # vai para aba Cadastro/Edição
        st.rerun()

    dados = listar_remedios()  # Retorna apenas excluido='N'
    if not dados:
        st.info("Nenhum remédio cadastrado.")
        return

    # Cabeçalhos: ID, Nome, Qtd, Freq, Período, [✏], [❌]
    cols_header = st.columns([1, 2, 2, 2, 2, 1, 1])
    cols_header[0].write("**ID**")
    cols_header[1].write("**Nome**")
    cols_header[2].write("**Qtd**")
    cols_header[3].write("**Freq**")
    cols_header[4].write("**Período**")
    cols_header[5].write("**✏**")
    cols_header[6].write("**❌**")

    for (rid, nome, qtd, freq, _tel, di, df, _exc) in dados:
        c1, c2, c3, c4, c5, c6, c7 = st.columns([1, 2, 2, 2, 2, 1, 1])
        c1.write(rid)
        c2.write(nome)
        c3.write(qtd)
        c4.write(freq)
        c5.write(f"{data_br(di)} → {data_br(df)}")

        editar = c6.button("✏", key=f"edit_{rid}")
        excluir = c7.button("❌", key=f"del_{rid}")

        if editar:
            # Preenche dados de edição e muda de aba
            st.session_state["edit_id"] = rid
            st.session_state["edit_nome"] = nome
            st.session_state["edit_qtd"] = qtd
            st.session_state["edit_freq"] = freq
            st.session_state["edit_ini"] = data_br(di)
            st.session_state["edit_fim"] = data_br(df)
            st.session_state["aba_ativa"] = 1
            st.rerun()

        if excluir:
            marcar_excluido(rid)
            st.warning(f"Remédio ID {rid} excluído.")
            st.rerun()

def tela_cadastro_edicao():
    """
    Aba 2: se 'edit_id' existir, exibimos edição;
    caso contrário, exibimos cadastro de novo remédio.
    Ao salvar, voltamos para Gerenciamento (aba_ativa=0).
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
                telefone="",  # se desejar manipular
                data_inicio=data_iso(di_br),
                data_fim=data_iso(df_br)
            )
            st.success(f"Remédio ID {edit_id} atualizado com sucesso!")
            # Limpamos o ID e voltamos para Gerenciamento
            st.session_state["edit_id"] = None
            st.session_state["aba_ativa"] = 0
            st.rerun()

        if st.button("Cancelar"):
            st.session_state["edit_id"] = None
            st.session_state["aba_ativa"] = 0
            st.info("Edição cancelada.")
            st.rerun()
    else:
        st.subheader("Cadastrar Novo Remédio")

        nome = st.text_input("Nome")
        qtd = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
        freq = st.text_input("Frequência (ex: a cada 8 horas)")
        dt_i = st.date_input("Data Início", datetime.date.today())
        dt_f = st.date_input("Data Fim", datetime.date.today())

        if st.button("Salvar"):
            if not (nome and qtd and freq):
                st.warning("Preencha todos os campos obrigatórios.")
                return
            inserir_remedio(
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone="",  # se desejar armazenar
                data_inicio=dt_i.strftime("%Y-%m-%d"),
                data_fim=dt_f.strftime("%Y-%m-%d")
            )
            st.success("Remédio cadastrado com sucesso!")
            # Retorna à aba Gerenciamento
            st.session_state["aba_ativa"] = 0
            st.rerun()

def main():
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios")

    create_table()

    # Inicializa a aba se não existir
    if "aba_ativa" not in st.session_state:
        st.session_state["aba_ativa"] = 0  # 0 = Gerenciamento, 1 = Cadastro/Edição

    abas = st.tabs(["Gerenciamento", "Cadastro/Edição"])
    with abas[0]:
        if st.session_state["aba_ativa"] == 0:
            tela_gerenciamento()
    with abas[1]:
        if st.session_state["aba_ativa"] == 1:
            tela_cadastro_edicao()

if __name__ == "__main__":
    main()

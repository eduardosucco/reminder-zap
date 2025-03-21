import streamlit as st
import datetime
import pandas as pd

# Supondo que estas funções existam no supabase_db.py:
#   create_table(), listar_remedios(), inserir_remedio(),
#   atualizar_remedio(), marcar_excluido()
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
    """ Aba de Gerenciamento:
        - Exibe tabela de remédios (excluido='N'), sem mostrar telefone
        - Botão 'Cadastrar Novo'
        - Botões 'Editar' e 'Excluir' em cada linha
    """
    st.subheader("Gerenciamento de Remédios")

    # Botão para mudar para a aba de cadastro (nova)
    if st.button("Cadastrar Novo"):
        st.session_state["edit_id"] = None  # Garantir que não estamos editando
        st.session_state["aba_ativa"] = 1
        return

    # Lista os remédios válidos (excluido='N')
    dados = listar_remedios()  # cada linha: (id, nome, qtd, freq, tel, data_i, data_f, excluido)
    if not dados:
        st.info("Não há remédios cadastrados.")
        return

    # Cabeçalho manual: ID, Nome, Quant, Freq, Período, [Editar], [Excluir]
    col_header = st.columns([1, 2, 2, 2, 2, 1, 1])
    col_header[0].write("**ID**")
    col_header[1].write("**Nome**")
    col_header[2].write("**Qtd**")
    col_header[3].write("**Freq**")
    col_header[4].write("**Período**")
    col_header[5].write("**✏**")
    col_header[6].write("**❌**")

    for (rid, nome, qtd, freq, _tel, ini, fim, _exc) in dados:
        cols = st.columns([1, 2, 2, 2, 2, 1, 1])
        cols[0].write(rid)
        cols[1].write(nome)
        cols[2].write(qtd)
        cols[3].write(freq)
        cols[4].write(f"{data_br(ini)} → {data_br(fim)}")

        editar_btn = cols[5].button("✏", key=f"edit_{rid}")
        excluir_btn = cols[6].button("❌", key=f"del_{rid}")

        if editar_btn:
            # Salva dados no session_state para edição
            st.session_state["edit_id"] = rid
            st.session_state["edit_nome"] = nome
            st.session_state["edit_qtd"] = qtd
            st.session_state["edit_freq"] = freq
            st.session_state["edit_ini"] = data_br(ini)
            st.session_state["edit_fim"] = data_br(fim)
            # Telefone não exibido aqui, mas se quiser editar, salve em session_state
            # st.session_state["edit_tel"] = _tel

            # Muda para a aba de cadastro/edição
            st.session_state["aba_ativa"] = 1

        if excluir_btn:
            marcar_excluido(rid)
            st.warning(f"Remédio ID {rid} foi excluído.")
            # Ao recarregar, sumirá da lista

def tela_cadastro_edicao():
    """
    Aba de Cadastro/Edição:
      - Se 'edit_id' estiver definido, entramos em modo edição
      - Caso contrário, é novo cadastro
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
                telefone="",  # ou se tiver st.session_state["edit_tel"]
                data_inicio=data_iso(di_br),
                data_fim=data_iso(df_br)
            )
            st.success(f"Remédio ID {edit_id} atualizado!")
            # Limpa form e volta ao Gerenciamento
            st.session_state["edit_id"] = None
            st.session_state["aba_ativa"] = 0

        if st.button("Cancelar"):
            st.session_state["edit_id"] = None
            st.info("Edição cancelada.")
            st.session_state["aba_ativa"] = 0

    else:
        st.subheader("Cadastrar Novo Remédio")

        nome = st.text_input("Nome")
        qtd = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
        freq = st.text_input("Frequência (ex: a cada 8 horas)")
        data_i = st.date_input("Data Início", datetime.date.today())
        data_f = st.date_input("Data Fim", datetime.date.today())
        # Se quiser perguntar telefone, adicione
        # tel = st.text_input("Telefone (WhatsApp)")

        if st.button("Salvar"):
            if not (nome and qtd and freq):
                st.warning("Preencha todos os campos.")
                return
            inserir_remedio(
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone="",  # se quiser
                data_inicio=data_i.strftime("%Y-%m-%d"),
                data_fim=data_f.strftime("%Y-%m-%d")
            )
            st.success("Remédio cadastrado!")
            # Se quiser voltar automaticamente para Gerenciamento:
            st.session_state["aba_ativa"] = 0

def main():
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios")

    create_table()

    # Define controle de abas
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

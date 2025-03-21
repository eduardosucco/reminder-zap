import streamlit as st
import datetime
import pandas as pd

# Importe suas funções de banco (Supabase)
from supabase_db import (
    create_table,
    inserir_remedio,
    listar_remedios,
    remover_remedio,
    atualizar_remedio
)

# ===================== FUNÇÕES DE FORMATO DE DATA =====================

def data_para_br(data_iso: str) -> str:
    """Converte YYYY-MM-DD para DD/MM/AAAA."""
    if not data_iso:
        return ""
    try:
        dt = datetime.datetime.strptime(data_iso, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return data_iso

def data_para_iso(data_br: str) -> str:
    """Converte DD/MM/AAAA para YYYY-MM-DD."""
    try:
        dt = datetime.datetime.strptime(data_br, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return data_br

# ===================== TELAS =====================

def tela_cadastro():
    st.subheader("Cadastro de Remédios")

    nome = st.text_input("Nome")
    qtd = st.text_input("Quantidade (ex: 5ml)")
    freq = st.text_input("Frequência (ex: a cada 8h)")
    tel = st.text_input("Telefone (WhatsApp)")
    data_i = st.date_input("Data Início", datetime.date.today())
    data_f = st.date_input("Data Fim", datetime.date.today())

    if st.button("Salvar"):
        if not (nome and qtd and freq and tel):
            st.warning("Preencha todos os campos.")
            return
        inserir_remedio(
            nome=nome,
            quantidade=qtd,
            frequencia=freq,
            telefone=tel,
            data_inicio=data_i.strftime("%Y-%m-%d"),
            data_fim=data_f.strftime("%Y-%m-%d")
        )
        st.success("Remédio cadastrado!")

    if st.button("Ir para Listagem"):
        st.session_state["page"] = "listagem"

def tela_listagem():
    st.subheader("Lista de Remédios")

    registros = listar_remedios()  # (id, nome, qtd, freq, tel, data_i, data_f)
    if not registros:
        st.info("Nenhum remédio encontrado.")
    else:
        # Monta DataFrame sem telefone
        df_data = []
        for (rid, nome, qtd, freq, _tel, di, df) in registros:
            df_data.append({
                "ID": rid,
                "Nome": nome,
                "Quantidade": qtd,
                "Frequência": freq,
                "Início": data_para_br(di),
                "Término": data_para_br(df)
            })
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)

    st.markdown("### Ações")
    id_acao = st.number_input("Informe o ID", min_value=1, value=1, step=1)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Editar"):
            # Verifica se existe esse ID na lista
            existe = any(r[0] == id_acao for r in registros)
            if existe:
                st.session_state["id_edicao"] = id_acao
                st.session_state["page"] = "edicao"
            else:
                st.warning("ID não encontrado.")

    with col2:
        if st.button("Remover"):
            remover_remedio(id_acao)
            st.success(f"Remédio ID {id_acao} removido.")

    with col3:
        if st.button("Cadastrar Novo"):
            st.session_state["page"] = "cadastro"

def tela_edicao():
    st.subheader("Edição de Remédio")

    # Carrega ID
    rid = st.session_state.get("id_edicao", None)
    if not rid:
        st.error("Nenhum ID em edição.")
        if st.button("Voltar à Listagem"):
            st.session_state["page"] = "listagem"
        return

    # Busca no banco
    registros = listar_remedios()
    registro = next((r for r in registros if r[0] == rid), None)
    if not registro:
        st.error("ID não encontrado no banco.")
        if st.button("Voltar à Listagem"):
            st.session_state["page"] = "listagem"
        return

    # registro => (id, nome, qtd, freq, tel, data_i, data_f)
    _, nome, qtd, freq, tel, di_iso, df_iso = registro

    nome_novo = st.text_input("Nome", nome)
    qtd_novo = st.text_input("Quantidade", qtd)
    freq_novo = st.text_input("Frequência", freq)
    tel_novo = st.text_input("Telefone", tel)

    di_br = st.text_input("Data Início (DD/MM/AAAA)", data_para_br(di_iso))
    df_br = st.text_input("Data Fim (DD/MM/AAAA)", data_para_br(df_iso))

    if st.button("Salvar Alterações"):
        atualizar_remedio(
            remedio_id=rid,
            nome=nome_novo,
            quantidade=qtd_novo,
            frequencia=freq_novo,
            telefone=tel_novo,
            data_inicio=data_para_iso(di_br),
            data_fim=data_para_iso(df_br)
        )
        st.success("Remédio atualizado!")
        st.session_state["page"] = "listagem"

    if st.button("Cancelar"):
        st.session_state["page"] = "listagem"

# ===================== MAIN =====================

def main():
    st.set_page_config(page_title="Remédios", layout="centered")
    st.title("Gerenciador de Remédios (Supabase)")

    create_table()  # Se tabela já existe, não faz nada

    # Define a página atual
    if "page" not in st.session_state:
        st.session_state["page"] = "cadastro"  # default

    if st.session_state["page"] == "cadastro":
        tela_cadastro()
    elif st.session_state["page"] == "listagem":
        tela_listagem()
    elif st.session_state["page"] == "edicao":
        tela_edicao()
    else:
        st.error("Página inválida.")

if __name__ == "__main__":
    main()

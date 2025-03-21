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

# =============== Conversões de data ===============
def data_para_br(data_iso: str) -> str:
    """YYYY-MM-DD -> DD/MM/AAAA"""
    try:
        dt = datetime.datetime.strptime(data_iso, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except:
        return data_iso

def data_para_iso(data_br: str) -> str:
    """DD/MM/AAAA -> YYYY-MM-DD"""
    try:
        dt = datetime.datetime.strptime(data_br, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except:
        return data_br

# =============== Telas ===============
def tela_gerenciamento():
    st.subheader("Gerenciamento de Remédios")

    # Botão para ir ao cadastro (segunda aba)
    if st.button("Cadastrar Novo Remédio"):
        # Salva a informação no session_state para mudar de aba
        st.session_state["aba_ativa"] = 1
        return

    dados = listar_remedios()
    if not dados:
        st.info("Nenhum remédio cadastrado.")
        return

    # Cabeçalho manual, sem a coluna de telefone
    cab = st.columns([1, 2, 2, 2, 2, 1, 1])
    cab[0].write("**ID**")
    cab[1].write("**Nome**")
    cab[2].write("**Quantidade**")
    cab[3].write("**Frequência**")
    cab[4].write("**Período**")  # (Início/Fim)
    cab[5].write("**✏**")
    cab[6].write("**❌**")

    for row in dados:
        # (id, nome, quantidade, frequencia, telefone, data_inicio, data_fim)
        r_id, r_nome, r_qtd, r_freq, _tel, d_ini, d_fim = row
        linha = st.columns([1, 2, 2, 2, 2, 1, 1])

        linha[0].write(r_id)
        linha[1].write(r_nome)
        linha[2].write(r_qtd)
        linha[3].write(r_freq)
        linha[4].write(f"{data_para_br(d_ini)} → {data_para_br(d_fim)}")

        # Botões de Editar e Remover
        editar = linha[5].button("✏", key=f"edit_{r_id}")
        remover = linha[6].button("❌", key=f"del_{r_id}")

        if editar:
            # Carrega info para edição
            st.session_state["edit_id"] = r_id
            st.session_state["edit_nome"] = r_nome
            st.session_state["edit_qtd"] = r_qtd
            st.session_state["edit_freq"] = r_freq
            st.session_state["edit_ini"] = data_para_br(d_ini)
            st.session_state["edit_fim"] = data_para_br(d_fim)
            # Se quisesse editar telefone também, salve em session_state
            st.session_state["edit_tel"] = _tel

            # Muda aba para "Cadastro" mas modo de edição
            st.session_state["aba_ativa"] = 1
            st.session_state["modo_edicao"] = True

        if remover:
            remover_remedio(r_id)
            st.warning(f"Remédio ID {r_id} removido.")


def tela_cadastro():
    """Tela para cadastrar ou editar."""
    # Verifica se estamos em modo edição
    modo_edicao = st.session_state.get("modo_edicao", False)
    if modo_edicao:
        st.subheader("Editar Remédio")
        r_id = st.session_state["edit_id"]
        nome = st.text_input("Nome", st.session_state["edit_nome"])
        qtd = st.text_input("Quantidade", st.session_state["edit_qtd"])
        freq = st.text_input("Frequência", st.session_state["edit_freq"])
        tel = st.text_input("Telefone (WhatsApp)", st.session_state.get("edit_tel", ""))
        di_br = st.text_input("Data Início (DD/MM/AAAA)", st.session_state["edit_ini"])
        df_br = st.text_input("Data Fim (DD/MM/AAAA)", st.session_state["edit_fim"])

        if st.button("Salvar Alterações"):
            atualizar_remedio(
                remedio_id=r_id,
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone=tel,
                data_inicio=data_para_iso(di_br),
                data_fim=data_para_iso(df_br)
            )
            st.success("Remédio atualizado com sucesso!")
            # Limpa o modo edição
            st.session_state["modo_edicao"] = False
            st.session_state["edit_id"] = None

        if st.button("Cancelar"):
            st.session_state["modo_edicao"] = False
            st.session_state["edit_id"] = None
            st.info("Edição cancelada.")

    else:
        st.subheader("Cadastrar Novo Remédio")
        nome = st.text_input("Nome")
        qtd = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
        freq = st.text_input("Frequência (ex: a cada 8h)")
        tel = st.text_input("Telefone (WhatsApp)")
        dt_ini = st.date_input("Data Início", datetime.date.today())
        dt_fim = st.date_input("Data Fim", datetime.date.today())

        if st.button("Salvar"):
            if not (nome and qtd and freq and tel):
                st.warning("Preencha todos os campos.")
                return
            inserir_remedio(
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone=tel,
                data_inicio=dt_ini.strftime("%Y-%m-%d"),
                data_fim=dt_fim.strftime("%Y-%m-%d")
            )
            st.success("Remédio cadastrado com sucesso!")

def main():
    st.set_page_config(page_title="Gerenciar Remédios", layout="centered")
    st.title("Gerenciador de Remédios")

    create_table()

    # Define controle de abas
    if "aba_ativa" not in st.session_state:
        st.session_state.aba_ativa = 0  # 0 = Gerenciamento, 1 = Cadastro
    if "modo_edicao" not in st.session_state:
        st.session_state.modo_edicao = False

    abas = st.tabs(["Gerenciamento", "Cadastro"])
    
    with abas[0]:
        # Aba 0: Gerenciamento
        if st.session_state.aba_ativa == 0:
            tela_gerenciamento()
    with abas[1]:
        # Aba 1: Cadastro (ou Edição)
        if st.session_state.aba_ativa == 1:
            tela_cadastro()

if __name__ == "__main__":
    main()

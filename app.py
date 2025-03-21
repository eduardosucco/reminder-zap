import streamlit as st
import datetime
import pandas as pd

from supabase_db import (
    create_table,
    inserir_remedio,
    listar_remedios,
    atualizar_remedio,
    marcar_excluido   # Nova função que marca 'excluido' = 'S'
)

# ================== Conversões de data ==================
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

# ================== TELA DE GERENCIAMENTO ==================
def tela_gerenciamento():
    st.subheader("Gerenciamento de Remédios")

    # Lista todos, inclusive os marcados como excluído
    # A função listar_remedios precisa trazer (id, nome, qtd, freq, tel, data_i, data_f, excluido)
    dados = listar_remedios()
    if not dados:
        st.info("Não há remédios cadastrados.")
        return

    # Cabeçalho manual para ID, Nome, Qtd, Freq, Periodo, Excl., [Editar], [Excluir]
    cab = st.columns([1, 2, 2, 2, 2, 1, 1, 1])
    cab[0].write("**ID**")
    cab[1].write("**Nome**")
    cab[2].write("**Qtd**")
    cab[3].write("**Freq**")
    cab[4].write("**Período**")
    cab[5].write("**Excl.**")
    cab[6].write("**✏**")
    cab[7].write("**❌**")

    for row in dados:
        # row => (id, nome, qtd, freq, tel, inicio, fim, excluido)
        r_id, r_nome, r_qtd, r_freq, _tel, r_ini, r_fim, r_exc = row

        linha = st.columns([1, 2, 2, 2, 2, 1, 1, 1])
        linha[0].write(r_id)
        linha[1].write(r_nome)
        linha[2].write(r_qtd)
        linha[3].write(r_freq)
        linha[4].write(f"{data_br(r_ini)} → {data_br(r_fim)}")

        # Exibe 'S' ou 'N'
        linha[5].write(r_exc)

        editar_btn = linha[6].button("✏", key=f"edit_{r_id}")
        excluir_btn = linha[7].button("❌", key=f"del_{r_id}")

        if editar_btn:
            # Preenche session_state para edição
            st.session_state["edit_id"] = r_id
            st.session_state["edit_nome"] = r_nome
            st.session_state["edit_qtd"] = r_qtd
            st.session_state["edit_freq"] = r_freq
            st.session_state["edit_ini"] = data_br(r_ini)
            st.session_state["edit_fim"] = data_br(r_fim)
            st.session_state["edit_excluido"] = r_exc  # se quiser manipular
            # Telefone não exibido, mas poderia ser salvo se precisar

            # Muda para aba de Cadastro/Edição
            st.session_state["aba_ativa"] = 1

        if excluir_btn:
            # Marca excluido = 'S'
            marcar_excluido(r_id)
            st.warning(f"Remédio ID {r_id} marcado como excluído.")

# ================== TELA DE CADASTRO / EDIÇÃO ==================
def tela_cadastro_edicao():
    # Se "edit_id" existir, estamos em modo edição
    edit_id = st.session_state.get("edit_id", None)
    if edit_id is not None:
        st.subheader("Edição de Remédio")

        nome = st.text_input("Nome", st.session_state.get("edit_nome", ""))
        qtd = st.text_input("Quantidade", st.session_state.get("edit_qtd", ""))
        freq = st.text_input("Frequência", st.session_state.get("edit_freq", ""))
        # Telefone omitido na listagem, mas se quiser editar, poderia exibir
        # tel = st.text_input("Telefone", st.session_state.get("edit_tel", ""))
        di_br = st.text_input("Data Início (DD/MM/AAAA)", st.session_state.get("edit_ini", ""))
        df_br = st.text_input("Data Fim (DD/MM/AAAA)", st.session_state.get("edit_fim", ""))

        if st.button("Salvar Alterações"):
            atualizar_remedio(
                remedio_id=edit_id,
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone="",  # ou st.session_state.get("edit_tel", "")
                data_inicio=data_iso(di_br),
                data_fim=data_iso(df_br)
            )
            st.success(f"Remédio ID {edit_id} atualizado com sucesso!")
            # Limpa session_state para apagar dados da tela
            st.session_state["edit_id"] = None
            st.session_state["edit_nome"] = ""
            st.session_state["edit_qtd"] = ""
            st.session_state["edit_freq"] = ""
            st.session_state["edit_ini"] = ""
            st.session_state["edit_fim"] = ""
            # Retorna para aba de Gerenciamento
            st.session_state["aba_ativa"] = 0

        if st.button("Cancelar"):
            # Cancela edição e apaga form
            st.session_state["edit_id"] = None
            st.info("Edição cancelada.")
            st.session_state["aba_ativa"] = 0
    else:
        st.subheader("Cadastro de Novo Remédio")
        nome = st.text_input("Nome")
        qtd = st.text_input("Quantidade (ex: 5ml)")
        freq = st.text_input("Frequência (ex: a cada 8 horas)")
        dt_i = st.date_input("Data Início", datetime.date.today())
        dt_f = st.date_input("Data Fim", datetime.date.today())
        # Telefone fica oculto no front, mas se quiser, exiba um st.text_input("Telefone")

        if st.button("Salvar"):
            if not (nome and qtd and freq):
                st.warning("Preencha os campos obrigatórios.")
                return
            inserir_remedio(
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone="",  # se quiser manter
                data_inicio=dt_i.strftime("%Y-%m-%d"),
                data_fim=dt_f.strftime("%Y-%m-%d")
            )
            st.success("Remédio cadastrado com sucesso!")
            # Limpar os campos? Basta não ter session_state. 
            # Se quiser trocar de aba depois de cadastrar, pode:
            # st.session_state["aba_ativa"] = 0

# ================== MAIN ==================
def main():
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios (Excluído = S/N)")

    create_table()

    if "aba_ativa" not in st.session_state:
        st.session_state["aba_ativa"] = 0  # 0 = Gerenciamento, 1 = Cadastro/Edição

    abas = st.tabs(["Gerenciamento", "Cadastro/Edição"])

    with abas[0]:
        # Se aba_ativa == 0
        if st.session_state["aba_ativa"] == 0:
            tela_gerenciamento()
    with abas[1]:
        # Se aba_ativa == 1
        if st.session_state["aba_ativa"] == 1:
            tela_cadastro_edicao()

if __name__ == "__main__":
    main()

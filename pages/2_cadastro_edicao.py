import streamlit as st
import datetime
import pandas as pd
from supabase_db import inserir_remedio, atualizar_remedio

def data_br_to_iso(data_str: str) -> str:
    """Converte 'DD/MM/AAAA' -> 'YYYY-MM-DD'."""
    try:
        dt = datetime.datetime.strptime(data_str, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return data_str

st.title("Cadastro / Edição")

st.markdown("""
**Esta página** permite cadastrar um novo remédio **ou** editar um existente.
Para editar, digite manualmente o ID, pois não há um botão de redirecionamento automático 
da página anterior (em um multipage app padrão).
""")

modo = st.radio("Escolha a ação:", ["Cadastrar Novo", "Editar Existente"])

if modo == "Cadastrar Novo":
    st.subheader("Novo Remédio")

    nome = st.text_input("Nome")
    qtd = st.text_input("Quantidade (ex: 5ml)")
    freq = st.text_input("Frequência (ex: a cada 8h)")
    data_i = st.date_input("Data Início", datetime.date.today())
    data_f = st.date_input("Data Fim", datetime.date.today())

    if st.button("Salvar"):
        if not (nome and qtd and freq):
            st.warning("Preencha os campos obrigatórios.")
        else:
            inserir_remedio(
                nome=nome,
                quantidade=qtd,
                frequencia=freq,
                telefone="",  # se quiser
                data_inicio=data_i.strftime("%Y-%m-%d"),
                data_fim=data_f.strftime("%Y-%m-%d")
            )
            st.success("Cadastrado com sucesso!")
            st.experimental_rerun()

else:
    st.subheader("Editar Remédio Existente")

    rid = st.number_input("ID do Remédio", min_value=1, value=1)
    nome_ed = st.text_input("Novo Nome")
    qtd_ed = st.text_input("Nova Quantidade")
    freq_ed = st.text_input("Nova Frequência")
    data_i_br = st.text_input("Data Início (DD/MM/AAAA)")
    data_f_br = st.text_input("Data Fim (DD/MM/AAAA)")

    if st.button("Salvar Alterações"):
        if not (nome_ed and qtd_ed and freq_ed and data_i_br and data_f_br):
            st.warning("Preencha todos os campos.")
        else:
            atualizar_remedio(
                remedio_id=rid,
                nome=nome_ed,
                quantidade=qtd_ed,
                frequencia=freq_ed,
                telefone="",
                data_inicio=data_br_to_iso(data_i_br),
                data_fim=data_br_to_iso(data_f_br)
            )
            st.success(f"Remédio ID {rid} atualizado!")
            st.experimental_rerun()

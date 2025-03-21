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

# Converte data ISO (YYYY-MM-DD) -> PT-BR (DD/MM/AAAA)
def data_br(data_iso):
    try:
        return datetime.datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except:
        return data_iso

# Converte data PT-BR (DD/MM/AAAA) -> ISO (YYYY-MM-DD)
def data_iso(data_str):
    try:
        return datetime.datetime.strptime(data_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        return data_str

def tela_cadastro():
    st.subheader("Cadastrar Remédio")
    nome = st.text_input("Nome")
    qtd = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
    freq = st.text_input("Frequência (ex: a cada 8 horas)")
    # Telefone é cadastrado, mas não exibido na tabela
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
        st.success("Remédio cadastrado com sucesso!")

def tela_listagem():
    st.subheader("Listagem de Remédios")
    registros = listar_remedios()
    if not registros:
        st.info("Nenhum remédio encontrado.")
        return

    # registros: (id, nome, quantidade, frequencia, telefone, data_inicio, data_fim)
    # Ocultamos 'telefone' na tabela
    df_data = []
    for (rid, nome, qtd, freq, _tel, di, df) in registros:
        df_data.append({
            "ID": rid,
            "Nome": nome,
            "Quantidade": qtd,
            "Frequência": freq,
            "Início": data_br(di),
            "Término": data_br(df)
        })
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True)

    # REMOVER - Digita o ID e remove
    st.markdown("### Remover Remédio")
    id_rm = st.number_input("ID para Remover", min_value=0, value=0)
    if st.button("Remover"):
        if id_rm > 0:
            remover_remedio(id_rm)
            st.success(f"Remédio ID {id_rm} removido.")
        else:
            st.warning("Informe um ID válido.")

    # EDITAR - Digita o ID e edita
    st.markdown("### Editar Remédio")
    id_ed = st.number_input("ID para Editar", min_value=0, value=0)
    if st.button("Carregar Dados"):
        if id_ed <= 0:
            st.warning("Informe um ID válido.")
        else:
            # Localiza o registro com aquele ID
            reg = next((r for r in registros if r[0] == id_ed), None)
            if not reg:
                st.error("Não foi encontrado esse ID.")
            else:
                editar_remedio(reg)

def editar_remedio(registro):
    # registro: (id, nome, qtd, freq, tel, data_i, data_f)
    rid, nome, qtd, freq, tel, di, df = registro
    st.write(f"**Editando o ID {rid}**")

    # Campos para edição
    novo_nome = st.text_input("Nome", nome)
    nova_qtd = st.text_input("Quantidade", qtd)
    nova_freq = st.text_input("Frequência", freq)
    # Telefone não é exibido na listagem, mas editamos aqui se quiser
    novo_tel = st.text_input("Telefone (WhatsApp)", tel)
    novo_di_br = st.text_input("Data Início (DD/MM/AAAA)", data_br(di))
    novo_df_br = st.text_input("Data Fim (DD/MM/AAAA)", data_br(df))

    if st.button("Salvar Alterações"):
        atualizar_remedio(
            remedio_id=rid,
            nome=novo_nome,
            quantidade=nova_qtd,
            frequencia=nova_freq,
            telefone=novo_tel,
            data_inicio=data_iso(novo_di_br),
            data_fim=data_iso(novo_df_br)
        )
        st.success("Remédio atualizado com sucesso.")

def main():
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios (Supabase)")

    create_table()  # Caso não exista, mas normalmente já criado

    abas = st.tabs(["Cadastro", "Listagem"])
    with abas[0]:
        tela_cadastro()
    with abas[1]:
        tela_listagem()

if __name__ == "__main__":
    main()

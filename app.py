"""
Aplicação web em Streamlit para gerenciar remédios, agora com:
1) Visual mais atraente (pequena customização de estilo),
2) Tabela interativa com botões para enviar mensagem e remover,
3) Menu lateral com botões em vez de selectbox.
"""

import streamlit as st
import datetime
import pandas as pd

from database import create_table, inserir_remedio, listar_remedios, remover_remedio
from notifications.twilio_service import enviar_whatsapp_body  # Ajuste se precisar

def set_page_style():
    """
    Pequena injeção de CSS para melhorar a aparência.
    Você pode customizar cores, fontes etc.
    """
    st.markdown(
        """
        <style>
        /* Centralizar títulos e ajustar fonte */
        .title, .sidebar .title {
            text-align: center;
            color: #2E4053;
            font-family: "Helvetica", sans-serif;
        }
        /* Mudar cor de fundo do header */
        header, .reportview-container {
            background-color: #F9FAFC;
        }
        /* Botão customizado */
        .stButton>button {
            background-color: #3498DB !important;
            color: #FFFFFF !important;
            border-radius: 4px !important;
            margin: 0px 5px 0px 0px;
        }
        /* Layout geral */
        .block-container {
            padding: 1rem 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def mostrar_menu_lateral():
    """
    Menu lateral com botões para navegação entre páginas:
    - Cadastrar Remédio
    - Lista de Remédios
    """
    st.sidebar.title("Menu")
    
    # Se não existir 'page' no st.session_state, define 'Cadastro' como default
    if "page" not in st.session_state:
        st.session_state.page = "Cadastro"
    
    # Botão de cadastro
    if st.sidebar.button("Cadastrar Remédio"):
        st.session_state.page = "Cadastro"
    
    # Botão de lista
    if st.sidebar.button("Lista de Remédios"):
        st.session_state.page = "Lista"

def exibir_cadastro():
    """
    Formulário para cadastrar um novo remédio.
    """
    st.header("Cadastro de Remédio")

    nome = st.text_input("Nome do remédio")
    quantidade = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
    frequencia = st.text_input("Frequência (ex: a cada 8 horas)")
    telefone = st.text_input("WhatsApp para lembrete (ex: +5521981664493)")
    data_inicio = st.date_input("Data de início", datetime.date.today())
    data_fim = st.date_input("Data de término", datetime.date.today())

    if st.button("Salvar"):
        if not (nome and quantidade and frequencia and telefone):
            st.error("Por favor, preencha todos os campos.")
            return
        
        inserir_remedio(
            nome=nome,
            quantidade=quantidade,
            frequencia=frequencia,
            telefone=telefone,
            data_inicio=data_inicio.strftime("%Y-%m-%d"),
            data_fim=data_fim.strftime("%Y-%m-%d")
        )
        st.success("Remédio cadastrado com sucesso!")

def exibir_lista():
    """
    Exibição em tabela dos remédios cadastrados + botões para
    enviar mensagem (Twilio) e remover cada registro.
    """
    st.header("Lista de Remédios")
    
    dados = listar_remedios()
    if not dados:
        st.info("Nenhum remédio cadastrado ainda.")
        return
    
    # Converter a lista de tuplas em DataFrame para exibir como tabela
    columns = ["ID", "Nome", "Quantidade", "Frequência", "Telefone", "Início", "Término"]
    df_data = []
    for row in dados:
        # row: (id, nome, quantidade, frequencia, telefone, data_inicio, data_fim)
        df_data.append({
            "ID": row[0],
            "Nome": row[1],
            "Quantidade": row[2],
            "Frequência": row[3],
            "Telefone": row[4],
            "Início": row[5],
            "Término": row[6]
        })

    df = pd.DataFrame(df_data, columns=columns)
    
    # Exibir a tabela (DataFrame)
    st.dataframe(df, use_container_width=True)

    # Abaixo da tabela, exibimos cada item com botões "Enviar" e "Remover"
    st.subheader("Ações Individuais")
    for row in dados:
        remedio_id, nome, quantidade, frequencia, telefone, inicio, fim = row
        
        col1, col2, col3 = st.columns([4,1,1])
        with col1:
            st.write(
                f"**ID**: {remedio_id} | **Nome**: {nome} | **Qtd.**: {quantidade} | "
                f"**Freq.**: {frequencia} | **Tel.**: {telefone} | "
                f"**Início**: {inicio} | **Término**: {fim}"
            )
        with col2:
            if st.button("Enviar", key=f"enviar_{remedio_id}"):
                try:
                    msg = (
                        f"Olá! Lembrete do remédio '{nome}' "
                        f"(Dose: {quantidade}, Freq: {frequencia})."
                    )
                    sid = enviar_whatsapp_body(telefone, msg)
                    st.success(f"Mensagem enviada! SID: {sid}")
                except Exception as e:
                    st.error(f"Falha ao enviar: {e}")

        with col3:
            if st.button("Remover", key=f"remover_{remedio_id}"):
                remover_remedio(remedio_id)
                st.warning(f"Remédio ID {remedio_id} removido.")
                st.experimental_rerun()

def main():
    """
    Função principal: define o estilo, mostra menu lateral e
    exibe a página correspondente (cadastro ou lista).
    """
    # Injetar nosso CSS customizado
    set_page_style()

    # Menu lateral com botões
    mostrar_menu_lateral()

    # Título principal (podemos repetir para ficar em evidência)
    st.title("Gerenciador de Remédios")

    # Decidir qual tela exibir com base na variável de sessão 'page'
    if st.session_state.page == "Cadastro":
        exibir_cadastro()
    else:
        exibir_lista()

if __name__ == "__main__":
    create_table()
    main()

import streamlit as st
import datetime
import pandas as pd

from database import create_table, inserir_remedio, listar_remedios, remover_remedio
from notifications.twilio_service import enviar_whatsapp_body  # Ajuste se precisar

def set_custom_style():
    """
    Injeção de CSS para customizar aparência de alguns elementos no Streamlit.
    Você pode alterar cores, fontes, etc.
    """
    st.markdown("""
    <style>
    /* Define um fundo mais claro no container */
    .block-container {
        background-color: #FBFBFB;
        padding: 2rem 2rem 2rem 2rem;
    }
    /* Título principal */
    .title {
        text-align: center;
        color: #2E4053;
        font-family: "Helvetica", sans-serif;
        margin-top: 0px;
    }
    /* Ajustes para cabeçalho da página */
    header, .reportview-container {
        background-color: #FFFFFF;
    }
    /* Estilo para os botões */
    .stButton>button {
        background-color: #3498DB !important;
        color: #FFFFFF !important;
        border-radius: 4px !important;
        margin: 0px 5px 0px 0px;
    }
    </style>
    """, unsafe_allow_html=True)

def exibir_cadastro():
    st.subheader("Cadastro de Remédio")
    nome = st.text_input("Nome do remédio")
    quantidade = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
    frequencia = st.text_input("Frequência (ex: a cada 8 horas)")
    telefone = st.text_input("WhatsApp (ex: +5521981664493)")
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
        st.success(f"Remédio '{nome}' cadastrado com sucesso!")

def exibir_lista():
    st.subheader("Lista de Remédios Cadastrados")
    dados = listar_remedios()
    
    if not dados:
        st.info("Nenhum remédio cadastrado ainda.")
        return
    
    # Convertendo para DataFrame
    colunas = ["ID", "Nome", "Quantidade", "Frequência", "Telefone", "Início", "Término"]
    registros = []
    for row in dados:
        # row: (id, nome, quantidade, frequencia, telefone, data_inicio, data_fim)
        registros.append({
            "ID": row[0],
            "Nome": row[1],
            "Quantidade": row[2],
            "Frequência": row[3],
            "Telefone": row[4],
            "Início": row[5],
            "Término": row[6]
        })
    df = pd.DataFrame(registros, columns=colunas)
    
    # Exibe tabela
    st.dataframe(df, use_container_width=True)

    # Opções de Ações em cada registro
    st.markdown("### Ações Individuais")
    for row in dados:
        remedio_id, nome, quantidade, frequencia, telefone, inicio, fim = row
        
        with st.expander(f"Detalhes do Remédio ID {remedio_id}"):
            st.write(f"**Nome**: {nome}")
            st.write(f"**Quantidade**: {quantidade}")
            st.write(f"**Frequência**: {frequencia}")
            st.write(f"**Telefone**: {telefone}")
            st.write(f"**Início**: {inicio}")
            st.write(f"**Término**: {fim}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Enviar WhatsApp", key=f"enviar_{remedio_id}"):
                    try:
                        msg = (
                            f"Olá! Lembrete do remédio '{nome}' "
                            f"(Dose: {quantidade}, Freq: {frequencia})."
                        )
                        sid = enviar_whatsapp_body(telefone, msg)
                        st.success(f"Mensagem enviada! SID: {sid}")
                    except Exception as e:
                        st.error(f"Erro ao enviar: {e}")

            with col2:
                if st.button("Remover", key=f"remover_{remedio_id}"):
                    remover_remedio(remedio_id)
                    st.warning(f"Remédio ID {remedio_id} removido.")
                    st.experimental_rerun()

def main():
    # Define título da página e layout
    st.set_page_config(
        page_title="Gerenciador de Remédios",
        layout="wide"
    )

    # Aplica CSS customizado
    set_custom_style()

    st.title("Gerenciador de Remédios")

    # Menu lateral usando radio (em vez de button)
    menu = st.sidebar.radio("Navegação", ("Cadastro", "Lista"))
    
    if menu == "Cadastro":
        exibir_cadastro()
    else:
        exibir_lista()

if __name__ == "__main__":
    create_table()
    main()

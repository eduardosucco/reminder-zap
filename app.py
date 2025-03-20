import streamlit as st
import datetime
import pandas as pd

# Importe as funções do seu módulo supabase_db (ou outro nome que não seja 'supabase.py')
from supabase_db import create_table, inserir_remedio, listar_remedios, remover_remedio

def formatar_data_br(data_iso: str) -> str:
    """
    Converte 'YYYY-MM-DD' para 'DD/MM/AAAA'.
    Se não for uma data válida ou vier vazia, retorna o valor original sem formato.
    """
    if not data_iso:
        return ""
    try:
        dt = datetime.datetime.strptime(data_iso, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return data_iso

def exibir_cadastro():
    st.subheader("Cadastrar Remédio")

    # Pedimos a data em PT-BR apenas como indicação visual;
    # O widget date_input depende do locale do navegador, mas armazenamos e exibimos manualmente
    hoje = datetime.date.today()

    nome = st.text_input("Nome do remédio")
    quantidade = st.text_input("Quantidade (ex: 5ml, 1 comprimido)")
    frequencia = st.text_input("Frequência (ex: a cada 8 horas)")
    telefone = st.text_input("WhatsApp (ex: +5521981664493)")
    data_inicio = st.date_input("Data de início (DD/MM/AAAA)", hoje)
    data_fim = st.date_input("Data de término (DD/MM/AAAA)", hoje)

    if st.button("Salvar Novo Remédio"):
        if not (nome and quantidade and frequencia and telefone):
            st.error("Por favor, preencha todos os campos obrigatórios.")
            return

        # Armazena no banco como YYYY-MM-DD (ISO)
        inserir_remedio(
            nome=nome,
            quantidade=quantidade,
            frequencia=frequencia,
            telefone=telefone,
            data_inicio=data_inicio.strftime("%Y-%m-%d"),
            data_fim=data_fim.strftime("%Y-%m-%d")
        )
        st.success(f"Remédio '{nome}' cadastrado com sucesso!")

def exibir_gerenciamento():
    st.subheader("Gerenciamento de Remédios")
    dados = listar_remedios()

    if not dados:
        st.info("Não há remédios cadastrados.")
        return

    # Cabeçalhos da "tabela" manual
    cab = st.columns([1, 2, 2, 2, 3, 2, 2, 2])
    cab[0].markdown("**ID**")
    cab[1].markdown("**Nome**")
    cab[2].markdown("**Qtd**")
    cab[3].markdown("**Frequência**")
    cab[4].markdown("**Telefone**")
    cab[5].markdown("**Início**")
    cab[6].markdown("**Término**")
    cab[7].markdown("**Ações**")

    for row in dados:
        r_id, r_nome, r_qtd, r_freq, r_tel, r_inicio_iso, r_fim_iso = row

        # Converter datas para PT-BR
        r_inicio_br = formatar_data_br(r_inicio_iso)
        r_fim_br = formatar_data_br(r_fim_iso)

        cols = st.columns([1, 2, 2, 2, 3, 2, 2, 2])
        cols[0].write(r_id)
        cols[1].write(r_nome)
        cols[2].write(r_qtd)
        cols[3].write(r_freq)
        cols[4].write(r_tel)
        cols[5].write(r_inicio_br)
        cols[6].write(r_fim_br)

        # Última coluna: botões alinhados (somente ícones)
        with cols[7]:
            # Dividir em duas colunas iguais dentro dessa coluna (para lápis e xis)
            col_edit, col_del = st.columns([1,1])

            with col_edit:
                editar_btn = st.button("✏️", key=f"edit_{r_id}", help="Editar este remédio")
            with col_del:
                remover_btn = st.button("❌", key=f"del_{r_id}", help="Remover este remédio")

            if editar_btn:
                # Exemplo simples de mensagem
                st.info(f"[Mock] Você clicou em editar o remédio ID={r_id}.")
                # Para editar de verdade, criar uma função atualizar_remedio(...) no supabase_db.
            
            if remover_btn:
                remover_remedio(r_id)
                st.warning(f"Remédio ID {r_id} removido!")
                st.experimental_rerun()

def main():
    # Layout "centered" para não ocupar toda a largura
    st.set_page_config(page_title="Gerenciador de Remédios", layout="centered")
    st.title("Gerenciador de Remédios (Supabase)")

    create_table()  # Se já existe, não faz nada

    # Duas abas para separar Cadastro de Gerenciamento
    tab_cadastro, tab_gerencia = st.tabs(["Cadastro", "Gerenciamento"])

    with tab_cadastro:
        exibir_cadastro()

    with tab_gerencia:
        exibir_gerenciamento()

if __name__ == "__main__":
    main()

import streamlit as st

# Definimos as páginas (cada Page aponta para um arquivo .py)
page1 = st.Page("1_gerenciamento.py", title="Página 1", icon=":house:")
page2 = st.Page("2_cadastro_edicao.py", title="Página 2", icon=":gear:")

# Cria o objeto de navegação
nav = st.navigation([page1, page2])

# Configuração global do app (título e favicon no navegador)
st.set_page_config(
    page_title="Meu App Multipage",
    page_icon=":fire:"
)

# Executa a navegação, exibindo as páginas conforme o usuário seleciona
nav.run()

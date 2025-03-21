import streamlit as st
import datetime
import pandas as pd
from supabase_db import listar_remedios, marcar_excluido  # Ajuste nomes se precisar

def data_br(iso: str) -> str:
    """Converte YYYY-MM-DD -> DD/MM/AAAA (simples)."""
    try:
        dt = datetime.datetime.strptime(iso, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return iso

st.title("Gerenciamento de Remédios")

dados = listar_remedios()  # Retorna apenas itens com excluido='N'
if not dados:
    st.info("Nenhum remédio encontrado.")
else:
    # Cabeçalho manual: ID, Nome, Qtd, Freq, Período, Excluir
    cab = st.columns([1, 2, 2, 2, 2, 1])
    cab[0].write("**ID**")
    cab[1].write("**Nome**")
    cab[2].write("**Qtd**")
    cab[3].write("**Freq**")
    cab[4].write("**Período**")
    cab[5].write("**❌**")

    for (rid, nome, qtd, freq, _tel, inicio, fim, _exc) in dados:
        c1, c2, c3, c4, c5, c6 = st.columns([1, 2, 2, 2, 2, 1])
        c1.write(rid)
        c2.write(nome)
        c3.write(qtd)
        c4.write(freq)
        c5.write(f"{data_br(inicio)} → {data_br(fim)}")

        excluir_btn = c6.button("❌", key=f"del_{rid}")
        if excluir_btn:
            marcar_excluido(rid)
            st.warning(f"Remédio ID {rid} excluído (lógico).")
            st.experimental_rerun()

st.markdown("---")
st.markdown("### Edição")
st.info("Para **Editar** ou **Cadastrar**, vá para a página 'Cadastro/Edição' na sidebar.")

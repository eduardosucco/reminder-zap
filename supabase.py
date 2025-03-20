"""
Módulo que lida com o banco de dados no Supabase (PostgreSQL).
Supondo que você já tenha uma tabela 'remedios' com as colunas:
    id (PK), nome, quantidade, frequencia, telefone, data_inicio, data_fim
"""

import os
from typing import List, Tuple
from supabase import create_client, Client

# Carrega as variáveis de ambiente (caso use python-dotenv, você pode fazer):
# from dotenv import load_dotenv
# load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://virdqpnbjolwocpsmafw.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpcmRxcG5iam9sd29jcHNtYWZ3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjUwMTkwOCwiZXhwIjoyMDU4MDc3OTA4fQ.sU2-IkLtpGbbUaYQXja50imYjf82i0RKCtAQi3vdbk4")

# Cria cliente do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_table():
    """
    Não faz nada aqui, pois assumimos que a tabela já foi criada
    manualmente no painel do Supabase.
    """
    pass

def inserir_remedio(nome: str,
                    quantidade: str,
                    frequencia: str,
                    telefone: str,
                    data_inicio: str,
                    data_fim: str) -> None:
    """
    Insere um novo remédio na tabela 'remedios'.
    :param nome: Nome do remédio
    :param quantidade: ex: "5ml", "1 comprimido"
    :param frequencia: ex: "a cada 8 horas"
    :param telefone: telefone no formato +55...
    :param data_inicio: "YYYY-MM-DD"
    :param data_fim: "YYYY-MM-DD"
    """
    data = {
        "nome": nome,
        "quantidade": quantidade,
        "frequencia": frequencia,
        "telefone": telefone,
        "data_inicio": data_inicio,
        "data_fim": data_fim
    }
    supabase.table("remedios").insert(data).execute()


def listar_remedios() -> List[Tuple]:
    """
    Lista todos os remédios da tabela 'remedios'.
    Retorna uma lista de tuplas no formato:
      (id, nome, quantidade, frequencia, telefone, data_inicio, data_fim)
    """
    # Faz o select de todas as colunas que precisamos
    result = supabase.table("remedios").select("*").execute()
    rows = result.data  # vem como lista de dicionários

    remedios = []
    for r in rows:
        # Garante que as chaves existem
        # (id, nome, quantidade, frequencia, telefone, data_inicio, data_fim)
        remedios.append((
            r["id"],
            r["nome"],
            r["quantidade"],
            r["frequencia"],
            r["telefone"],
            r["data_inicio"],
            r["data_fim"]
        ))
    return remedios

def remover_remedio(remedio_id: int) -> None:
    """
    Remove o remédio cujo 'id' seja igual ao remedio_id.
    """
    supabase.table("remedios").delete().eq("id", remedio_id).execute()

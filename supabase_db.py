"""
Arquivo local que contém as funções de CRUD no Supabase.
Renomeie para 'supabase_db.py' (ou outro nome).
"""

import os
from typing import List, Tuple
from supabase import create_client, Client  # Agora importa da biblioteca 'supabase-py'

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://virdqpnbjolwocpsmafw.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpcmRxcG5iam9sd29jcHNtYWZ3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjUwMTkwOCwiZXhwIjoyMDU4MDc3OTA4fQ.sU2-IkLtpGbbUaYQXja50imYjf82i0RKCtAQi3vdbk4")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_table():
    # Caso já tenha criado a tabela no painel do Supabase, não precisa fazer nada aqui.
    pass

def inserir_remedio(nome: str,
                    quantidade: str,
                    frequencia: str,
                    telefone: str,
                    data_inicio: str,
                    data_fim: str) -> None:
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
    result = supabase.table("remedios").select("*").execute()
    rows = result.data  # lista de dicionários
    remedios = []
    for r in rows:
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
    supabase.table("remedios").delete().eq("id", remedio_id).execute()

def atualizar_remedio(remedio_id: int,
                      nome: str,
                      quantidade: str,
                      frequencia: str,
                      telefone: str,
                      data_inicio: str,
                      data_fim: str) -> None:
    """
    Atualiza as informações de um remédio pelo ID, alterando os campos.
    As datas devem ser passadas em formato YYYY-MM-DD.
    """
    supabase.table("remedios") \
        .update({
            "nome": nome,
            "quantidade": quantidade,
            "frequencia": frequencia,
            "telefone": telefone,
            "data_inicio": data_inicio,
            "data_fim": data_fim
        }) \
        .eq("id", remedio_id) \
        .execute()

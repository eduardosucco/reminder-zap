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
    """
    Se você já criou a tabela manualmente ou via SQL, esta função pode ser apenas um "pass".
    Aqui como exemplo, deixo vazio.
    """
    pass

def listar_remedios():
    """
    Retorna apenas os registros com 'excluido' = 'N', preservando os dados de quem foi excluído logicamente.
    Retorna uma lista de tuplas: (id, nome, qtd, freq, telefone, data_inicio, data_fim, excluido)
    """
    resp = supabase.table("remedios") \
        .select("id, nome, quantidade, frequencia, telefone, data_inicio, data_fim, excluido") \
        .eq("excluido", "N") \
        .execute()
    
    data = resp.data  # lista de dicionários
    resultado = []
    for r in data:
        resultado.append((
            r["id"],
            r["nome"],
            r["quantidade"],
            r["frequencia"],
            r["telefone"],
            r["data_inicio"],
            r["data_fim"],
            r["excluido"]  # 'N'
        ))
    return resultado

def inserir_remedio(nome, quantidade, frequencia, telefone, data_inicio, data_fim):
    """Insere um novo registro em 'remedios' (excluido='N' por default)."""
    supabase.table("remedios").insert({
        "nome": nome,
        "quantidade": quantidade,
        "frequencia": frequencia,
        "telefone": telefone,
        "data_inicio": data_inicio,  # formato YYYY-MM-DD
        "data_fim": data_fim,        # formato YYYY-MM-DD
        "excluido": "N"
    }).execute()

def atualizar_remedio(remedio_id, nome, quantidade, frequencia, telefone, data_inicio, data_fim):
    """
    Atualiza os campos do remédio, sem mexer em 'excluido'.
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

def marcar_excluido(remedio_id):
    """Marca o remedio como excluido (S), mantendo-o no banco, mas fora da listagem."""
    supabase.table("remedios") \
        .update({"excluido": "S"}) \
        .eq("id", remedio_id) \
        .execute()
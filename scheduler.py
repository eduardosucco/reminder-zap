"""
Script que roda em background (ou no Codespaces) para enviar mensagens de lembrete
nos horários configurados.
"""
import time
import schedule
import datetime
from database import listar_remedios
from notifications.twilio_service import enviar_whatsapp

# Telefone(s) de destino (no formato E.164). Ex: "+5521XXXXXXXX"
DESTINOS = [
    "+5521981664493",  # Seu número
    "+5521988839535",  # Número da sua esposa
]

def job_enviar_lembretes():
    """
    Verifica se há algum remédio cujo horário de lembrete coincide com o momento atual
    e envia mensagem. Como exemplo, aqui vamos apenas enviar um lembrete diariamente
    às 08:00 e às 20:00 (exemplo fixo).
    """
    # Horário atual (HH:MM)
    agora = datetime.datetime.now().strftime("%H:%M")

    # Defina aqui os horários fixos (ex.: "08:00" e "20:00")
    horarios_lembrete = ["08:00", "20:00"]

    if agora in horarios_lembrete:
        # Lista todos os remédios
        lista = listar_remedios()
        if not lista:
            return

        # Monta uma mensagem simples com todos os remédios
        texto_remedios = "\n".join([
            f"- {item[1]} (Quantidade: {item[2]}, Freq: {item[3]})"
            for item in lista
        ])
        mensagem = f"Lembrete de Remédios:\n{texto_remedios}"

        # Envia para todos os números em DESTINOS
        for numero in DESTINOS:
            try:
                sid = enviar_whatsapp(mensagem, numero)
                print(f"Mensagem enviada para {numero}. SID: {sid}")
            except Exception as e:
                print(f"Erro ao enviar para {numero}: {e}")

def main():
    """
    Configura o schedule para rodar a cada 1 minuto, conferindo se deve
    disparar o lembrete (às 08:00 e 20:00, conforme exemplo).
    """
    # Verifica a função a cada 1 minuto
    schedule.every(1).minutes.do(job_enviar_lembretes)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()

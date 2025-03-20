"""
Script que roda em background para enviar mensagens de lembrete (WhatsApp) em horários específicos.
Em português BR, data no formato DD/MM/AAAA e hora HH:MM (24h).
"""

import schedule
import time
import datetime
from database import listar_remedios
from notifications.twilio_service import enviar_whatsapp_body

# Telefone(s) de destino no formato internacional SEM "whatsapp:" (deixe o script adicionar).
DESTINOS = [
    "+5521981664493",  # Seu número
    "+5521988839535",  # Número da sua esposa
]

def job_enviar_lembretes():
    """
    Verifica se é hora de enviar lembretes (08:00 ou 20:00 no exemplo)
    Formata a mensagem em português, puxa os dados do banco de dados
    e envia via WhatsApp para os números em DESTINOS.
    """
    agora = datetime.datetime.now()
    # Formato 24H para hora-minuto
    horario_atual = agora.strftime("%H:%M")
    # Formato DD/MM/AAAA para data
    data_atual = agora.strftime("%d/%m/%Y")

    # Horários em que deseja enviar notificações (24H).
    # Ajuste conforme suas necessidades.
    horarios_lembrete = ["08:00", "20:00"]

    if horario_atual in horarios_lembrete:
        # Busca todos os remédios no banco
        lista_remedios = listar_remedios()
        if not lista_remedios:
            return  # Se não há remédios cadastrados, não envia nada

        # Monta o cabeçalho da mensagem
        cabecalho = (
            f"Lembrete de Medicamentos\n"
            f"Data: {data_atual}\n"
            f"Horário: {horario_atual}\n\n"
            f"Você precisa tomar:\n"
        )

        corpo_remedios = ""
        for item in lista_remedios:
            # A estrutura do item é: (id, nome, quantidade, frequencia, data_inicio, data_fim)
            remedio_id, nome, quantidade, frequencia, data_inicio, data_fim = item

            # data_inicio/data_fim vêm no formato YYYY-MM-DD, então convertemos para DD/MM/AAAA
            try:
                inicio_formatado = datetime.datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError:
                inicio_formatado = data_inicio  # se der erro, deixa como está

            try:
                fim_formatado = datetime.datetime.strptime(data_fim, "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError:
                fim_formatado = data_fim

            # Montamos uma linha descrevendo o remédio
            corpo_remedios += (
                f"- {nome}, {quantidade}, {frequencia}.\n"
                f"  Início: {inicio_formatado}, Término: {fim_formatado}\n\n"
            )

        mensagem = cabecalho + corpo_remedios

        # Envia a mensagem para cada número de destino
        for numero in DESTINOS:
            try:
                sid = enviar_whatsapp_body(numero, mensagem)
                print(f"Mensagem enviada para {numero}, SID: {sid}")
            except Exception as e:
                print(f"Erro ao enviar para {numero}: {e}")

def main():
    """
    Configura a verificação a cada 1 minuto para ver se é hora de disparar a notificação.
    """
    schedule.every(1).minutes.do(job_enviar_lembretes)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()

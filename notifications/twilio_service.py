"""
Módulo responsável por enviar mensagens via Twilio (WhatsApp).
Exemplos de envio usando body simples ou content_sid + content_variables (modelo de template).
"""

import os
from twilio.rest import Client

# -----------------------------------------------------------------------------
# DICAS DE SEGURANÇA:
# Em produção, NÃO deixe os dados expostos em texto puro no código.
# Utilize variáveis de ambiente ou algum cofre seguro para armazenar:
# - TWILIO_ACCOUNT_SID
# - TWILIO_AUTH_TOKEN
# -----------------------------------------------------------------------------
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "SEU_SID_AQUI")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "SEU_TOKEN_AQUI")

# Número do WhatsApp de origem (o 'sandbox' da Twilio normalmente é +14155238886)
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "+14155238886")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def enviar_whatsapp_body(to_number: str, mensagem: str) -> str:
    """
    Envia mensagem WhatsApp usando o parâmetro 'body'.
    :param to_number: Número de destino (ex.: +5521981664493) SEM o 'whatsapp:' no começo
    :param mensagem: Texto da mensagem a ser enviada
    :return: SID da mensagem enviada
    """
    message = client.messages.create(
        from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
        body=mensagem,
        to=f"whatsapp:{to_number}"
    )
    return message.sid


def enviar_whatsapp_template(to_number: str,
                             content_sid: str,
                             content_variables: dict) -> str:
    """
    Envia mensagem WhatsApp usando 'content_sid' (template Twilio) e 'content_variables'.
    :param to_number: Número de destino (ex.: +5521981664493) SEM o 'whatsapp:' no começo
    :param content_sid: SID do template de conteúdo criado no Twilio
    :param content_variables: Dicionário (JSON) com variáveis do template
    :return: SID da mensagem enviada
    """
    # content_variables deve ser serializado como string JSON, ex.: '{"1":"12/1","2":"3pm"}'
    # Então, se você passar um dict python, transformamos em string:
    import json
    content_vars_str = json.dumps(content_variables)

    message = client.messages.create(
        from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
        content_sid=content_sid,
        content_variables=content_vars_str,
        to=f"whatsapp:{to_number}"
    )
    return message.sid


if __name__ == "__main__":
    """
    Exemplo rápido de teste local (ENVIE APENAS PARA NÚMEROS QUE JÁ INTERAGIRAM COM O SANDBOX!)
    Mude 'SEU_NUMERO' para o seu e 'NUMERO_DA_ESPOSA' para sua esposa.
    Lembre-se de que Twilio só permite no trial enviar para números verificados ou que tenham
    interagido com o sandbox.
    """

    # Altere para os números desejados, sem o prefixo 'whatsapp:':
    meu_numero = "5521981664493"      # Seu número
    esposa_numero = "5521988839535"   # Número da esposa

    # 1) Exemplo de envio com body simples
    sid1 = enviar_whatsapp_body(
        to_number=meu_numero,
        mensagem="Olá! Este é um lembrete de teste pelo Twilio (usando body)."
    )
    print("SID da mensagem (body) para você:", sid1)

    sid2 = enviar_whatsapp_body(
        to_number=esposa_numero,
        mensagem="Olá! Este é um lembrete de teste para sua esposa (usando body)."
    )
    print("SID da mensagem (body) para sua esposa:", sid2)

    # 2) Exemplo de envio com content_sid + content_variables (template)
    # Supondo que você tenha um template no Twilio (content_sid) como "HXb5b62575e6e4ff6129ad7c8efe1f983e"
    # e queira passar variáveis para o template.
    content_sid_exemplo = "HXb5b62575e6e4ff6129ad7c8efe1f983e"
    variables_exemplo = {
        "1": "12/1",
        "2": "3pm"
    }

    sid3 = enviar_whatsapp_template(
        to_number=meu_numero,
        content_sid=content_sid_exemplo,
        content_variables=variables_exemplo
    )
    print("SID da mensagem (template) para você:", sid3)

    sid4 = enviar_whatsapp_template(
        to_number=esposa_numero,
        content_sid=content_sid_exemplo,
        content_variables=variables_exemplo
    )
    print("SID da mensagem (template) para sua esposa:", sid4)

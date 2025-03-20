# Gerenciador de Remédios (Streamlit + WhatsApp)

Aplicação simples para **cadastrar remédios** e **enviar lembretes** via WhatsApp (usando Twilio).  
Utiliza **Streamlit** para a interface, **SQLite** como banco de dados e a biblioteca **schedule** para o agendamento.

## Como Funciona
1. **Cadastro e Consulta**: Pelo Streamlit (`app.py`), você insere o nome do remédio, quantidade/dose, frequência, data de início e data de término.  
2. **Banco de Dados**: Tudo fica gravado em um arquivo SQLite local (`remedios.db`).  
3. **Lembretes Automáticos**: Um script separado (`scheduler.py`) verifica os horários escolhidos (ex.: 08:00 e 20:00) e envia mensagens de WhatsApp via Twilio para os números configurados.

## Instruções Rápidas
1. **Clonar** o projeto e entrar na pasta:
   ```bash
   git clone https://github.com/SEU_USUARIO/meu_projeto.git
   cd meu_projeto
   ```
2. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Definir Variáveis de Ambiente** (dados da Twilio):
   ```bash
   export TWILIO_ACCOUNT_SID="SEU_SID"
   export TWILIO_AUTH_TOKEN="SEU_TOKEN"
   export TWILIO_WHATSAPP_NUMBER="+14155238886"
   ```
4. **Executar** o app Streamlit:
   ```bash
   streamlit run app.py
   ```
5. **Agendar Envio** (em outro terminal):
   ```bash
   python scheduler.py
   ```

## Observações
- Em modo **trial** da Twilio, só é possível enviar para números que tenham interagido com o **WhatsApp Sandbox** ou estejam verificados.  
- O `scheduler.py` precisa **ficar rodando** para os lembretes funcionarem.  
- Ajuste os horários no arquivo `scheduler.py` (por padrão, 08:00 e 20:00).  
- Para uso **em produção**, configure o **WhatsApp Business** via Twilio e libere seus modelos de mensagem.

**Bom desenvolvimento!**  

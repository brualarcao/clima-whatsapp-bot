import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import requests

# Configurações
API_KEY = os.getenv("OWM_API_KEY")
LAT = "-23.0264"
LON = "-45.5553"
UNITS = "metric"
LANG = "pt_br"

# E-mail
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

DIAS_SEMANA = {
    "Monday": "Segunda-Feira",
    "Tuesday": "Terça-Feira",
    "Wednesday": "Quarta-Feira",
    "Thursday": "Quinta-Feira",
    "Friday": "Sexta-Feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

def obter_temperaturas():
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&units={UNITS}&lang={LANG}&appid={API_KEY}"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        hoje = dados["daily"][0]
        return hoje["temp"]["min"], hoje["temp"]["max"]
    else:
        raise Exception(f"Erro na API: {resposta.status_code} - {resposta.text}")

def enviar_email(temp_min, temp_max):
    hoje = datetime.now()
    data = hoje.strftime("%d/%m/%Y")
    dia_semana = DIAS_SEMANA.get(hoje.strftime("%A"), hoje.strftime("%A"))
    temp_media = (temp_min + temp_max) / 2

    assunto = f"☁️ Clima do dia - {data}"

    corpo_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 500px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
          <h2 style="color: #1e90ff; text-align: center;">🌤️ Previsão do Dia</h2>
          <p><strong>📅 Data:</strong> {data}</p>
          <p><strong>📆 Dia da Semana:</strong> {dia_semana}</p>
          <hr style="border: none; border-top: 1px solid #eee;">
          <p><strong>🌡️ Temperatura Mínima:</strong> {temp_min:.2f}°C</p>
          <p><strong>🌡️ Temperatura Máxima:</strong> {temp_max:.2f}°C</p>
          <p><strong>🌡️ Temperatura Média:</strong> {temp_media:.2f}°C</p>
          <hr style="border: none; border-top: 1px solid #eee;">
          <p style="font-style: italic; color: #555;">Tenha uma ótima tarde! 😊</p>
          <p style="text-align: right; font-weight: bold; color: #c62828;">♥️ Amo você, b.</p>
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo_html, "html"))

    # Enviar e-mail via SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

    print("E-mail enviado com sucesso.")


def main():
    try:
        temp_min, temp_max = obter_temperaturas()
        enviar_email(temp_min, temp_max)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()

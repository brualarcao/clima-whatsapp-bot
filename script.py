import requests
from datetime import datetime
import os

# Variáveis de ambiente
API_KEY = os.getenv("OWM_API_KEY")
LAT = "-23.0264"
LON = "-45.5553"
UNITS = "metric"
LANG = "pt_br"
WHATSAPP_NUMBER = "5512991302647"
TOKEN = os.getenv("WHATSAPP_TOKEN")

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

def enviar_mensagem(temp_min, temp_max):
    hoje = datetime.now()
    data = hoje.strftime("%d/%m/%Y")
    dia_semana = DIAS_SEMANA.get(hoje.strftime("%A"), hoje.strftime("%A"))
    temp_media = (temp_min + temp_max) / 2

    mensagem = (
        f"📅 *Data*: {data}\n"
        f"📆 *Dia da Semana*: {dia_semana}\n"
        f"🌡️ *Temp. Mínima*: {temp_min:.2f}°C\n"
        f"🌡️ *Temp. Máxima*: {temp_max:.2f}°C\n"
        f"🌡️ *Temp. Média*: {temp_media:.2f}°C\n"
        "\nTenha uma ótima tarde! 😊\nAmo você b, ♥️"
    )

    url = f"https://api.callmebot.com/whatsapp.php?phone={WHATSAPP_NUMBER}&text={requests.utils.quote(mensagem)}&apikey={TOKEN}"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        print("Mensagem enviada com sucesso.")
    else:
        print(f"Erro ao enviar mensagem: {resposta.text}")

def main():
    try:
        temp_min, temp_max = obter_temperaturas()
        enviar_mensagem(temp_min, temp_max)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()

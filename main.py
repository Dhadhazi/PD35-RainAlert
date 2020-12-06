import requests
import os
from twilio.rest import Client

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API")
account_sid = "AC3ece9797be922418acd882010f01d60d"
auth_token = os.environ.get("TWILIO_AUTH")

weather_params = {
    "lat": 52.370216,
    "lon": 4.895168,
    "exclude" : "current,minutely,daily",
    "appid": api_key
}


def get_weather_data():
    response = requests.get(OWM_Endpoint, params=weather_params)
    response.raise_for_status()
    return response.json()


def will_it_rain(weather_data):
    rain = False
    for i in range(0, 12):
        id = weather_data["hourly"][i]["weather"][0]["id"]
        if id < 700:
            rain = True
    return rain


def send_text():
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                         body="It will rain. Bring an umbrella!",
                         from_='+16096045754',
                         to='+31645257600'
                     )
    print(message.status)

if will_it_rain(get_weather_data()):
    send_text()
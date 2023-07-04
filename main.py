import os
from requests import *
from twilio.rest import Client

api_key = os.environ['API_KEY']

account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
from_phone = os.environ['FROM_PHONE_NUMBER']
to_phone = os.environ['TO_PHONE_NUMBER']

parameters = {
    "lat": 47.700634,
    "lon": 19.289368,
    "appid": api_key,
}

response = get("https://pro.openweathermap.org/data/2.5/forecast/hourly", params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data['weather'][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today.\nRemember to bring an ☂!",
        from_=from_phone,
        to=to_phone)
    print(message.status)

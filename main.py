import requests
import arrow
import pytz
from datetime import datetime
import smtplib
from email.message import EmailMessage

geoloc = requests.get("https://ipinfo.io").json()
loc = (geoloc.get('loc')).split(',')

tz = geoloc.get('timezone')
tz = pytz.timezone(tz)
now = datetime.now(tz)
offset = now.strftime("%z")  # e.g. +0300
offset_formatted = f"GMT{offset[:-2]}:{offset[-2:]}"

start = arrow.now(tz).floor('day').to('UTC').format('YYYY-MM-DD HH:mm:ss')
end   = arrow.now(tz).ceil('day').to('UTC').format('YYYY-MM-DD HH:mm:ss')

key = "82c233d8-8e8d-11f0-b41a-0242ac130006-82c2348c-8e8d-11f0-b41a-0242ac130006"
try:
  response = requests.get(
      'https://api.stormglass.io/v2/weather/point',
      params={
          'lat': loc[0],
          'lng': loc[1],
          'params': ','.join(['windSpeed', 'airTemperature', 'cloudCover']),
          'start': start,
          'end': end,
    },
      headers={
          'Authorization': f'{key}'
    },
    timeout=10
  )
  response.raise_for_status()
  try:
    data = response.json()
    
  except requests.exceptions.JSONDecodeError as err:
    print(f"JSON Decode error: {err}")
    
except requests.exceptions.HTTPError as err:
  print(f"HTTP error: {err}")
  
except requests.exceptions.RequestException as e:
  print(f"An error occured: {e}")
  
hours = data['hours']
city = geoloc.get('city')

lines = []
#manipulating data to make readable lines of info
for hour in hours:
    time = hour['time']
    temp = hour['airTemperature']['sg']
    wind = hour['windSpeed']['sg']
    clouds = hour['cloudCover']['sg']
    lines.append(f"{time} | Temp: {temp}°C | Wind: {wind} m/s | Clouds: {clouds}%| City: {city}")
    
forecast_text = "\n".join(lines)
#sandbox email because actual sending isnt needed, response is printed
msg = EmailMessage()
msg["Subject"] = f"Daily Weather Forecast for {city}"
msg["From"] = "hello@www.portgo.xyz"
msg["To"] = "blackangelmusic22@gmail.com"

msg.set_content(forecast_text)

with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
    server.starttls()
    server.login("7ae883b3569372", "dc68b68186cf0b")
    server.send_message(msg)
    
print(forecast_text)
        

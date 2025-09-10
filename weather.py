import requests

key = "82c233d8-8e8d-11f0-b41a-0242ac130006-82c2348c-8e8d-11f0-b41a-0242ac130006"
response = requests.get(
    'https://api.stormglass.io/v2',
    params={
        'lat': 58.7984,
        'lng': 17.8081,
        'params': 'windSpeed',
  },
    headers={
        'Authorization': f'{key}'
  })

data = response.json()
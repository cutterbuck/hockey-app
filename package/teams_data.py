import requests, json


response = requests.get('https://statsapi.web.nhl.com/api/v1/teams')
teams_data = json.loads(response.content)['teams']

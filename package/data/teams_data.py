import requests, json


response = requests.get('https://statsapi.web.nhl.com/api/v1/teams')
teams_data = json.loads(response.content)['teams']



# team colors

team_colors = {
    'ANA': {'primary': 'rgb(252,76,2)', 'secondary': 'rgb(176,152,98)'},
    'ARI': {'primary': 'rgb(140,38,51)', 'secondary': 'rgb(226,214,181)'},
    'BOS': {'primary': 'rgb(255,184,28)', 'secondary': 'rgb(0,0,0)'},
    'BUF': {'primary': 'rgb(4,30,66)', 'secondary': 'rgb(255,184,28)'},
    'CGY': {'primary': 'rgb(200,16,46)', 'secondary': 'rgb(241, 190, 72)'},
    'CAR': {'primary': 'rgb(226,24,54)', 'secondary': 'rgb(35,31,32)'},
    'CHI': {'primary': 'rgb(200,16,46)', 'secondary': 'rgb(255,103,27)'},
    'COL': {'primary': 'rgb(111,38,61)', 'secondary': 'rgb(35,97,146)'},
    'CBJ': {'primary': 'rgb(4,30,66)', 'secondary': 'rgb(200,16,46)'},
    'DAL': {'primary': 'rgb(0,99,65)', 'secondary': 'rgb(162,170,173)'},
    'DET': {'primary': 'rgb(200,16,46)', 'secondary': 'rgb(255,255,255)'},
    'EDM': {'primary': 'rgb(4,30,66)', 'secondary': 'rgb(252,76,2)'},
    'FLA': {'primary': 'rgb(4,30,66)', 'secondary': 'rgb(185,151,91)'},
    'LAK': {'primary': 'rgb(0,0,0)', 'secondary': 'rgb(162,170,173)'},
    'MIN': {'primary': 'rgb(21,71,52)', 'secondary': 'rgb(166,25,46)'},
    'MTL': {'primary': 'rgb(166,25,46)', 'secondary': 'rgb(0,30,98)'},
    'NSH': {'primary': 'rgb(238,173,30)', 'secondary': 'rgb(4,30,66)'},
    'NJD': {'primary': 'rgb(200,16,46)', 'secondary': 'rgb(0,0,0)'},
    'NYI': {'primary': 'rgb(0,83,155)', 'secondary': 'rgb(244, 125, 48)'},
    'NYR': {'primary': 'rgb(0,56,168)', 'secondary': 'rgb(200,16,46)'},
    'OTT': {'primary': 'rgb(200,16,46)', 'secondary': 'rgb(198,146,20)'},
    'PHI': {'primary': 'rgb(250,70,22)', 'secondary': 'rgb(0,0,0)'},
    'PIT': {'primary': 'rgb(0,0,0)', 'secondary': 'rgb(252,181,20)'},
    'STL': {'primary': 'rgb(0,48,135)', 'secondary': 'rgb(255,184,28)'},
    'SJS': {'primary': 'rgb(0,98,114)', 'secondary': 'rgb(229,114,0)'},
    'TBL': {'primary': 'rgb(0,32,91)', 'secondary': 'rgb(0,0,0)'},
    'TOR': {'primary': 'rgb(0,32,91)', 'secondary': 'rgb(255,255,255)'},
    'VAN': {'primary': 'rgb(0,32,91)', 'secondary': 'rgb(10,134,61)'},
    'VGK': {'primary': 'rgb(185,151,91)', 'secondary': 'rgb(51,63,72)'},
    'WSH': {'primary': 'rgb(200,16,46)', 'secondary': 'rgb(4,30,66)'},
    'WPG': {'primary': 'rgb(4,30,66)', 'secondary': 'rgb(85,86,90)'}
}

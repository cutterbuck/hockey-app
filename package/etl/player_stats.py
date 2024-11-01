# import os, pandas
# import re
#
# cwd = os.getcwd()
#
# # stats data
# names = ["Player", "Season", "Team", "Position", "GP", "TOI", "G", "A", "P", "P1", "P/60", "P1/60", "GS", "GS/60", "CF", "CA", "C+/-", "CF%", "Rel CF%", "GF", "GA", "G+/-", "GF%", "Rel GF%", "xGF", "xGA", "xG+/-", "xGF%", "Rel xGF%", "iPENT", "iPEND", "iP+/-", "iCF", "iCF/60", "ixGF", "ixGF/60", "iSh%", "PDO", "ZSR", "TOI%", "TOI% QoT", "CF% QoT", "TOI% QoC", "CF% QoC"]
#
#
# seventeen_eighteen = pandas.read_csv(cwd+'/2017_18.csv', names=names)
# sixteen_seventeen = pandas.read_csv(cwd+'/2016_17.csv', names=names)
# fifteen_sixteen = pandas.read_csv(cwd+'/2015_16.csv', names=names)
#
#
# seventeen_eighteen[names] = seventeen_eighteen[names].replace('--', 0)
# sixteen_seventeen[names] = sixteen_seventeen[names].replace('--', 0)
# fifteen_sixteen[names] = fifteen_sixteen[names].replace('--', 0)
#
# s1 = seventeen_eighteen.to_dict('records')[1:]
# s2 = sixteen_seventeen.to_dict('records')[1:]
# s3 = fifteen_sixteen.to_dict('records')[1:]
#
# data = s1+s2+s3
#
# for player in data:
#     if '..' in player['Player']:
#         first, last = player['Player'].split('..')
#         player['Player'] = first.replace(" ", "").upper() + " " + last.title()
#     elif len(player['Player'].split(" ")[0]) == 2:
#         first, last = player['Player'].split(' ')
#         player['Player'] = first.upper() + " " + last.title()
#     elif bool(re.search(r'\d', player['Player'])):
#         if player['Player'].startswith('5'):
#             player['Player'] = player['Player'].replace('5', 'S')
#
#     if '/' in player['Team']:
#         player['Team'] = player['Team'].split('/ ')[-1]
#
#     if player['Team'] == 'N.J':
#         player['Team'] = 'NJD'
#     elif player['Team'] == 'T.B':
#         player['Team'] = 'TBL'
#     elif player['Team'] == 'L.A':
#         player['Team'] = 'LAK'
#     elif player['Team'] == 'S.J':
#         player['Team'] = 'SJS'
#
#
# # cap hit data
# raw = pandas.read_csv(cwd+'/contracts.csv',usecols=["Player", "Cap Hit"])
# raw.fillna('0', inplace=True)
# cap_hits = raw.to_dict('records')[1:]
#
# for player in cap_hits:
#     player['Player'] = player['Player'].lower()
#     player['Player'] = re.sub(r'(?<!\w)([a-z])\.', r'\1', player['Player'])
#     comma_strip = player['Cap Hit'].replace(',', '')
#     player['Cap Hit'] = int(comma_strip)
#
# # player ages
# raw_ages = pandas.read_csv(cwd+'/player_age.csv', usecols=["Player", "Age"])
# ages = raw_ages.to_dict('records')[1:]
# for player in ages:
#     player['Player'] = player['Player'].split("\\")[0]
#     player['Player'] = player['Player'].lower()
#     player['Player'] = re.sub(r'(?<!\w)([a-z])\.', r'\1', player['Player'])

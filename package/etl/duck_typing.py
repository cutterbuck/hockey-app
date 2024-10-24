from models import *

# leagues
nhl = League(name='NHL')
ahl = League(name='AHL')
db.session.add_all([nhl, ahl])


# teams
rangers = Team(name="New York Rangers")
sabres = Team(name='Buffalo Sabres')
wolfpack = Team(name='Hartford Wolfpack')
americans = Team(name='Rochester Americans')
teams = [rangers, sabres, wolfpack, americans]
rangers.affiliates.append(wolfpack)
sabres.affiliates.append(americans)
rangers.league = nhl
sabres.league = nhl
americans.league = ahl
db.session.add_all(teams)


# seasons
twenty4_twenty5_season = Season(start_year=2024, end_year=2025)
db.session.add(twenty4_twenty5_season)
twenty1_twenty2_season.teams.extend(teams)


# players
tuch = Player(name="Alex Tuch")
db.session.add(tuch)


tuch_vegas_stats = PlayerStats(player=tuch, season=twenty1_twenty2_season, team=vgk)
tuch_sabre_stats = PlayerStats(player=tuch, season=twenty1_twenty2_season, team=sabres)

db.session.commit()
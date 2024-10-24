from package.models import *


# leagues
nhl = League(name='NHL')
ahl = League(name='AHL')

# teams
rangers = Team(name="New York Rangers")
sabres = Team(name='Buffalo Sabres')
vgk = Team(name='Vegas Golden Knights')
wolfpack = Team(name='Hartford Wolfpack')
americans = Team(name='Rochester Americans')
teams = [rangers, sabres, wolfpack, americans]
rangers.affiliates.append(wolfpack)
sabres.affiliates.append(americans)
rangers.league = nhl
sabres.league = nhl
americans.league = ahl

# seasons
twenty4_twenty5_season = Season(start_year=2024, end_year=2025)
twenty4_twenty5_season.teams.extend(teams)

# players
tuch = Player(full_name="Alex Tuch")

tuch_vegas_stats = PlayerStats(player=tuch, season=twenty4_twenty5_season, team=vgk)
tuch_sabre_stats = PlayerStats(player=tuch, season=twenty4_twenty5_season, team=sabres)


# import pdb; pdb.set_trace()
# db.session.add_all([nhl, ahl])
# db.session.add_all(teams)
# db.session.add(twenty4_twenty5_season)
# db.session.add(tuch)
# db.session.commit()
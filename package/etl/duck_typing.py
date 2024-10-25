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
teams = [rangers, sabres, vgk, wolfpack, americans]
rangers.farm_teams.append(wolfpack)
sabres.farm_teams.append(americans)
rangers.league = nhl
sabres.league = nhl
vgk.league = nhl
wolfpack.league = ahl
americans.league = ahl

# seasons
twenty4_twenty5_season = Season(start_year=2024, end_year=2025, name='2024-25')
twenty4_twenty5_season.teams.extend(teams)

# players
tuch = Player(full_name="Alex Tuch")
laf = Player(full_name="Alexis Lafreniere")
rempe = Player(full_name="Matt Rempe")

tuch_vegas_stats = PlayerStats(player=tuch, season=twenty4_twenty5_season, team=vgk)
tuch_sabre_stats = PlayerStats(player=tuch, season=twenty4_twenty5_season, team=sabres)
laf_rangers_stats = PlayerStats(player=laf, season=twenty4_twenty5_season, team=rangers)
rempe_rangers_stats = PlayerStats(player=rempe, season=twenty4_twenty5_season, team=rangers)
rempe_wolfpack_stats = PlayerStats(player=rempe, season=twenty4_twenty5_season, team=wolfpack)

db.session.add_all([nhl, ahl])
db.session.add_all(teams)
db.session.add(twenty4_twenty5_season)
db.session.add_all([tuch, laf, rempe])
db.session.add_all([tuch_vegas_stats, tuch_sabre_stats, laf_rangers_stats, rempe_rangers_stats, rempe_wolfpack_stats])
db.session.commit()
import pdb; pdb.set_trace()

from teams_data import teams_data
from player_stats import data
from models import Team, Player, Season, Statistic, db


def create_team_objects():
    for team in teams_data:
        team_obj = Team(name=team['name'], abbreviation=team['abbreviation'], city=team['venue']['city'], arena=team['venue']['name'], division=team['division']['name'], conference=team['conference']['name'], official_site=team['officialSiteUrl'])
        db.session.add(team_obj)
    db.session.commit()

def create_player_objects():
    for player in data:
        if bool(db.session.query(Player).filter_by(name=player['Player']).first()) == False:
            player_obj = Player(name=player['Player'], position=player['Position'][0])
            db.session.add(player_obj)
    db.session.commit()

def create_weighted_cf(player):
    if int(player['CF']) != 0:
        weighted_cf = 100*(int(player['GF'])/int(player['CF']))
        return round(weighted_cf, 2)

def create_weighted_ca(player):
    if int(player['CA']) != 0:
        weighted_ca = 100*(int(player['GA'])/int(player['CA']))
        return round(weighted_ca, 2)

def create_weighted_corsi_percent(player):
    if create_weighted_cf(player) and create_weighted_ca(player):
        wc_denom = create_weighted_cf(player)+create_weighted_ca(player)
        return round(100*(create_weighted_cf(player)/wc_denom), 2)


def create_season_and_stat_objects():
    for player in data:
        player_search = Player.query.filter_by(name=player['Player']).first()
        team_search = Team.query.filter_by(abbreviation=player['Team']).first()
        stat_line = Statistic(end_yr_team=player['Team'], games_played=int(player['GP']), time_on_ice=round(float(player['TOI']),2), goals=int(player['G']), assists=int(player['A']), points=int(player['P']), primary_points=int(player['P1']), pts_per_60=round(float(player['P/60']),2), p_pts_per_60=round(float(player['P1/60']),2), cf=int(player['CF']), ca=int(player['CA']), corsi_plus_minus=int(player['C+/-']), cf_percentage=round(float(player['CF%']),2), rel_cf=round(float(player['Rel CF%']),2), gf=int(player['GF']), ga=int(player['GA']), plus_minus=int(player['G+/-']), pdo=round(float(player['PDO']),2), zsr=round(float(player['ZSR']),2), weighted_cf=create_weighted_cf(player), weighted_ca=create_weighted_ca(player), weighted_corsi_percentage=create_weighted_corsi_percent(player))
        season = Season(year=player['Season'], player=player_search, team=team_search, statistic=stat_line)
        db.session.add(season)
    db.session.commit()

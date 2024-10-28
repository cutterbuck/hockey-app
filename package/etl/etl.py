from package.models import *
import requests, json
from package.data.team_colors import team_colors
from nhlpy import NHLClient

client = NHLClient()

def create_team_objects():
    teams = client.teams.teams_info()
    for team in teams:
        team_obj = Team(name=team['name'], abbr=team['abbr'], common_name=team['common_name'], logo=team['logo'])
        db.session.add(team_obj)
    db.session.commit()

def create_season_object(season_id):
    new_season = Season(id=season_id, start_year=int(str(season_id)[0:4]), end_year=int(str(season_id)[-4:]), name=str(season_id)[0:4] + '-' + str(season_id)[-2:])
    db.session.add(new_season)
    print('Adding Season() for', new_season.name)
    db.session.commit()
    return new_season

def get_standings(past_season_id=None):
    if past_season_id:
        standings = client.standings.get_standings(season=past_season_id)
    else:
        standings = client.standings.get_standings()

    for team in standings['standings']:
        team_obj = Team.query.filter(Team.name == team['teamName']['default']).first()
        season_obj = Season.query.filter(Season.id == team['seasonId']).first()

        if bool(season_obj) == False:
            season_obj = create_season_object(team['seasonId'])
        if season_obj not in team_obj.seasons:
            team_obj.seasons.append(season_obj)
        team_stats_obj = TeamStats.query.filter(TeamStats.team == team_obj, TeamStats.season == season_obj).first()
        team_stats_obj.games_played = team['gamesPlayed']
        team_stats_obj.wins = team['wins']
        team_stats_obj.losses = team['losses']
        team_stats_obj.ties = team['ties']
        team_stats_obj.shootout_wins = team['shootoutWins']
        team_stats_obj.points = team['points']
        team_stats_obj.goals_forward = team['goalFor']
        team_stats_obj.goals_against = team['goalAgainst']
        team_stats_obj.l10_wins = team['l10Wins']
        team_stats_obj.regulation_wins = team['regulationWins']
        team_stats_obj.regulation_plut_ot_wins = team['regulationPlusOtWins']
        team_stats_obj.goal_differential = team['goalDifferential']
        db.session.add(team_stats_obj)
        print("Updating standings for", team_obj.name)
    db.session.commit()
# create_team_objects()
# get_standings()
# import pdb; pdb.set_trace()

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

def add_cap_hit_info():
    for player in Player.query.all():
        lower_case = player.name.lower()
        for cap_hit in cap_hits:
            if lower_case == cap_hit['Player']:
                player.cap_hit = int(cap_hit['Cap Hit'])
                db.session.add(player)
    db.session.commit()

def add_age_info():
    for player in Player.query.all():
        lower_case = player.name.lower()
        for age in ages:
            if lower_case == age['Player']:
                player.age = age['Age']
                db.session.add(player)
    db.session.commit()

def add_colors_to_teams():
    for team_obj in Team.query.all():
        for team, colors in team_colors.items():
            if team_obj.abbreviation == team:
                team_obj.primary_color = colors['primary']
                team_obj.secondary_color = colors['secondary']
                db.session.add(team_obj)
    db.session.commit()




def add_all_to_db():
    create_team_objects()
    create_player_objects()
    create_season_and_stat_objects()
    add_cap_hit_info()
    add_age_info()
    add_colors_to_teams()
# add_all_to_db()

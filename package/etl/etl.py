from package.models import *
from package.data.misc_data import *
import requests
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from nhlpy import NHLClient
client = NHLClient()


def create_or_update_leagues():
    for league in leagues:
        league_obj = League.query.filter(League.name == league['name']).first()
        if bool(league_obj) == False:
            league_obj = League(name=league['name'])
            print('Creating League() for', league_obj.name)
        db.session.add(league_obj)
    db.session.commit()

def create_or_update_conferences():
    for conf in conferences:
        conf_obj = Conference.query.filter(Conference.name == conf['name']).first()
        if bool(conf_obj) == False:
            conf_obj = Conference(name=conf['name'])
            print('Creating Conference() for', conf_obj.name)
        db.session.add(conf_obj)
    db.session.commit()

def create_or_update_divisions():
    for division in divisions:
        division_obj = Division.query.filter(Division.name == division['name']).first()
        if bool(division_obj) == False:
            conf_obj = Conference.query.filter(Conference.name == division['conference']).first()
            division_obj = Division(name=division['name'], conference=conf_obj)
            print('Creating Division() for', division_obj.name)
        db.session.add(division_obj)
    db.session.commit()
# create_or_update_leagues()
# create_or_update_conferences()
# create_or_update_divisions()

def create_or_update_season_objects():
    for season in seasons:
        season_obj = Season.query.filter(Season.name == season['name']).first()
        if bool(season_obj) == False:
            season_id = int(str(season['start_date'].year) + str(season['end_date'].year))
            season_obj = Season(id=season_id, start_date=season['start_date'], end_date=season['end_date'], name=season['name'])
        db.session.add(season_obj)
        print('Adding Season() for', season_obj.name)
    db.session.commit()
# create_or_update_season_objects()

def create_team_objects():
    # adds all historical franchises
    franchises = client.teams.all_franchises()
    franchises = sorted(franchises, key=lambda d: d['id'])
    for team in franchises:
        team_obj = Team(name=team['fullName'], common_name=team['teamCommonName'], location=team['teamPlaceName'])
        db.session.add(team_obj)
        print("Adding the", team_obj.name)
    db.session.commit()

    # adds logo and abbreviation to current teams
    teams = client.teams.teams_info()
    for team in teams:
        team_obj = Team.query.filter(Team.name==team['name']).first()
        team_obj.abbr = team['abbr']
        team_obj.logo = team['logo']
        db.session.add(team_obj)
    db.session.commit()

    coyotes = Team.query.filter(Team.name=='Arizona Coyotes').first()
    coyotes.abbr = 'ARI'
    coyotes.logo = 'https://assets.nhle.com/logos/nhl/svg/ARI_light.svg'

    db.session.add(coyotes)
    db.session.commit()
# create_team_objects()

def get_standings(prior_seasons_end_date=None):
    if prior_seasons_end_date:
        standings = client.standings.get_standings(date=prior_seasons_end_date)
    else:
        standings = client.standings.get_standings()

    for team in standings['standings']:
        team_obj = Team.query.filter(Team.name == team['teamName']['default']).first()
        season_obj = Season.query.filter(Season.id == team['seasonId']).first()
        if season_obj not in team_obj.seasons:
            team_obj.seasons.append(season_obj)

        team_stats_obj = TeamStandings.query.filter(TeamStandings.team == team_obj, TeamStandings.season == season_obj).first()
        team_stats_obj.games_played = team['gamesPlayed']
        team_stats_obj.wins = team['wins']
        team_stats_obj.losses = team['losses']
        team_stats_obj.ties = team['ties']
        team_stats_obj.shootout_wins = team['shootoutWins']
        team_stats_obj.points = team['points']
        team_stats_obj.points_percentage = round(team['pointPctg'], 3)
        team_stats_obj.goals_for = team['goalFor']
        team_stats_obj.goals_against = team['goalAgainst']
        team_stats_obj.goal_differential = team['goalDifferential']
        team_stats_obj.l10_wins = team['l10Wins']
        team_stats_obj.regulation_wins = team['regulationWins']
        team_stats_obj.regulation_plut_ot_wins = team['regulationPlusOtWins']
        conference_obj = Conference.query.filter(Conference.name == team['conferenceName']).first()
        division_obj = Division.query.filter(Division.name == team['divisionName']).first()
        team_stats_obj.division = division_obj
        db.session.add(team_stats_obj)
        print("Updating", season_obj.name, "standings for", team_obj.name)
    db.session.commit()
# get_standings('2023-04-14')
# get_standings('2024-04-18')
get_standings()
import pdb; pdb.set_trace()

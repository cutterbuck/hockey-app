from teams_data import teams_data
from player_stats import data
from models import Team, Player, Season, Statistic, db


def create_team_objects():
    for team in teams_data:
        team_obj = Team(name=team['name'], abbreviation=team['abbreviation'], city=team['venue']['city'], arena=team['venue']['name'], division=team['division']['name'], conference=team['conference']['name'], official_site=team['officialSiteUrl'])
        db.session.add(team_obj)
    db.session.commit()

def create_player_objects():
    for player in data[1:]:
        team = db.session.query(Team).filter(Team.abbreviation == player['Team']).first()
        if bool(db.session.query(Player).filter_by(name=player['Player']).first()) == False:
            player_obj = Player(name=player['Player'], position=player['Position'][0], team=team)
            db.session.add(player_obj)
    db.session.commit()

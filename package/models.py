from __init__ import db
from sqlalchemy.sql import func


class League(db.Model):
    __tablename__ = 'leagues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    abbreviation = db.Column(db.String(5))
    country = db.Column(db.String(30))
    continent = db.Column(db.String(30))
    teams = db.relationship('Team', back_populates='league')

class TeamStats(db.Model):
    __tablename__ = 'team_stats'
    games_played = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    ties = db.Column(db.Integer)
    overtime_wins = db.Column(db.Integer)
    overtime_losses = db.Column(db.Integer)
    shootout_wins = db.Column(db.Integer)
    points = db.Column(db.Integer)
    goals_forward = db.Column(db.Integer)
    goals_against = db.Column(db.Integer)

    team_id = db.Column(db.ForeignKey('teams.id'), primary_key=True)
    team = db.relationship('Team', backref='team_stats')
    season_id = db.Column(db.ForeignKey('seasons.id'), primary_key=True)
    season = db.relationship('Season', backref='team_stats')

class PlayerStats(db.Model):
    __tablename__ = 'player_stats'
    age = db.Column(db.Integer)
    cap_hit = db.Column(db.Integer)
    height = db.Column(db.String(10))
    weight = db.Column(db.Integer)
    games_played = db.Column(db.Integer)
    time_on_ice = db.Column(db.REAL)
    goals = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    points = db.Column(db.Integer)
    primary_points = db.Column(db.Integer)
    pts_per_60 = db.Column(db.REAL)
    p_pts_per_60 = db.Column(db.REAL)
    pim = db.Column(db.Integer)
    cf = db.Column(db.Integer)
    ca = db.Column(db.Integer)
    corsi_plus_minus = db.Column(db.Integer)
    cf_percentage = db.Column(db.REAL)
    rel_cf = db.Column(db.REAL)
    gf = db.Column(db.Integer)
    ga = db.Column(db.Integer)
    plus_minus = db.Column(db.Integer)
    pdo = db.Column(db.REAL)
    zsr = db.Column(db.REAL)
    # goalie stats
    save_percentage = db.Column(db.REAL)
    goals_against_average = db.Column(db.REAL)

    player_id = db.Column(db.ForeignKey('players.id'), primary_key=True)
    player = db.relationship('Player', backref='player_stats')
    season_id = db.Column(db.ForeignKey('seasons.id'), primary_key=True)
    season = db.relationship('Season', backref='player_stats')

    team_id = db.Column(db.ForeignKey('teams.id'), primary_key=True)
    team = db.relationship('Team', back_populates='players')

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    abbreviation = db.Column(db.String(3))
    primary_color = db.Column(db.String(30))
    secondary_color = db.Column(db.String(30))
    city = db.Column(db.String(30))
    arena = db.Column(db.String(40))
    division = db.Column(db.String(20))
    conference = db.Column(db.String(20))
    official_site = db.Column(db.String(50))

    # self-reference for affiliated teams
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    affiliates = db.relationship("Team", backref=db.backref('parent_team', remote_side=[id]))

    league_id = db.Column(db.Integer, db.ForeignKey('leagues.id'))
    league = db.relationship('League', back_populates='teams')
    seasons = db.relationship('Season', secondary='team_stats')
    players = db.relationship('PlayerStats', back_populates='team')

class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(db.Integer, primary_key=True)
    start_year = db.Column(db.String(8), nullable=False)
    end_year = db.Column(db.String(8), nullable=False)

    teams = db.relationship('Team', secondary='team_stats')
    players = db.relationship('Player', secondary='player_stats')

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    alternate_first_name_1 = db.Column(db.String())
    alternate_first_name_2 = db.Column(db.String())
    alternate_first_name_3 = db.Column(db.String())
    alternate_last_name_1 = db.Column(db.String())
    alternate_last_name_2 = db.Column(db.String())
    alternate_last_name_3 = db.Column(db.String())
    date_of_birth = db.Column(db.Date)
    place_of_birth = db.Column(db.String())
    nationality = db.Column(db.String())
    second_nationality = db.Column(db.String())
    position = db.Column(db.String(1))
    shoots = db.Column(db.String())
    player_type = db.Column(db.String())
    position = db.Column(db.String())

    seasons = db.relationship('Season', secondary='player_stats')


db.create_all()


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

# players
tuch = Player(name="Alex Tuch")
db.session.add(tuch)

twenty1_twenty2_season.teams.extend(teams)

tuch_vegas_stats = PlayerStats(player=tuch, season=twenty1_twenty2_season, team=vgk)
tuch_sabre_stats = PlayerStats(player=tuch, season=twenty1_twenty2_season, team=sabres)

db.session.commit()
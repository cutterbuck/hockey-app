from __init__ import db
import datetime
from dateutil.relativedelta import relativedelta


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
    position = db.Column(db.String())
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
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    full_name = db.Column(db.String(), nullable=False)
    alt_first_name_1 = db.Column(db.String())
    alt_first_name_2 = db.Column(db.String())
    alt_first_name_3 = db.Column(db.String())
    alt_last_name_1 = db.Column(db.String())
    alt_last_name_2 = db.Column(db.String())
    alt_last_name_3 = db.Column(db.String())
    date_of_birth = db.Column(db.Date)
    place_of_birth = db.Column(db.String())
    nationality = db.Column(db.String())
    second_nationality = db.Column(db.String())
    shoots = db.Column(db.String())
    player_type = db.Column(db.String())

    seasons = db.relationship('Season', secondary='player_stats')

    def age(self):
        return relativedelta(datetime.date.today(), self.date_of_birth).years


db.create_all()
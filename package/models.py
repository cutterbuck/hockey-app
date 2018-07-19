from __init__ import db

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    abbreviation = db.Column(db.String(3))
    city = db.Column(db.String(30), nullable=False)
    arena = db.Column(db.String(40), nullable=False)
    division = db.Column(db.String(20), nullable=False)
    conference = db.Column(db.String(20), nullable=False)
    official_site = db.Column(db.String(50), nullable=False)
    players = db.relationship('Player', back_populates='team', lazy='dynamic')

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    position = db.Column(db.String(1), nullable=False)
    team = db.relationship('Team', back_populates='players')
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    seasons = db.relationship('Season', back_populates='player', lazy='dynamic')

class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(5), nullable=False)
    player = db.relationship('Player', back_populates='seasons')
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    statistic = db.relationship('Statistic', back_populates='season', uselist=False)

class Statistic(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True)
    end_yr_team = db.Column(db.String(3))
    games_played = db.Column(db.Integer)
    time_on_ice = db.Column(db.REAL)
    goals = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    points = db.Column(db.Integer)
    primary_points = db.Column(db.Integer)
    pts_per_60 = db.Column(db.REAL)
    p_pts_per_60 = db.Column(db.REAL)
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
    weighted_cf = db.Column(db.REAL)
    weighted_ca = db.Column(db.REAL)
    weighted_corsi_percentage = db.Column(db.REAL)
    season = db.relationship('Season', back_populates='statistic')
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'))

db.create_all()

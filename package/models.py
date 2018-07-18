from __init__ import db

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3), nullable=False)
    city = db.Column(db.String(20))
    arena = db.Column(db.String(30))
    players = db.relationship('Player', back_populates='team')

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    position = db.Column(db.String(1), nullable=False)
    team = db.relationship('Team', back_populates='players')
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    seasons = db.relationship('Season', back_populates='player')

class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(5), nullable=False)
    player = db.relationship('Player', back_populates='seasons')
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    statistic = db.relationship('Statistic', back_populates='season', uselist=False)

class Statistic(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True)
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
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)

db.create_all()

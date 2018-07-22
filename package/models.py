from package import db
from sqlalchemy.sql import func

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    abbreviation = db.Column(db.String(3))
    primary_color = db.Column(db.String(30))
    secondary_color = db.Column(db.String(30))
    city = db.Column(db.String(30), nullable=False)
    arena = db.Column(db.String(40), nullable=False)
    division = db.Column(db.String(20), nullable=False)
    conference = db.Column(db.String(20), nullable=False)
    official_site = db.Column(db.String(50), nullable=False)
    seasons = db.relationship('Season', back_populates='team', lazy='dynamic')
    players = db.relationship('Player', secondary='seasons', back_populates='teams', lazy='dynamic')

    def roster(self, year_input):
        return [season.player for season in self.seasons.all() if season.year == year_input]



class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(8), nullable=False)
    team = db.relationship('Team', back_populates='seasons')
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    player = db.relationship('Player', back_populates='seasons')
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    statistic = db.relationship('Statistic', back_populates='season', uselist=False)



class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer)
    position = db.Column(db.String(1), nullable=False)
    cap_hit = db.Column(db.Integer)
    seasons = db.relationship('Season', back_populates='player', lazy='dynamic')
    teams = db.relationship('Team', secondary='seasons', back_populates='players', lazy='dynamic')
    statistics = db.relationship('Statistic', secondary='seasons')
    def total_goals(self):
        total = 0
        for stat in self.statistics:
            total += stat.goals
        return total

    def total_assists(self):
        total = 0
        for stat in self.statistics:
            total += stat.assists
        return total

    def total_points(self):
        total = 0
        for stat in self.statistics:
            total += stat.points
        return total

    def total_primary_points(self):
        total = 0
        for stat in self.statistics:
            total += stat.primary_points
        return total

    def avg_games_played(self):
        total = 0
        for stat in self.statistics:
            total += stat.games_played
        return round(total/len(self.seasons.all()), 2)

    def stats_by_year(self, year_input):
        season = Season.query.filter(Season.player==self, Season.year==year_input).first()
        return season.statistic

    def team_this_year(self, year_input):
        season = Season.query.filter(Season.player==self, Season.year==year_input).first()
        return season.team


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

    # @classmethod
    # def top_10_corsi_players(cls):
    #     max = 0
    #     histo = {}
    #     for stat_line in cls.query.all():
    #         if stat_line.games_played > 30:
    #             histo[stat_line.season.player.name] = {'corsi': stat_line.cf_percentage, 'season': stat_line.season.year}
    #     return histo

db.create_all()

from package.app import db
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

class Conference(db.Model):
    __tablename__ = 'conferences'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    divisions = db.relationship('Division', back_populates='conference')

class Division(db.Model):
    __tablename__ = 'divisions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    conference_id = db.Column(db.Integer, db.ForeignKey('conferences.id'))
    conference = db.relationship('Conference', back_populates='divisions')
    team_standings = db.relationship('TeamStandings', back_populates='division')


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    common_name = db.Column(db.String(40), nullable=False)
    abbr = db.Column(db.String(5))
    logo = db.Column(db.String(75))
    primary_color = db.Column(db.String(30))
    secondary_color = db.Column(db.String(30))
    location = db.Column(db.String(30), nullable=False)
    # arena = db.Column(db.String(40))
    # division = db.Column(db.String(20))
    # conference = db.Column(db.String(20))
    official_site = db.Column(db.String(50))

    # self-reference for affiliated teams
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    farm_teams = db.relationship("Team", backref=db.backref('nhl_affiliate', remote_side=[id]))

    league_id = db.Column(db.Integer, db.ForeignKey('leagues.id'))
    league = db.relationship('League', back_populates='teams')

    seasons = db.relationship('Season', secondary='team_standings')
    players = db.relationship('Player', secondary='player_stats')


class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(7), nullable=False)

    teams = db.relationship('Team', secondary='team_standings', overlaps='seasons,players')
    players = db.relationship('Player', secondary='player_stats', overlaps='seasons,players')


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    full_name = db.Column(db.String(), nullable=False)
    alt_first_name_1 = db.Column(db.String())
    alt_first_name_2 = db.Column(db.String())
    alt_last_name_1 = db.Column(db.String())
    alt_last_name_2 = db.Column(db.String())
    date_of_birth = db.Column(db.Date)
    place_of_birth = db.Column(db.String())
    nationality = db.Column(db.String())
    second_nationality = db.Column(db.String())
    shoots = db.Column(db.String())
    player_type = db.Column(db.String())

    seasons = db.relationship('Season', secondary='player_stats', overlaps='players,seasons')
    teams = db.relationship('Team', secondary='player_stats', overlaps='players,seasons')

    def age(self):
        return relativedelta(datetime.date.today(), self.date_of_birth).years


class TeamStandings(db.Model):
    __tablename__ = 'team_standings'
    id = db.Column(db.Integer, primary_key=True)
    games_played = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    ties = db.Column(db.Integer)
    shootout_wins = db.Column(db.Integer)
    points = db.Column(db.Integer)
    points_percentage = db.Column(db.Float)
    goals_for = db.Column(db.Integer)
    goals_against = db.Column(db.Integer)
    goal_differential = db.Column(db.Integer)
    l10_wins = db.Column(db.Integer)
    regulation_wins = db.Column(db.Integer)
    regulation_plut_ot_wins = db.Column(db.Integer)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship("Team", backref=db.backref("team_standings", cascade="all, delete-orphan", overlaps="seasons,teams"), overlaps="seasons,teams")
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'))
    season = db.relationship("Season", backref=db.backref("team_standings", cascade="all, delete-orphan", overlaps="seasons,teams"), overlaps="seasons,teams")
    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'))
    division = db.relationship('Division', back_populates='team_standings')


class PlayerStats(db.Model):
    __tablename__ = 'player_stats'
    id = db.Column(db.Integer, primary_key=True)
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
    primary_pts_per_60 = db.Column(db.REAL)
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

    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    player = db.relationship("Player", backref=db.backref("player_stats", cascade="all, delete-orphan", overlaps="seasons,players,teams"), overlaps="seasons,players,teams")
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'))
    season = db.relationship("Season", backref=db.backref("player_stats", cascade="all, delete-orphan", overlaps="seasons,players"), overlaps="seasons,players,teams")

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship("Team", backref=db.backref("player_stats", cascade="all, delete-orphan", overlaps="players,teams"), overlaps="players,teams,seasons")


db.create_all()
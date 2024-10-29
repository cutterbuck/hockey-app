from dash import dcc, html, Input, Output, callback
from package.app import app
from package.models import *
import plotly.graph_objs as go
import datetime
from PIL import Image




def return_rows_background_color(color_index):
    if color_index % 2 == 1:
        return 'rgb(245,245,245)'
    elif color_index % 2 == 0:
        return 'rgb(255,255,255)'

def create_seasons_dd():
    seasons_options = [{'label': szn, 'value': szn} for szn in db.session.execute(db.select(Season.name).order_by(Season.start_date.desc())).scalars().all()]
    today = datetime.datetime.today()

    if today.month >= 10 and today.month <= 12:
        value_szn_id = int(str(today.year) + str(today.year+1))
    else:
        value_szn_id = int(str(today.year-1) + str(today.year))

    return dcc.Dropdown(
        id='seasons-dropdown',
        options=seasons_options,
        value=Season.query.get(value_szn_id).name,
        className='three columns'
    )

def goal_diff_color(value):
    if value > 0:
        return "rgb(66,124,48)"
    elif value < 0:
        return "rgb(210,55,32)"
    elif value == 0:
        return "black"


def create_standings_table(season_input):
    standings_data = db.session.query(Team.name, TeamStandings.games_played, TeamStandings.wins, TeamStandings.losses, TeamStandings.points, TeamStandings.points_percentage, TeamStandings.regulation_wins, TeamStandings.regulation_plut_ot_wins, TeamStandings.goals_for, TeamStandings.goals_against, TeamStandings.goal_differential).join(TeamStandings.team).join(TeamStandings.season).filter(Season.name == season_input).order_by(TeamStandings.points.desc()).all()
    columns = ["", "Team" , "GP", "W", "L", "PTS", "P%", "RW", "ROW", "GF", "GA", "DIFF"]
    table_rows = [html.Tr(id='header-row', children=[html.Th(children=column) for column in columns])]

    image = Image.open(url)
    image.draft('RGB', (1008, 756))
    color_index = 0
    for (team, gp, wins, losses, pts, pts_pctg, rw, row, gf, ga, diff) in standings_data:
        color_index += 1
        row_cells = [
            html.Td(html.Img(src=image, style={'width': "50px", 'height': "30px"})),
            html.Td(team),
            html.Td(gp),
            html.Td(wins),
            html.Td(losses),
            html.Td(pts),
            html.Td(pts_pctg),
            html.Td(rw),
            html.Td(row),
            html.Td(gf),
            html.Td(ga),
            html.Td(diff, style={'color': goal_diff_color(diff)})
        ]
        table_rows.append(html.Tr(id=team+'-row', children=row_cells, style={'background-color': return_rows_background_color(color_index)}))
    return html.Table(id='nhl-standings', children=table_rows)

@callback(Output('standings-output', 'children'),
    [Input('seasons-dropdown', 'value')])
def change_table(season_input):
    return create_standings_table(season_input)

app.layout = html.Div(id="hockey-app", style={'marginTop': '5%', 'marginLeft': '5%'}, children=[
    create_seasons_dd(),
    html.Div(id='standings-output'),
])


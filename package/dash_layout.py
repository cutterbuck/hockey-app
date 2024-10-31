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
        className='three columns',
        persistence=True,
        persistence_type='session',
        clearable=False
    )

def goal_diff_color(value):
    if value > 0:
        return "rgb(66,124,48)"
    elif value < 0:
        return "rgb(210,55,32)"
    elif value == 0:
        return "black"

def style_diff(value):
    return "+"+str(value) if value > 0 else str(value)

def create_standings_table(season_input, standings_type_input):
    print('standings_type_input', standings_type_input)
    standings_data = db.session.query(Team.logo, Team.name, TeamStandings.games_played, TeamStandings.wins, TeamStandings.losses, TeamStandings.points, TeamStandings.points_percentage, TeamStandings.regulation_wins, TeamStandings.regulation_plut_ot_wins, TeamStandings.goals_for, TeamStandings.goals_against, TeamStandings.goal_differential).join(TeamStandings.team).join(TeamStandings.season).filter(Season.name == season_input).order_by(TeamStandings.points.desc()).all()
    columns = ["Team", "GP", "W", "L", "PTS", "P%", "RW", "ROW", "GF", "GA", "DIFF"]
    table_rows = [html.Tr(id='header-row', children=[html.Th(children=column) for column in columns])]

    color_index = 0
    for (logo, team, gp, wins, losses, pts, pts_pctg, rw, row, gf, ga, diff) in standings_data:
        color_index += 1
        row_cells = [
            html.Td(html.Div(children=[
                    html.Img(src=logo, style={'width': "36px", 'height': "24px", 'verticalAlign': 'middle', 'paddingRight': '8px'}),
                    html.Div(team, style={'display': 'inline-block'})
                ]), style={'paddingTop': '5px', 'paddingBottom': '5px'}),
            html.Td(gp, style={'paddingTop': '5px', 'paddingBottom': '5px', 'textAlign': 'center'}),
            html.Td(wins, style={'paddingTop': '5px', 'paddingBottom': '5px', 'textAlign': 'center'}),
            html.Td(losses, style={'paddingTop': '5px', 'paddingBottom': '5px', 'textAlign': 'center'}),
            html.Td(pts, style={'paddingTop': '5px', 'paddingBottom': '5px', 'textAlign': 'center'}),
            html.Td(pts_pctg, style={'paddingTop': '5px', 'paddingBottom': '5px', 'textAlign': 'center'}),
            html.Td(rw, style={'paddingTop': '5px', 'paddingBottom': '5px', 'textAlign': 'center'}),
            html.Td(row, style={'paddingTop': '5px', 'paddingBottom': '5px', 'textAlign': 'center'}),
            html.Td(gf, style={'paddingTop': '5px', 'paddingBottom': '5px', 'textAlign': 'center'}),
            html.Td(ga, style={'paddingTop': '5px', 'paddingBottom': '5px', 'textAlign': 'center'}),
            html.Td(style_diff(diff), style={'color': goal_diff_color(diff), 'paddingTop': '5px', 'paddingBottom': '5px', 'textAlign': 'center'})
        ]
        table_rows.append(html.Tr(id=team+'-row', children=row_cells, style={'background-color': return_rows_background_color(color_index), 'height': '50px'}))
    return html.Table(id='nhl-standings', children=table_rows)

def generate_standings_type_tabs():
    return html.Div([
        dcc.Tabs(id="standings-type-tabs", persistence=True, persistence_type='session', value='division', style={'font-size':'small'}, children=[
            dcc.Tab(label='Division', value='division'),
            dcc.Tab(label='Wild Card', value='wild card'),
            dcc.Tab(label='Conference', value='conference'),
            dcc.Tab(label='League', value='league')
        ]),
    ], style={'width': '50%', 'height': '50px', 'paddingTop': '2%', 'paddingBottom': '2%'})

@callback(Output('standings-output', 'children'),
    [Input('seasons-dropdown', 'value'), Input('standings-type-tabs', 'value')])
def change_table(season_input, standings_type_input):
    return create_standings_table(season_input, standings_type_input)

app.layout = html.Div(id="hockey-app", style={'marginTop': '3%', 'marginLeft': '5%'}, children=[
    html.Div(id='seasons-dd-div', style={'display': 'grid', 'width': '75%'}, children=create_seasons_dd()),
    generate_standings_type_tabs(),
    html.Div(id='standings-output'),
])


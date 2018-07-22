import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from package import app
from package.models import db, Team, Player, Season, Statistic
import plotly.graph_objs as go


def generate_team_dropdown():
    sorted_teams = sorted(Team.query.all(), key=lambda team: team.name)
    teams = [{'label': team.name, 'value': team.name} for team in sorted_teams]
    teams.insert(0, {'label': 'Total NHL', 'value': 'Total NHL'})
    return dcc.Dropdown(
        id='team_selector',
        options=teams,
        value='Total NHL',
        className='three columns'
    )

def generate_season_dropdown():
    seasons = [{'label': season.year, 'value': season.year} for season in Player.query.all()[1].seasons.all()]
    return dcc.Dropdown(
        id='season_selector',
        options=seasons,
        value='17-18',
        className='three columns'
    )

def generate_x_axis_dropdown():
    items = dir(Statistic)
    items = [el for el in items if '__' not in el if not el.startswith('_')]
    dd_items = [{'label': item, 'value': item} for item in items if item not in ('end_yr_team', 'metadata', 'id', 'season_id', 'query', 'query_class', 'season')]
    dd_items.remove
    return dcc.Dropdown(
        id='x_axis_selector',
        options=dd_items,
        value='pdo',
        className='three columns'
    )

def generate_y_axis_dropdown():
    items = dir(Statistic)
    items = [el for el in items if '__' not in el if not el.startswith('_')]
    dd_items = [{'label': item, 'value': item} for item in items]
    return dcc.Dropdown(
        id='y_axis_selector',
        options=dd_items,
        value='weighted_corsi_percentage',
        className='three columns'
    )


def player_filter(players, year_input):
    return [player for player in players if player.stats_by_year(year_input).games_played > 30]


def get_relevant_players(team_input, year_input):
    if team_input=='Total NHL':
        players = [season.player for season in Season.query.all() if season.year == year_input]
        return player_filter(players, year_input)
    else:
        team = Team.query.filter(Team.name == team_input).first()
        players = team.roster(year_input)
        return player_filter(players, year_input)


def create_graph(players, year_input, x_axis_input, y_axis_input):
    names = [player.name for player in players]
    x = [getattr(player.stats_by_year(year_input), x_axis_input) for player in players]
    y = [getattr(player.stats_by_year(year_input), y_axis_input) for player in players]
    return dcc.Graph(
        id='life-exp-vs-gdp',
        className='container',
        figure={
            'data': [
                go.Scatter(
                    x=x,
                    y=y,
                    text=names,
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=names
                )
            ],
            'layout': go.Layout(
                xaxis={'title': x_axis_input},
                yaxis={'title': y_axis_input},
                title='NHL 5v5 Stats by Team',
                margin={'l': 40, 'b': 40, 't': 50, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )


def generate_scatter_plot(team_input, year_input, x_input, y_input):
    players = get_relevant_players(team_input, year_input)
    return create_graph(players, year_input, x_input, y_input)



@app.callback(
    Output(component_id='nhl_graph_container', component_property='children'),
    [Input(component_id='team_selector', component_property='value'), Input(component_id='season_selector', component_property='value'), Input(component_id='x_axis_selector', component_property='value'),Input(component_id='y_axis_selector', component_property='value')]
)
def change_table(team_input, season_input, x_input, y_input):
    return generate_scatter_plot(team_input, season_input, x_input, y_input)


app.layout = html.Div(children=[
        html.Div(id='dropdown_container', className='container', children=[
        html.Div([generate_team_dropdown()]),
        html.Div([generate_season_dropdown()]),
        html.Div([generate_x_axis_dropdown()]),
        html.Div([generate_y_axis_dropdown()])]),
        html.Div(id='nhl_graph_container')
])

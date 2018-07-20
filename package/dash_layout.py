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
        value='Total NHL'
    )

def generate_season_dropdown():
    seasons = [{'label': season.year, 'value': season.year} for season in Player.query.all()[1].seasons.all()]
    return dcc.Dropdown(
        id='season_selector',
        options=seasons,
        value='17-18'
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


def create_graph(players, year_input):
    names = [player.name for player in players]
    zsrs = [player.stats_by_year(year_input).zsr for player in players]
    corsis = [player.stats_by_year(year_input).weighted_corsi_percentage for player in players]
    return dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=zsrs,
                    y=corsis,
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
                xaxis={'title': 'Zone Start Percentage'},
                yaxis={'title': 'Weighted Corsi Percentage'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )


def generate_scatter_plot(team_input, year_input):
    players = get_relevant_players(team_input, year_input)
    return create_graph(players, year_input)



@app.callback(
    Output(component_id='nhl_graph_container', component_property='children'),
    [Input(component_id='team_selector', component_property='value'), Input(component_id='season_selector', component_property='value'),]
)
def change_table(team_input, season_input):
    return generate_scatter_plot(team_input, season_input)


app.layout = html.Div(children=[
        html.Div([generate_team_dropdown()]),
        html.Div([generate_season_dropdown()]),
        html.Div(id='nhl_graph_container')
])

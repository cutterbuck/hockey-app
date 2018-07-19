import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from package import app
from package.models import db, Team, Player, Season, Statistic
import plotly.graph_objs as go


def generate_team_drop_down():
    teams = [{'label': team.name, 'value': team.name} for team in Team.query.all()]
    return dcc.Dropdown(
        id='teams_selector',
        options=teams,
        value="New York Rangers"
    )

# build scatter plot using 2 drop down: 1) team 2) season
# 1) create drop down for season
# 2) tweak Team.roster() IM to take season as argument and return that seasons's roster
# 3) create Player IM that can accept season argument and return stats for that season
# 4) create functions in this file to get the right data for each for scatter plot
# 5) write callbacks

def get_team_players(team_name):
    team = Team.query.filter(Team.name == team_name).first()
    return team.roster()

def create_corsi_data(team_players):
    for player in team_players:


def generate_corsi_scatter_plot(team):
    all_players = get_team_players(team)
    corsi_data =
    data = create_corsi_data(all_players, team)
    return create_graph(data, 'Population')


# app.layout = html.Div([
#     dcc.Graph(
#         id='life-exp-vs-gdp',
#         figure={
#             'data': [
#                 go.Scatter(
#                     x=i.zsr,
#                     y=i.weighted_corsi_percentage,
#                     text=i.season,
#                     mode='markers',
#                     opacity=0.7,
#                     marker={
#                         'size': 15,
#                         'line': {'width': 0.5, 'color': 'white'}
#                     },
#                     name=i
#                 ) for i in Statistic.query.all()
#             ],
#             'layout': go.Layout(
#                 xaxis={'title': 'Zone Start Percentage'},
#                 yaxis={'title': 'Corsi Percentage'},
#                 margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#                 legend={'x': 0, 'y': 1},
#                 hovermode='closest'
#             )
#         }
#     )
# ])


app.layout = html.Div(children=[
    generate_team_drop_down()
])

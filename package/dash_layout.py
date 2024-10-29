from dash import dcc, html, Input, Output, callback, dash_table
from package.app import app
from package.models import *
import plotly.graph_objs as go


def generate_team_dropdown():
    sorted_teams = sorted(Team.query.all(), key=lambda team: team.name)
    teams = [{'label': team.name, 'value': team.name} for team in sorted_teams]
    teams.insert(0, {'label': 'Total NHL', 'value': 'Total NHL'})
    return dcc.Dropdown(
        id='team_selector',
        options=teams,
        value='New York Rangers',
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

def items_filter(items):
    for item_string in items:
        if '_' in item_string:
            index = items.index(item_string)
            split_words = item_string.split('_')
            formatted_words = []
            for word in split_words:
                if len(word) < 4:
                    word = word.upper()
                    formatted_words.append(word)
                else:
                    word = word.capitalize()
                    formatted_words.append(word)
            items[index] = ' '.join(formatted_words)
        elif len(item_string) < 5:
            index = items.index(item_string)
            items[index] = item_string.upper()
        elif len(item_string) >= 5:
            index = items.index(item_string)
            items[index] = item_string.capitalize()
    return items

def generate_x_axis_dropdown():
    items = dir(Statistic)
    items = [el for el in items if '__' not in el if not el.startswith('_')]
    filtered_items = items_filter(items)
    dd_items = [{'label': item, 'value': item} for item in filtered_items if item not in ('END YR Team', 'Metadata', 'ID', 'Season ID', 'Query', 'Query Class', 'Season')]

    return dcc.Dropdown(
        id='x_axis_selector',
        options=dd_items,
        value='PDO',
        className='three columns'
    )

def generate_y_axis_dropdown():
    items = dir(Statistic)
    items = [el for el in items if '__' not in el if not el.startswith('_')]
    filtered_items = items_filter(items)
    dd_items = [{'label': item, 'value': item} for item in filtered_items if item not in ('END YR Team', 'Metadata', 'ID', 'Season ID', 'Query', 'Query Class', 'Season')]
    return dcc.Dropdown(
        id='y_axis_selector',
        options=dd_items,
        value='Weighted Corsi Percentage',
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
    fomatted_x_input = input_converter(x_axis_input)
    formatted_y_input = input_converter(y_axis_input)

    x = [getattr(player.stats_by_year(year_input), fomatted_x_input) for player in players]
    y = [getattr(player.stats_by_year(year_input), formatted_y_input) for player in players]
    primary_color = [player.team_this_year(year_input).primary_color for player in players]
    secondary_color = [player.team_this_year(year_input).secondary_color for player in players]

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
                        'size': 17,
                        'line': {'width': 2.0, 'color': secondary_color},
                        'color': primary_color,
                        'opacity': 0.95
                    },
                )
            ],
            'layout': go.Layout(
                xaxis={'title': x_axis_input},
                yaxis={'title': y_axis_input},
                title='NHL 5v5 Stats by Team',
                margin={'l': 40, 'b': 40, 't': 50, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                plot_bgcolor='rgba(211,211,211,0.1)'
            )
        }
    )


def input_converter(input):
    input_dict = {
        'PDO': 'pdo',
        'Games Played': 'games_played',
        'Time ON ICE': 'time_on_ice',
        'Goals': 'goals',
        'Assists': 'assists',
        'Points': 'points',
        'Primary Points': 'primary_points',
        'PTS PER 60': 'pts_per_60',
        'P PTS PER 60': 'p_pts_per_60',
        'CF': 'cf',
        'CA': 'ca',
        'Corsi Plus Minus': 'corsi_plus_minus',
        'CF Percentage': 'cf_percentage',
        'GF': 'gf',
        'GA': 'ga',
        'Plus Minus': 'plus_minus',
        'PDO': 'pdo',
        'ZSR': 'zsr',
        'Weighted CF': 'weighted_cf',
        'Weighted CA': 'weighted_ca',
        'Weighted Corsi Percentage': 'weighted_corsi_percentage',
        'REL CF': 'rel_cf'
    }
    return input_dict[input]

def generate_scatter_plot(team_input, year_input, x_input, y_input):
    players = get_relevant_players(team_input, year_input)
    return create_graph(players, year_input, x_input, y_input)


@callback(
    Output('nhl_graph_container', 'children'),
    [Input('team_selector', 'value'), Input('season_selector', 'value'), Input('x_axis_selector', 'value'),Input('y_axis_selector', 'value')]
)
def change_table(team_input, season_input, x_input, y_input):
    return generate_scatter_plot(team_input, season_input, x_input, y_input)




def return_rows_background_color(color_index):
    if color_index % 2 == 1:
        return 'rgb(221,230,240)'
    elif color_index % 2 == 0:
        return 'rgb(255,255,255)'

def create_standings_table():
    standings_data = db.session.query(Team.name, TeamStandings.games_played, TeamStandings.wins, TeamStandings.losses, TeamStandings.points, TeamStandings.regulation_wins, TeamStandings.regulation_plut_ot_wins, TeamStandings.goals_for, TeamStandings.goals_against, TeamStandings.goal_differential).join(TeamStandings.team).join(TeamStandings.season).filter(Season.id == 20242025).order_by(TeamStandings.points.desc()).all()
    columns = ["Team" , "GP", "W", "L", "PTS", "RW", "ROW", "GF", "GA", "DIFF"]
    table_rows = [html.Tr(id='header-row', children=[html.Th(children=column) for column in columns])]

    color_index = 0
    for (team, gp, wins, losses, pts, rw, row, gf, ga, diff) in standings_data:
        color_index += 1
        row_cells = [
            html.Td(team),
            html.Td(gp),
            html.Td(wins),
            html.Td(losses),
            html.Td(pts),
            html.Td(rw),
            html.Td(row),
            html.Td(gf),
            html.Td(ga),
            html.Td(diff)
        ]
        table_rows.append(html.Tr(id=team+'-row', children=row_cells, style={'background-color': return_rows_background_color(color_index)}))
    return html.Table(id='nhl-standings', children=table_rows)

app.layout = html.Div(id="hockey-app", style={'marginTop': '5%', 'marginLeft': '5%'}, children=[
    create_standings_table()

    # html.Div(id='dropdown_container', className='container', children=[
    # html.Div([generate_team_dropdown()]),
    # html.Div([generate_season_dropdown()]),
    # html.Div([generate_x_axis_dropdown()]),
    # html.Div([generate_y_axis_dropdown()])]),
    # html.Div(id='nhl_graph_container')
])

print("\nHockey app is running!\n----------------------")

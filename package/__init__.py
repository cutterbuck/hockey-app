from flask_sqlalchemy import SQLAlchemy
import dash

app = dash.Dash(__name__, url_base_pathname='/dashboard/')

app.server.config['DEBUG'] = True
app.server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/hockey_stats'
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['suppress_callback_exceptions']=True

db = SQLAlchemy(app.server)

from package import dash_layout

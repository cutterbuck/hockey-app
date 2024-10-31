import dash, os
from flask_sqlalchemy import SQLAlchemy

app = dash.Dash(__name__, url_base_pathname='/', title='Hockey App Demo')
app.server.config['DEBUG'] = True

# local db
# app.server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/hockey_app_db'

app.server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('hockey_app_uri')

app.server.app_context().push()
app.config['suppress_callback_exceptions']=True
db = SQLAlchemy(app.server)

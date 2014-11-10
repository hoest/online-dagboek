import config
import flask
import flask.ext.sqlalchemy

app = flask.Flask(__name__)

# configuration
app.config.from_object(config)
app.config.from_envvar("FLASK_DIARY_SETTINGS", silent=True)

# SQLAlchemy
db = flask.ext.sqlalchemy.SQLAlchemy(app)

# application imports
import diary.api.views

# Register blueprints
app.register_blueprint(diary.api.views.mod)

# create database tables
db.create_all()

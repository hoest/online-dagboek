import diary.config
import flask
import flask.ext.restless
import flask.ext.sqlalchemy

app = flask.Flask(__name__)

# configuration
app.config.from_object(diary.config)
app.config.from_envvar("FLASK_DIARY_SETTINGS", silent=True)

# SQLAlchemy
db = flask.ext.sqlalchemy.SQLAlchemy(app)

import diary.models
import diary.views
import diary.preprocessors

# create database tables
db.create_all()

# global processors for restless-api
global_preprocessors = {
  "GET_SINGLE": [diary.preprocessors.auth_func],
  "GET_MANY": [diary.preprocessors.auth_func],
  "POST": [diary.preprocessors.auth_func],
  "DELETE": [diary.preprocessors.auth_func],
}

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app,
                                        preprocessors=global_preprocessors,
                                        flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(diary.models.Diary,
                   url_prefix="/api/v1",
                   collection_name="diaries",
                   exclude_columns=["posts"],
                   preprocessors={
                     "GET_SINGLE": [
                       diary.preprocessors.single_diary,
                     ],
                     "GET_MANY": [
                       diary.preprocessors.user_filter,
                     ],
                   },
                   methods=["GET", "POST", "PATCH", "DELETE"])

import datetime
import diary
import flask
import flask.ext.restless


@diary.app.before_request
def check_user_status():
  """
  Check global user_id
  """
  flask.g.user = None
  if "user_id" in flask.session:
    flask.g.user = diary.models.User.query.filter_by(id=flask.session["user_id"]).first()


@diary.app.route("/login", methods=["GET"])
def login():
  return flask.render_template("login.html")


@diary.app.route("/api/v1/loggedin", methods=["GET"])
def loggedin():
  result = {
    "success": flask.g.user is not None
  }

  return flask.jsonify(result)


@diary.app.route("/api/v1/check_token", methods=["POST"])
def check_token():
  token_obj = flask.request.get_json()

  token = None
  if token_obj is not None:
    token = token_obj["token"]
  flask.g.user = diary.models.User.verify_auth_token(token)
  flask.session["user_id"] = flask.g.user.id

  result = {
    "success": flask.g.user.id is not None
  }

  return flask.jsonify(result)


@diary.app.route("/api/v1/get_token", methods=["POST"])
def get_token():
  token = {}
  facebook_obj = flask.request.get_json()

  if facebook_obj is not None:
    if "facebookResponse" not in facebook_obj or "authResponse" not in facebook_obj:
      return flask.jsonify(token)

    user = diary.models.User.query.filter_by(emailaddress=facebook_obj["facebookResponse"]["email"]).first()
    if user is None:
      # new user
      user = diary.models.User()
      user.emailaddress = facebook_obj["facebookResponse"]["email"]
    user.firstname = facebook_obj["facebookResponse"]["first_name"]
    user.lastname = facebook_obj["facebookResponse"]["last_name"]
    user.facebook_id = facebook_obj["facebookResponse"]["id"]
    diary.db.session.add(user)

    auth = diary.models.Auth.query.filter_by(token=facebook_obj["authResponse"]["accessToken"]).first()
    if auth is None:
      auth = diary.models.Auth()
      auth.owner_id = user.id
    auth.facebook_token = facebook_obj["authResponse"]["accessToken"]
    auth.token = user.generate_auth_token()
    auth.modified = datetime.datetime.utcnow()
    diary.db.session.add(auth)
    diary.db.session.commit()

    token["token"] = auth.token

  return flask.jsonify(token)

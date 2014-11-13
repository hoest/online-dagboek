import datetime
import diary
import diary.api.models
import flask
import functools
import requests

# Blueprint
mod = flask.Blueprint("api", __name__, url_prefix="/api/v1")


@mod.route("/token", methods=["POST"])
def get_token():
  """
  Gets a API token
  """
  token = {}
  facebook_obj = flask.request.get_json()

  if facebook_obj is not None:
    if "facebook" not in facebook_obj or "auth" not in facebook_obj:
      return flask.jsonify(token)

    facebook_token = facebook_obj["auth"]["accessToken"]
    facebook_id = facebook_obj["facebook"]["id"]
    if facebook_token is None:
      return flask.jsonify(token)

    if not validate_fbtoken(facebook_id, facebook_token):
      return flask.jsonify(token)

    fb_email = facebook_obj["facebook"]["email"]
    user = diary.api.models.User.query.filter_by(emailaddress=fb_email).first()

    if user is None:
      # new user
      user = diary.api.models.User()
    user.emailaddress = fb_email
    user.firstname = facebook_obj["facebook"]["first_name"]
    user.lastname = facebook_obj["facebook"]["last_name"]
    if user.facebook_id is None:
      user.facebook_id = facebook_id

    # add and commit user
    diary.db.session.add(user)
    diary.db.session.commit()

    auth = diary.api.models.Auth()
    auth.owner_id = user.id
    auth.facebook_token = facebook_token
    auth.token = user.generate_auth_token()
    auth.modified = datetime.datetime.utcnow()

    # add and commit auth_token
    diary.db.session.add(auth)
    diary.db.session.commit()

    token["token"] = auth.token

  return flask.jsonify(token)


def validate_fbtoken(id, token):
  """
  Validate Facebook access-token
  """
  payload = {
    "access_token": token
  }

  r = requests.get("https://graph.facebook.com/me", verify=True, params=payload)
  fb_json = r.json()
  return "id" in fb_json and fb_json["id"] == id


def authorized(fn):
  """
  Decorator to check the given token and create the current user
  """
  @functools.wraps(fn)
  def decorated_function(*args, **kwargs):
    # Unauthorized response
    unauth_resp = flask.jsonify({"message": "Unauthorized"})
    unauth_resp.status_code = 401

    if flask.request.authorization is None:
      # Unauthorized
      return unauth_resp

    if "password" not in flask.request.authorization:
      # Unauthorized
      return unauth_resp

    auth_token = flask.request.authorization["password"]
    user = diary.api.models.User.verify_auth_token(auth_token)
    if user is None:
      # Unauthorized
      return unauth_resp

    return fn(user=user, *args, **kwargs)
  return decorated_function


@mod.route("/diaries", methods=["GET"])
@authorized
def get_diaries(user):
  """
  Return all diaries for a specific user
  """
  result = []
  for d in user.diaries:
    result.append(d.to_dict())

  return flask.jsonify({"diaries": result})


@mod.route("/diaries", methods=["POST"])
@mod.route("/diaries/<int:diary_id>", methods=["PUT"])
@authorized
def create_diary(user, diary_id=None):
  """
  Create a diary
  """
  json_obj = flask.request.get_json()

  # JSON not complete/valid
  if "title" not in json_obj:
    return flask.jsonify({"message": "Title is required"})

  d = None
  if diary_id is None:
    d = diary.api.models.Diary()
  else:
    d = diary.api.models.Diary.query.get(diary_id)

  d.title = json_obj["title"]
  d.owner_id = user.id
  d.users.append(user)

  diary.db.session.add(d)
  diary.db.session.commit()

  return flask.jsonify(d.to_dict())


@mod.route("/diaries/<int:diary_id>/posts", methods=["GET"])
@mod.route("/diaries/<int:diary_id>/posts/<int:page>", methods=["GET"])
@authorized
def get_posts(user, diary_id, page=0):
  """
  Return all posts per diary for a specific user; sorted by date (DESC)
  """
  my_diary = user.diaries.filter_by(id=diary_id).first()

  if my_diary is None:
    # Unauthorized response
    unauth_resp = flask.jsonify({"message": "Unauthorized"})
    unauth_resp.status_code = 401
    return unauth_resp

  result = []
  for p in my_diary.sorted_posts(10, page):
    result.append(p.to_dict())

  return flask.jsonify({"posts": result})


@mod.route("/diaries/<int:diary_id>/posts", methods=["POST"])
@mod.route("/diaries/<int:diary_id>/posts/<int:post_id>", methods=["PUT"])
@authorized
def create_post(user, diary_id=None, post_id=None):
  """
  Create a post
  """
  my_diary = user.diaries.filter_by(id=diary_id).first()

  if my_diary is None:
    # Unauthorized response
    unauth_resp = flask.jsonify({"message": "Unauthorized"})
    unauth_resp.status_code = 401
    return unauth_resp

  json_obj = flask.request.get_json()

  # JSON not complete/valid
  if "title" not in json_obj or "body" not in json_obj or "date" not in json_obj:
    return flask.jsonify({"message": "Title, body and date are required"})

  p = None
  if post_id is None:
    p = diary.api.models.Post()
  else:
    p = diary.api.models.Post.query.get(post_id)
    p.modified = datetime.datetime.now()

  p.title = json_obj["title"]
  p.body = json_obj["body"]
  p.date = json_obj["date"]
  p.user_id = user.id
  p.diary_id = diary_id

  diary.db.session.add(p)
  diary.db.session.commit()

  return flask.jsonify(p.to_dict())

import datetime
import diary
import diary.api.models
import flask
import functools

# Blueprint
mod = flask.Blueprint("api", __name__, url_prefix="/api/v1")



@mod.route("/get_token", methods=["POST"])
def get_token():
  token = {}
  facebook_obj = flask.request.get_json()

  if facebook_obj is not None:
    if "facebook" not in facebook_obj or "auth" not in facebook_obj:
      return flask.jsonify(token)

    facebook_token = facebook_obj["auth"]["accessToken"]
    if facebook_token is None:
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
      user.facebook_id = facebook_obj["facebook"]["id"]
    diary.db.session.add(user)

    auth = diary.api.models.Auth()
    auth.owner_id = user.id
    auth.facebook_token = facebook_token
    auth.token = user.generate_auth_token()
    auth.modified = datetime.datetime.utcnow()
    diary.db.session.add(auth)

    diary.db.session.commit()

    token["token"] = auth.token

  return flask.jsonify(token)


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
  for item in user.diaries:
    result.append({
      "id": item.id,
      "owner_id": item.owner_id,
      "title": item.title,
      "slug": item.slug,
      "created": item.created,
    })

  return flask.jsonify({"diaries": result})


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
  for item in my_diary.sorted_posts(10, page):
    pics = []
    for pic in item.pictures.all():
      pics.append({
        "id": pic.id,
        "title": pic.title,
        "file_url": pic.file_url,
        "thumb_url": pic.thumb_url,
      })

    result.append({
      "id": item.id,
      "user_id": item.user_id,
      "diary_id": item.diary_id,
      "title": item.title,
      "body": item.body,
      "date": item.date.isoformat(),
      "created": item.created.isoformat(),
      "modified": item.modified.isoformat(),
      "pictures": pics,
    })

  return flask.jsonify({"posts": result})
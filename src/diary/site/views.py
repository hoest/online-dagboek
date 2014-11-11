import flask

# Blueprint
mod = flask.Blueprint("site", __name__, url_prefix="/", template_folder="templates")


@mod.route("/", methods=["GET"])
def index():
  return flask.render_template("login.html")

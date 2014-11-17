import flask

# Blueprint
mod = flask.Blueprint("site", __name__, url_prefix="/site",
                      template_folder="templates", static_folder="static")


@mod.route("/", methods=["GET"])
def index():
  return flask.render_template("index.html")

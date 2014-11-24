import flask

# Blueprint
mod = flask.Blueprint("site", __name__, url_prefix="/site",
                      template_folder="templates", static_folder="static")


@mod.route("/", methods=["GET"])
def index():
  return flask.render_template("index.html")


@mod.route("/<path:path>", methods=["GET"])
def redirect_to_index(path):
  redirect = "{0}#!/{1}".format(flask.url_for("site.index"), path)
  return flask.redirect(redirect)

import diary
import flask
import flask.ext.restless


def check_global_user():
  if flask.g.user is None:
    raise flask.ext.restless.ProcessingException(description="Not authenticated!", code=401)


# Preprocessor functions
def auth_func(*args, **kw):
  check_global_user()


def single_diary(instance_id=None, **kw):
  """
  Accepts a single argument, `instance_id`, the primary key of the
  instance of the model to get.
  """
  check_global_user()
  if not flask.g.user.has_access(instance_id):
    flask.g.user = None
    flask.session.pop("user_id", None)
    raise flask.ext.restless.ProcessingException(description="Not authenticated!", code=401)


def user_filter(search_params=None, **kw):
  """
  Accepts a single argument, `search_params`, which is a dictionary
  containing the search parameters for the request.
  """
  check_global_user()
  filt = dict(name="users",
              op="any",
              val=dict(name="id",
                       op="eq",
                       val=flask.g.user.id))

  # Check if there are any filters there already.
  if "filters" not in search_params:
    search_params["filters"] = []

  # *Append* your filter to the list of filters.
  search_params["filters"].append(filt)


def sort_by_date(search_params=None, **kw):
  order = dict(field="post__date", direction="desc")

  if search_params is None:
    search_params = {}

  # Check if there are any order_by there already.
  if "order_by" not in search_params:
    search_params["order_by"] = []

  # *Append* your filter to the list of order_by.
  search_params["order_by"].append(order)

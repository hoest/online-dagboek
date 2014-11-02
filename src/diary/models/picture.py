from diary import db, utils


class Picture(db.Model):
  """
  The Picture object
  """
  __tablename__ = "picture"

  id = db.Column(db.Integer, primary_key=True)
  post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
  title = db.Column(db.String(1024), nullable=False, index=True)
  file_url = db.Column(db.String(1024), nullable=False)
  thumb_url = db.Column(db.String(1024), nullable=True)
  slug = db.Column(db.String(256), nullable=False)

  def __init__(self, title):
    self.title = title
    self.slug = utils.slugify(title)

  def __repr__(self):
    return u"<Picture %s>" % (self.title)

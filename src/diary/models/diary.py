from datetime import datetime
from diary import db, utils
from diary.models import Post


class Diary(db.Model):
  """
  The Diary object
  """
  __tablename__ = "diary"

  id = db.Column(db.Integer, primary_key=True)
  owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  title = db.Column(db.String(1024), nullable=False, index=True)
  slug = db.Column(db.String(256), nullable=False, unique=True)
  created = db.Column(db.DateTime, default=datetime.utcnow)

  # relations
  posts = db.relationship("Post", lazy="dynamic")

  def __init__(self, title):
    self.title = title
    self.create_slug()

  def create_slug(self):
    self.slug = utils.slugify(self.title)

    counter = 0
    new = self.slug
    while self.query.filter(Diary.slug == new).first() is not None:
      counter += 1
      new = "{0}-{1}".format(self.slug, counter)
    self.slug = new

  def get_post(self, slug):
    return self.posts.filter(Post.slug == slug)

  def sorted_posts(self):
    return self.posts.order_by(Post.date.desc())

  def last_post(self):
    return self.posts.order_by(Post.created.desc()).first()

  def __repr__(self):
    return u"<Diary %d : %s>" % (self.id, self.title)

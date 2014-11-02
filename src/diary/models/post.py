from datetime import datetime
from diary import db, utils


class Post(db.Model):
  """
  The Post object
  """
  __tablename__ = "post"

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  diary_id = db.Column(db.Integer, db.ForeignKey("diary.id"))
  title = db.Column(db.String(1024), nullable=False, index=True)
  body = db.Column(db.Text, nullable=False)
  date = db.Column(db.Date, default=datetime.utcnow)
  slug = db.Column(db.String(256), nullable=False)
  created = db.Column(db.DateTime, default=datetime.utcnow)
  modified = db.Column(db.DateTime, default=datetime.utcnow)

  # relations
  pictures = db.relationship("Picture", lazy="dynamic")

  def __init__(self, diary_id, title):
    self.diary_id = diary_id
    self.title = title
    self.create_slug(diary_id)

  def create_slug(self, diary_id):
    self.slug = utils.slugify(self.title)

    counter = 0
    new = self.slug
    while self.query.filter(Post.slug == new, Post.diary_id == diary_id).first() is not None:
      counter += 1
      new = "{0}-{1}".format(self.slug, counter)
    self.slug = new

  def __repr__(self):
    return u"<Post: %s> %s" % (self.id, self.title)

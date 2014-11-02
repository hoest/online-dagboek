from datetime import datetime
from diary import db, bcrypt
from diary.model import Diary, Post
from flask.ext.login import UserMixin

ROLE_USER = 0
ROLE_ADMIN = 1

dairy_user_table = db.Table(
  "dairy_user",
  db.Model.metadata,
  db.Column("diary_id", db.Integer, db.ForeignKey("diary.id")),
  db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)


class User(db.Model, UserMixin):
  """
  The User object
  """
  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(256), nullable=False)
  lastname = db.Column(db.String(256), nullable=False, index=True)
  emailaddress = db.Column(db.String(1024), nullable=False, index=True, unique=True)
  password = db.Column(db.String(1024), nullable=True)
  role = db.Column(db.SmallInteger, default=ROLE_USER)
  active = db.Column(db.Boolean, default=True)
  created = db.Column(db.DateTime, default=datetime.utcnow)

  # relations
  diaries = db.relationship("Diary", secondary=dairy_user_table, lazy="dynamic", backref="users")
  posts = db.relationship("Post", lazy="dynamic")

  def __init__(self, firstname, lastname, emailaddress, password=None):
    self.firstname = firstname
    self.lastname = lastname
    self.emailaddress = emailaddress
    if password is not None:
      self.password = bcrypt.generate_password_hash(password)

  def is_password_correct(self, password):
    return bcrypt.check_password_hash(self.password, password)

  def has_access(self, diary_id):
    return len(self.diaries.filter(Diary.id == diary_id).all()) is 1

  def get_diary(self, slug):
    if self.role == ROLE_USER:
      return self.diaries.filter(Diary.slug == slug)
    else:
      return Diary.query.filter(Diary.slug == slug)

  def sorted_diaries(self):
    return self.diaries.order_by(Diary.title)

  def last_post(self):
    return self.posts.order_by(Post.created.desc()).first()

  def __repr__(self):
    return u"<User %d : %s>" % (self.id, self.emailaddress)

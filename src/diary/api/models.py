import diary
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

ROLE_USER = 0
ROLE_ADMIN = 1

"""
User-diary many-to-many relationship
"""
dairy_user_table = diary.db.Table(
  "dairy_user",
  diary.db.Model.metadata,
  diary.db.Column("diary_id",
                  diary.db.Integer,
                  diary.db.ForeignKey("diary.id")),
  diary.db.Column("user_id",
                  diary.db.Integer,
                  diary.db.ForeignKey("user.id")))


class User(diary.db.Model):
  """
  The User object
  """
  __tablename__ = "user"

  id = diary.db.Column(diary.db.Integer, primary_key=True)
  firstname = diary.db.Column(diary.db.Unicode(256), nullable=False)
  lastname = diary.db.Column(diary.db.Unicode(256), nullable=False, index=True)
  emailaddress = diary.db.Column(diary.db.Unicode(1024), nullable=False, index=True, unique=True)
  facebook_id = diary.db.Column(diary.db.Unicode, nullable=True)
  role = diary.db.Column(diary.db.SmallInteger, default=ROLE_USER)
  active = diary.db.Column(diary.db.Boolean, default=True)
  created = diary.db.Column(diary.db.DateTime, default=datetime.datetime.utcnow)

  # relations
  diaries = diary.db.relationship("Diary",
                                  secondary=dairy_user_table,
                                  lazy="dynamic",
                                  backref="users")
  tokens = diary.db.relationship("Auth", lazy="dynamic")
  posts = diary.db.relationship("Post", lazy="dynamic")

  def has_access(self, diary_id):
    return len(self.diaries.filter(Diary.id == diary_id).all()) is 1

  def generate_auth_token(self, expiration=600):
    s = Serializer(diary.app.config["SECRET_KEY"], expires_in=expiration)
    user_data = {
      "user_id": self.id,
      "user_email": self.emailaddress,
    }

    return unicode(s.dumps(user_data), "utf-8")

  @staticmethod
  def verify_auth_token(token):
    s = Serializer(diary.app.config["SECRET_KEY"])

    try:
      data = s.loads(token)
    except SignatureExpired:
      return None  # valid token, but expired
    except BadSignature:
      return None  # invalid token
    user = User.query.get(data["user_id"])
    return user


class Auth(diary.db.Model):
  """
  Auth tokens
  """
  __tablename__ = "auth_token"

  id = diary.db.Column(diary.db.Integer, primary_key=True)
  owner_id = diary.db.Column(diary.db.Integer, diary.db.ForeignKey("user.id"))
  facebook_token = diary.db.Column(diary.db.Unicode, nullable=False)
  token = diary.db.Column(diary.db.Unicode, nullable=False)
  modified = diary.db.Column(diary.db.DateTime, default=datetime.datetime.utcnow)


class Diary(diary.db.Model):
  """
  The Diary object
  """
  __tablename__ = "diary"

  id = diary.db.Column(diary.db.Integer, primary_key=True)
  owner_id = diary.db.Column(diary.db.Integer, diary.db.ForeignKey("user.id"))
  title = diary.db.Column(diary.db.Unicode(1024), nullable=False, index=True)
  slug = diary.db.Column(diary.db.Unicode(256), nullable=False, unique=True)
  created = diary.db.Column(diary.db.DateTime, default=datetime.datetime.utcnow)

  # relations
  posts = diary.db.relationship("Post", lazy="dynamic")

  def sorted_posts(self, limit, offset):
    return self.posts.order_by(Post.date.desc(), Post.id).limit(limit).offset(offset).all()


class Post(diary.db.Model):
  """
  The Post object
  """
  __tablename__ = "post"

  id = diary.db.Column(diary.db.Integer, primary_key=True)
  user_id = diary.db.Column(diary.db.Integer, diary.db.ForeignKey("user.id"))
  diary_id = diary.db.Column(diary.db.Integer, diary.db.ForeignKey("diary.id"))
  title = diary.db.Column(diary.db.Unicode(1024), nullable=False, index=True)
  body = diary.db.Column(diary.db.Text, nullable=False)
  date = diary.db.Column(diary.db.Date, default=datetime.datetime.utcnow)
  created = diary.db.Column(diary.db.DateTime, default=datetime.datetime.utcnow)
  modified = diary.db.Column(diary.db.DateTime, default=datetime.datetime.utcnow)

  # relations
  pictures = diary.db.relationship("Picture", lazy="dynamic")


class Picture(diary.db.Model):
  """
  The Picture object
  """
  __tablename__ = "picture"

  id = diary.db.Column(diary.db.Integer, primary_key=True)
  post_id = diary.db.Column(diary.db.Integer, diary.db.ForeignKey("post.id"))
  title = diary.db.Column(diary.db.Unicode(1024), nullable=False, index=True)
  file_url = diary.db.Column(diary.db.Unicode(1024), nullable=False)
  thumb_url = diary.db.Column(diary.db.Unicode(1024), nullable=True)

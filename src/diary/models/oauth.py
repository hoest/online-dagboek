from diary import db

OAUTH_TWITTER = 1
OAUTH_FACEBOOK = 2
OAUTH_GOOGLE = 3


class OAuth(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  oauth_token = db.Column(db.String(1024), nullable=False)
  oauth_token_secret = db.Column(db.String(1024), nullable=True)
  oauth_type = db.Column(db.SmallInteger, default=OAUTH_FACEBOOK)

  def __init__(self, user_id, oauth_token, oauth_token_secret=None, oauth_type=OAUTH_FACEBOOK):
    self.user_id = user_id
    self.oauth_token = oauth_token
    self.oauth_token_secret = oauth_token_secret
    self.oauth_type = oauth_type

  def __repr__(self):
    return u"<OAuth %s : %s : %s>" % (self.user_id, self.oauth_type, self.oauth_token)

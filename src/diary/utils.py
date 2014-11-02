import re

_punct_re = re.compile(r"[\t !\"#$%&'()*\-/<=>?@\[\\\]^_`{|},.]+")
internal = ["pages", "favicon.ico", "create", "delete", "login", "logout", "facebook", "diary"]


def slugify(text, delim=u"-"):
  """
  Generates an ASCII-only slug.
  """
  result = []
  for word in _punct_re.split(text.lower()):
    word = word.encode("translit/long")
    if word:
      result.append(word)
  my_slug = (delim.join(result)).decode("utf-8")[:64]
  if any(my_slug in s for s in internal):
    return "diary-%s" % my_slug
  else:
    return my_slug

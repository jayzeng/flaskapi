from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import inspect

class SerializableModel(object):

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def serialize(self, included_fields=None, excluded_fields=None):
        """
        Serializes all fields in a model that being with a character. Optionally,
        a list of field names can be passed in to only serialize those fields

        included_fields and excluded_fields are *not* passed in at the same time

        :param included_fields: explicitly specify which fields to serialize
        :param excluded_fields: explicitly exclude fields to serialize
        :return: a serialized representation of this model
        """
        class_fields = set(self.__class__.__dict__.keys())

        if excluded_fields:
            class_fields = set.difference(class_fields, excluded_fields)
        elif included_fields:
            class_fields = included_fields

        # only keep class variables that is alpha
        return {field: getattr(self, field) for field in class_fields if field[0].isalpha() \
                and not inspect.ismethod(getattr(self, field)) }

    def fromdict(self, **kwargs):
        for column in self.__table__.columns:
            col_name = column.name

            if col_name in kwargs and kwargs[col_name]:
                setattr(self, col_name, kwargs[col_name])

    def clone(self, other):
        for column in self.__table__.columns:
            col_name = column.name
            setattr(self, col_name, getattr(other, col_name))

class Developer(SerializableModel, db.Model):
    __tablename__ = 'developer'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),
                      nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    bio = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(SerializableModel, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or \
               hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


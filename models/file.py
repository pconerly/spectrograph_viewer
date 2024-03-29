from flaskapp import db


class SirensFile(db.Model):
    __tablename__ = 'sirens_file'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), index=True, unique=True)
    value = db.Column(db.String(256), unique=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<SirensFile %s/%s/>' % (self.key, self.value)

    def toDict(self):
        return {'id': self.id, 'key': self.key, 'value': self.value}

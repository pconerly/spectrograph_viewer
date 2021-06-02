import json

import numpy as np
from attrdict import AttrDict
import datetime

from sqlalchemy import create_engine

from sqlalchemy import create_engine
from sqlalchemy import (Table, Boolean, Column, Integer, String, Text,
                        MetaData, ForeignKey, LargeBinary, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from os import path
from utils import getRightDirs

resource_dir, data_path = getRightDirs()
databasefile = path.abspath(path.join(data_path, 'sv.db'))
print('databasefile', databasefile)
engine = create_engine('sqlite:///%s' % databasefile, echo=True)

print("engine", engine)

DecBase = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))


class Derp(DecBase):
    __tablename__ = 'derp'

    id = Column(Integer, primary_key=True)
    key = Column(String(80), index=True, unique=True)
    value = Column(String(256), unique=False)

    def __repr__(self):
        return '<Derp %s: %s/%s/>' % (self.id, self.key, self.value)

    def __init__(self, key, value):
        self.key = key
        self.value = value


StatusEnum = AttrDict({
    'pending': 'pending',
    'error': 'error',
    'done': 'done',
})


class SirensFile(DecBase):
    __tablename__ = 'sirensfile'

    id = Column(Integer, primary_key=True)
    filepath = Column(String(512), index=True)

    status = Column(String(20))
    last_updated = Column(
        DateTime,
        onupdate=datetime.datetime.now,
        default=datetime.datetime.now)
    spectograph = Column(LargeBinary)
    data = Column(LargeBinary)

    def __repr__(self):
        return '<SirensFile %s: %s />' % (self.id, self.filepath)

    def __init__(self, filepath):
        self.filepath = filepath
        self.status = 'pending'

    def getData(self):
        return json.loads(self.data)

    def getSpectograph(self):
        return np.frombuffer(self.spectograph, dtype=np.dtype('f8'))


def create_tables():
    # this call is idempotent
    DecBase.metadata.create_all()


session = Session()

if __name__ == '__main__':
    # session = Session()
    # d = Derp('what', 'FOOBAR')
    # # d.save()
    # print(d)
    # session.add(d)
    # session.commit()

    derps = session.query(Derp).all()
    print(derps)

    session.close()

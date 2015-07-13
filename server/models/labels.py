from sqlalchemy import create_engine, Column, Integer, Sequence, String, DateTime
from server import Base

class Labels(Base):
    __tablename__ = 'labels'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    driverGroup = Column(Integer)
    idLabel = Column(Integer)

    def __repr__(self):
        return "<Labels: '%s' (driverGroup:'%s', idLabel:'%s')>" % (self.id, self.driverGroup, self.idLabel)
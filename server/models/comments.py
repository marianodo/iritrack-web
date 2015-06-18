from sqlalchemy import create_engine, Column, Integer, Sequence, String
from server import Base

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    driver_group = Column(Integer)
    comment = Column(String(300))

    def __repr__(self):
        return "<Comment: '%s' (driver_group:'%s', comment:'%s')>" % (self.id, self.driver_group, self.comment)
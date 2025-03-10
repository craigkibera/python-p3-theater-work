from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)
    auditions = relationship('Audition', backref=backref('role', uselist=False))

    @property
    def actors(self):
        return [audition.actor for audition in self.auditions]
    
    @property
    def location(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hiredAuditions = [audition for audition in self.auditions if audition.hired]
        if hiredAuditions:
            return hiredAuditions[0]
        return 'no actor has been hired for this role'

    def understudy(self):
        hiredAuditions = [audition for audition in self.auditions if audition.hired]
        if len(hiredAuditions) > 1:
            return hiredAuditions[1]
        return 'no actor has been hired for understudy for this role'

    
class Audition(Base):
    __tablename__ =  'auditions'
    id = Column(Integer,primary_key=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    hired = Column(Boolean, nullable=False, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    role = relationship('Role', backref=backref('auditions', cascade='all, delete-orphan'))

    def callback(self):
        self.hired = True




    

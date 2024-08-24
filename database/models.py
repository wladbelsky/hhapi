from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata

class BaseModel(Base):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Vacancy(BaseModel):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    specialty = Column(String(255), nullable=False)
    min_salary = Column(Integer, nullable=True)
    max_salary = Column(Integer, nullable=True)

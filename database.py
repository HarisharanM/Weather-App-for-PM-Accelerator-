from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///weather_data.db")
Base = declarative_base()

class WeatherEntry(Base):
    __tablename__ = 'weather_entries'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    date = Column(String)
    temperature = Column(Float)
    condition = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()



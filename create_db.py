from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://root:111111@localhost/data_base_avito", echo=True)
Base = declarative_base()


class AvitoTechnic(Base):
    __tablename__ = 'sh_technic_new'

    id = Column(Integer, primary_key=True)
    hex_id = Column(String(40), unique=True)
    reference_ad = Column(String(250), nullable=False)
    title_text = Column(String(250), nullable=False)
    type_technic = Column(String(30), nullable=True)
    price = Column(Float, nullable=True)
    offer_datetime = Column(DateTime, nullable=False)
    address = Column(String(250), nullable=True)
    area = Column(String(30), nullable=False)
    model_request = Column(String(30), nullable=True)
    model_research = Column(String(30), nullable=True)
    model_exact = Column(String(30), nullable=True)
    year = Column(Integer, nullable=True)
    condition = Column(String(30), nullable=True)
    maker = Column(String(30), nullable=True)
    maker_request = Column(String(30), nullable=True)
    moto_hours = Column(Integer, nullable=True)
    document = Column(String(30), nullable=True)


Base.metadata.create_all(engine)


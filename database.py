# database.py
from sqlalchemy import create_engine, Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///inventory.db", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    location = Column(String)
    status = Column(String)
    item = Column(String)
    computer_name = Column(String)
    ip_address = Column(String)
    mac_address = Column(String)
    make = Column(String)
    model = Column(String)
    screen_size = Column(String)
    man_serial_no = Column(String)
    g_serial_number = Column(String)
    operating_system = Column(String)
    os_version = Column(String)
    os_build = Column(String)
    system_type = Column(String)
    storage_size = Column(String)
    memory_size = Column(String)
    processor_speed = Column(String)
    office_suite = Column(String)
    comments = Column(Text)
    recommendations = Column(Text)
    date_of_purchase = Column(String)
    cost = Column(String)
    supplier = Column(String)
    gpo_no = Column(String)
    warranty_period = Column(String)
    quantity = Column(Integer)
    storage_type = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)

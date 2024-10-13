from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DSN = 'postgresql+asyncpg://postgres:postgres@localhost:5432/ads'

engine = create_async_engine(DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class Ads(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    header = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)
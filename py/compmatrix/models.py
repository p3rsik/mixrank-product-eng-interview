from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class App(Base):
    __tablename__ = "app"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    company_url = Column(Text)
    release_date = Column(Date)
    genre_id = Column(Integer)
    artwork_large_url = Column(Text)
    seller_name = Column(Text)

    five_star_ratings = Column(Integer)
    four_star_ratings = Column(Integer)
    three_star_ratings = Column(Integer)
    two_star_ratings = Column(Integer)
    one_star_ratings = Column(Integer)

    sdks = relationship("AppSDK", back_populates="app")


class SDK(Base):
    __tablename__ = "sdk"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    slug = Column(Text)
    url = Column(Text)
    description = Column(Text)

    apps = relationship("AppSDK", back_populates="sdk")


class AppSDK(Base):
    __tablename__ = "app_sdk"

    app_id = Column(Integer, ForeignKey("app.id"), primary_key=True)
    sdk_id = Column(Integer, ForeignKey("sdk.id"), primary_key=True)
    installed = Column(Boolean)

    app = relationship("App", back_populates="sdks")
    sdk = relationship("SDK", back_populates="apps")

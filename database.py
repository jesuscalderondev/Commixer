from sqlalchemy import Integer, Double, Text, Uuid, Boolean, VARCHAR, TIMESTAMP
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine
from uuid import uuid4
from datetime import datetime

database = f'sqlite:///database.db'
engine = create_engine(database)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Users(Base):
    __tablename__ = 'Users'

    Id = Column(Uuid, primary_key=True, nullable=False, default=uuid4)
    FullName = Column(VARCHAR(500), nullable=False)
    Direction = Column(VARCHAR(500), nullable=False)
    Email = Column(VARCHAR(225), nullable=False, unique=True)
    Password = Column(VARCHAR(225), nullable=False)
    Birthdate = Column(TIMESTAMP)
    Active = Column(Boolean, nullable=False, default=0)
    Token = Column(VARCHAR(500))

class Products(Base):

    __tablename__ = 'Products'

    Id = Column(Uuid, primary_key=True, nullable=False, default=uuid4)
    Name = Column(VARCHAR(500), nullable=False)
    Description = Column(Text)
    Stock = Column(Integer, nullable=False)
    Quantity = Column(Integer, nullable=False)
    Size = Column(VARCHAR(500))
    Weight = Column(Double)
    Color = Column(VARCHAR(500))
    Cover = Column(Text)
    Price = Column(Double, nullable=False)
    Status = Column(VARCHAR(500), nullable=False)
    Available = Column(Boolean, nullable=False)
    Display = Column(Boolean, nullable=False)
    VariantOf = Column(Integer)
    CreateAt = Column(TIMESTAMP, nullable=False)
    UpdateAt = Column(TIMESTAMP)

    PrecingHistory = relationship('PrecingHistory', backref='Product', cascade='delete, delete-orphan')
    Discount = relationship('Discount', uselist=False, cascade='delete, delete-orphan')
    Sources = relationship('ProductMedia', backref='Products', cascade='delete, delete-orphan')

    def __init__(self, name, description, stock, quantity, size, weight, color, cover, price):
        self.Name = name
        self.Description = description
        self.Stock = stock
        self.Quantity = quantity
        self.Size = size
        self.Weight = weight
        self.Color = color
        self.Cover = cover
        self.Price = price
        self.CreateAt = datetime.now()
        self.Display = True
        self.Available = True
        self.Status = 'Disponible'


class Discount(Base):

    __tablename__ = 'Discounts'

    Id = Column(Uuid, primary_key=True, nullable=False, default=uuid4)
    ProductId = Column(Uuid, ForeignKey('Products.Id'), nullable=False)
    Percent = Column(Double, nullable=False)
    Units = Column(Integer, nullable=False)
    ActiveFrom = Column(TIMESTAMP, nullable=False)
    ActiveTo = Column(TIMESTAMP)
    CreateAt = Column(TIMESTAMP, nullable=False)
    UpdateAt = Column(TIMESTAMP)

class PrecingHistory(Base):

    __tablename__ = 'PrecingHistory'

    Id = Column(Uuid, primary_key=True, nullable=False, default=uuid4)
    ProductId = Column(Uuid, ForeignKey('Products.Id'))
    Price = Column(Double, nullable=False)
    ActiveFrom = Column(TIMESTAMP, nullable=False)
    ActiveTo = Column(TIMESTAMP)
    CreateAt = Column(TIMESTAMP, nullable=False)
    UpdateAt = Column(TIMESTAMP)


class ProductMedia(Base):

    __tablename__ = 'ProductMedia'

    Id = Column(Uuid, primary_key=True, nullable=False, default=uuid4)
    ProductId = Column(Uuid, ForeignKey('Products.Id'), nullable=False)
    Url = Column(Text, nullable=False)
    Type = Column(VARCHAR(225), nullable=False)
    CreateAt = Column(TIMESTAMP, nullable=False)
    UpdateAt = Column(TIMESTAMP)


    def __init__(self, productId, url, type):
        self.ProductId = productId
        self.Url = url
        self.Type = type
        self.CreateAt = datetime.now()
    

    def __str__(self):
        return self.Url
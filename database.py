from sqlalchemy import create_engine, select, insert, text, update, delete, Table, Column, Date, Float, Integer, String, MetaData, ForeignKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, nullable=False)
  username = Column(String, nullable=False)
  password = Column(String, nullable=False)
  shopping_cart = relationship("ShoppingCart", uselist=False, back_populates="user")
  orders = relationship("Order", back_populates="user", uselist=False)

class Order(Base):
  __tablename__ = 'orders'

  id = Column(Integer, primary_key=True)
  status = Column(String, nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"))
  user = relationship("User", back_populates="orders")
  payment = relationship("Payment", uselist=False, backref="orders")
  date = Column(Date, nullable=False)
  store_items = relationship('StoreItem', secondary='orders_store_item_link')

class Address(Base):
  __tablename__ = 'address'

  id = Column(Integer, primary_key=True)
  address_line1 = Column(String, nullable=False)
  address_line2 = Column(String)
  city = Column(String, nullable=False)
  state = Column(String)
  country = Column(String, nullable=False)
  zip = Column(String)
  order_id = Column(Integer, ForeignKey("orders.id"))
  payment_id = Column(Integer, ForeignKey("payment.id"))
  
class Payment(Base):
  __tablename__ = 'payment'

  id = Column(Integer, primary_key=True)
  card_number = Column(Integer,nullable=False)
  cvv = Column(Integer, nullable=False)
  expiration = Column(Date, nullable=False)
  order_id = Column(Integer, ForeignKey("orders.id"))
  billing_address = relationship("Address", uselist=False, backref="payment")

class ShoppingCartItem(Base):
  __tablename__ = 'shopping_cart_item'

  id = Column(Integer, primary_key=True)
  count = Column(Integer, nullable=False)
  date_added = Column(Date, nullable=False)
  shopping_cart_id = Column(Integer, ForeignKey("shopping_cart.id"))
  shopping_cart = relationship("ShoppingCart", back_populates="items")
  item = relationship('StoreItem', secondary='shopping_cart_item_store_item_link')

class StoreItem(Base):
  __tablename__ = 'store_item'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  price = Column(Float, nullable=False)
  description = Column(String)
  stock = Column(Integer, nullable=False)
  category = Column(String)
  shopping_cart_item_id = relationship('ShoppingCartItem', secondary='shopping_cart_item_store_item_link')
  order_id = relationship('Order', secondary='orders_store_item_link')

class ShoppingCart(Base):
  __tablename__ = 'shopping_cart'

  id = Column(Integer, primary_key=True, nullable=False)
  date_created = Column(Date, nullable=False)
  items = relationship("ShoppingCartItem", uselist=False, back_populates="shopping_cart")
  user_id = Column(Integer, ForeignKey("users.id"))
  user = relationship("User", back_populates="shopping_cart")

# Association tables (many to many) tables below
class ShoppingCartItemStoreItemLink(Base):
  __tablename__ = 'shopping_cart_item_store_item_link'

  shopping_cart_item_id = Column(Integer, ForeignKey('shopping_cart_item.id'), primary_key=True)
  store_item_id = Column(Integer, ForeignKey("store_item.id"), primary_key=True)

class OrderStoreItemLink(Base):
  __tablename__ = 'orders_store_item_link'

  order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
  store_item_id = Column(Integer, ForeignKey("store_item.id"), primary_key=True)


class Database:
  engine = create_engine('sqlite:///:memory:')
  connection = engine.connect()

  def __init__(self):
    Base.metadata.create_all(self.engine)

    # insert test data

    # Address data
    ins = insert(Address).values(
      address_line1 = '62 Headline Road',
      address_line2 = 'Apartment 2',
      city = 'Starkville',
      state = 'MS',
      country = 'USA',
      zip = 39759
    )
    addr1_id = self.connection.execute(ins).inserted_primary_key[0]

    ins = insert(Address).values(
      address_line1 = '322 Annapurna Road',
      address_line2 = 'Ward Number 9',
      city = 'Pokhara, Kaski District',
      country = 'Nepal'
    )
    addr2_id = self.connection.execute(ins).inserted_primary_key[0]

    # User data
    ins = insert(User).values(
      username = 'justin',
      password = 'password1234'
    )
    justin_id = self.connection.execute(ins).inserted_primary_key[0]

    ins = insert(User).values(
      username='tanmay',
      password='professor'
    )
    tanmay_id = self.connection.execute(ins).inserted_primary_key[0]

    # ShoppingCart data
    ins = insert(ShoppingCart).values(
      date_created = date.today(),
      user_id = justin_id
    )
    justin_shopping_cart_id = self.connection.execute(ins).inserted_primary_key[0]

    # sel = select([User])
    # for row in self.connection.execute(sel):
    #   print(row)
    
    # sel = select([ShoppingCart])
    # for row in self.connection.execute(sel):
    #   print(row)

  """ Tries to auth user by username and password
  :param username:
  :param password:

  :return User.id of user
  """
  def auth_user(self, username: str, password: str):
    if len(username) > 0 and len(password) > 0:
      statement = text("SELECT * FROM users WHERE users.username = '{}' AND users.password = '{}'".format(username, password))
      result = self.connection.execute(statement)
      return result.lastrowid
    else:
      return -1

  def get_user_cart(self, uid: int) -> int:
    if uid > 0:
      statement = text("SELECT * FROM shopping_cart WHERE shopping_cart.user_id = '{}'".format(uid))
      return self.connection.execute(statement).fetchone().id
    else:
      return -1

    
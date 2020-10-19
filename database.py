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
  shipping_address = Column(Integer, ForeignKey("address.id"))
  shopping_cart = relationship("ShoppingCart", uselist=False, back_populates="user")
  orders = relationship("Order", back_populates="user", uselist=False)

class Order(Base):
  __tablename__ = 'orders'

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  user = relationship("User", back_populates="orders")
  payment = relationship("Payment", uselist=False, backref="orders")
  shipping_address = Column(Integer, ForeignKey("address.id"))
  date = Column(Date, nullable=False)
  item_id = Column(Integer, ForeignKey('store_item.id'))
  item = relationship("StoreItem", back_populates="order_items")

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
  shopping_cart = relationship("ShoppingCart")
  item_id = Column(Integer, ForeignKey('store_item.id'))
  item = relationship("StoreItem", back_populates="shopping_cart_items")

class StoreItem(Base):
  __tablename__ = 'store_item'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  price = Column(Float, nullable=False)
  description = Column(String)
  stock = Column(Integer, nullable=False)
  category = Column(String)
  shopping_cart_items = relationship("ShoppingCartItem", back_populates="item")
  order_items = relationship("Order", back_populates="item")
  order_id = relationship('Order', secondary='orders_store_item_link')

class ShoppingCart(Base):
  __tablename__ = 'shopping_cart'

  id = Column(Integer, primary_key=True, nullable=False)
  date_created = Column(Date, nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"))
  items = Column(Integer, ForeignKey("shopping_cart_item.id"))
  user = relationship("User", back_populates="shopping_cart")

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

    # StoreItem data
    ins = insert(StoreItem).values(
      name = "Stale Chips",
      price = 25.50,
      description = "10 year old bag of chips that no one wants",
      stock = 2,
      category = "Food"
    )
    self.connection.execute(ins)

    ins = insert(StoreItem).values(
      name = "Harry Potter Book",
      price = 15.99,
      description = "Classic Harry Potter Book",
      stock = 5,
      category = "Book"
    )
    self.connection.execute(ins)

  """ Tries to auth user by username and password
  :param username:
  :param password:

  :return User.id of user
  """
  def auth_user(self, username: str, password: str) -> int:
    if len(username) > 0 and len(password) > 0:
      statement = text("SELECT * FROM users WHERE users.username = '{}' AND users.password = '{}'".format(username, password))
      res = self.connection.execute(statement).fetchone()
      if res:
        return res.id
      else:
        return -1
    else:
      return -1

  def get_user_cart(self, uid: int) -> int:
    if uid > 0:
      statement = text("SELECT * FROM shopping_cart WHERE shopping_cart.user_id = '{}'".format(uid))
      res = self.connection.execute(statement).fetchone()
      if res:
        return res
      else:
        return -1
    else:
      return -1

  def get_cart_contents(self, cart_id: int):
    if cart_id > 0:
      statement = text("SELECT * FROM shopping_cart_item WHERE shopping_cart_item.shopping_cart_id = '{}'".format(cart_id))
      res = self.connection.execute(statement)
      if res:
        return res
      else:
        return -1

  def get_item_info(self, id: int):
    if id > 0:
      statement = text("SELECT * FROM store_item WHERE store_item.id = '{}'".format(id))
      res = self.connection.execute(statement).fetchone()
      if res:
        return res.id
      else:
        return -1
    else:
      return -1

  def get_item_by_category(self, category):
    statement = text("SELECT * FROM store_item WHERE store_item.category = '{}'".format(category[0]))
    res = self.connection.execute(statement).fetchone()
    if res:
      print(res)
      return res
    else:
      return -1

  def add_item_to_cart(self, uid: int, iid: int, count):
    if uid > 0 and iid > 0 and count > 0:
      statement = text("SELECT * FROM users WHERE users.id = '{}'".format(uid))
      res = self.connection.execute(statement).fetchone()
      if res:
        statement = text("SELECT * FROM store_item WHERE store_item.id = '{}'".format(iid))
        res = self.connection.execute(statement).fetchone()
        if res:
          cart_id = self.get_user_cart(uid).id
          ins = insert(ShoppingCartItem).values(
            count = count,
            date_added = date.today(),
            shopping_cart_id = cart_id,
            item_id = iid
          )
          self.connection.execute(ins)
          return 1
  
  def remove_item_from_cart(self, uid, iid, count):
    if uid > 0 and iid > 0 and count > 0:
      statement = text("SELECT * FROM users WHERE users.id = '{}'".format(uid))
      res = self.connection.execute(statement).fetchone()
      if res:
        cart_id = self.get_user_cart(uid).id
        statement = text("SELECT * FROM shopping_cart_item WHERE item_id = '{}'".format(iid))
        res = self.connection.execute(statement).fetchone()
        print(res.count)
        print(count)
        if res.count <= count:
          statement = text("DELETE FROM shopping_cart_item WHERE item_id = '{}'".format(iid))
          res = self.connection.execute(statement)
          if res:
            return 1
          else:
            return -1
        else:
          statement = text("UPDATE shopping_cart_item SET count = count - '{}' WHERE item_id = '{}'".format(count, iid))
          res = self.connection.execute(statement)
          if res:
            return 1
          else:
            return -1

  def complete_order(self, uid: int):
    if uid > 0:
      statement = text("SELECT * FROM users WHERE users.id = '{}'".format(uid))
      res = self.connection.execute(statement).fetchone()
      if res:
        cart_id = self.get_user_cart(uid).id
        cart_contents = self.get_cart_contents(cart_id)
        for row in cart_contents:
          statement = text("INSERT INTO orders (user_id, item_id, date) VALUES ('{}', '{}', '{}')".format(uid, row.item_id, date.today()))
          if not self.connection.execute(statement):
            return -1

  def print_orders(self, uid: int):
    if uid > 0:
      sel = select([Order])
      res = self.connection.execute(sel)
      if res:
        for row in res:
          print("id: {}, user_id: {}, item_id: {}".format(row.id, row.user_id, row.item_id))
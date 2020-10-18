from sqlalchemy import create_engine, select, Table, Column, Date, Float, Integer, String, MetaData, ForeignKeyConstraint, ForeignKey
from enum import Enum

class DB:

  # Upon __init__ of DB class, sqlite3 SQL tables are created and populated in memory (RAM)
  def __init__(self):
    self.engine = create_engine('sqlite:///:memory:')
    self.conn = self.engine.connect()
    self.metadata = MetaData()

    # initialize tables
    self.address = Table('address', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('address_line1', String, nullable=False),
      Column('address_line2', String),
      Column('city', String, nullable=False),
      Column('region', String),
      Column('country', String, nullable=False),
      Column('zip', String, nullable=False))

    self.payment = Table('payment', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('card_number', Integer, nullable=False),
      Column('cvv', Integer, nullable=False),
      Column('expiration', Date, nullable=False))

    # order is reserved word so use orders
    self.orders = Table('orders', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('item_id', Integer),
      Column('user', Integer, nullable=False),
      Column('shipping_address', Integer, nullable=False),
      Column('payment', Integer, nullable=False),
      Column('date', Date, nullable=False))

    self.user = Table('user', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('username', String, nullable=False),
      Column('password', String, nullable=False),
      Column('shipping_address', Integer, nullable=False),
      Column('order_history', Integer),
      Column('shopping_cart', Integer))

    self.shopping_cart = Table('shopping_cart', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('user', Integer, nullable=False),
      Column('items', Integer, nullable=False),
      Column('date_created', Date, nullable=False))
    
    self.shopping_cart_item = Table('shopping_cart_item', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('item', Integer, nullable=False),
      Column('count', Integer, nullable=False),
      Column('date_added', Date, nullable=False))

    self.store_item = Table('store_item', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('name', String, nullable=False),
      Column('price', Float, nullable=False),
      Column('description', String),
      Column('stock', Integer, nullable=False),
      Column('category', String))

    # Add Foreign Key Constraints

    address = Column('address', Integer, ForeignKey('address.id'))
    self.payment.append_column(address)

    item_id = Column('item_id', Integer, ForeignKey('store_item.id'))
    self.orders.append_column(item_id)
    shipping_address = Column('shipping_address', Integer, ForeignKey('address.id'))
    self.orders.append_column(shipping_address)
    payment = Column('payment', Integer, ForeignKey('payment.id'))
    self.orders.append_column(payment)
    user = Column('user', Integer, ForeignKey('user.id'))
    self.orders.append_column(user)

    order_history = Column('order_history', Integer, ForeignKey('orders.id'))
    self.user.append_column(order_history)
    shopping_cart = Column('shopping_cart', Integer, ForeignKey('shopping_cart.id'))
    self.user.append_column(shopping_cart)

    owner = Column('owner', Integer, ForeignKey('user.id'))
    self.shopping_cart.append_column(owner)
    items = Column('items', Integer, ForeignKey('shopping_cart_item.id'))
    self.shopping_cart.append_column(items)

    item = Column('item', Integer, ForeignKey('store_item.id'))
    self.shopping_cart_item.append_column(item)

    self.metadata.create_all(self.engine)

    self.setup_data()

  def setup_data(self):
    ins = self.address.insert().values(
      address_line1='62 Headline Way',
      address_line2='Apt. 9',
      city='Starkville',
      country='USA',
      zip=39759
    )
    self.engine.execute(ins)

    ins = self.user.insert().values(
      username='justin',
      password='testing123',
      shipping_address=1
    )
    self.engine.execute(ins)

  """ Generic method for performing 'SELECT * from a table'.
  :param self.table: DB.'table_name' for selecting from

  :return result <List> 
  """
  def select_all(self, table):
    sel = select([table])
    result = []
    for row in self.conn.execute(sel):
      result.append(row)
    return result

  def select_column(self, table_column):
    sel = select([table_column])
    result = []
    for row in self.conn.execute(sel):
      result.append(row)
    return result

  """ Select all records from 'user' table.
  :return result <List>
  """
  def select_users(self):
    return self.select_all(self.user)
  
  """ Select all records from 'orders' table.
  :return result <List>
  """
  def select_orders(self):
    return self.select_all(self.orders)

  """ Select all records from 'payment' table.
  :return result <List>
  """
  def select_payments(self):
    return self.select_all(self.payment)

  """ Select all records from 'address' table.
  :return result <List>
  """
  def select_addresses(self):
    return self.select_all(self.address)

  """ Select all records from 'shopping_cart' table.
  :return result <List>
  """
  def select_shopping_carts(self):
    return self.select_all(self.shopping_cart)

  """ Select all records from 'shopping_cart_item' table.
  :return result <List>
  """
  def select_shopping_cart_items(self):
    return self.select_all(self.shopping_cart_item)
  
  """ Select all records from 'store_item' table.
  :return result <List>
  """
  def select_store_items(self):
    return self.select_all(self.store_item)

  def select_address_by(self, column):
    for col in self.address.columns:
      if str(col) == 'address.' + column:
        return self.select_column(col)

  def __del__(self):
    self.conn.close()
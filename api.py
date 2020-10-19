from database import Database
db = Database()

class Api:
    """ Attempts to log in to the client.
    :param uname: User name
    :param pw: Password

    :raises Api.LoginError: Invalid login
    :return uid
    """
    def login(self, uname: str, pw: str) -> int:
        # Placeholder
        uid = db.auth_user(uname, pw)
        if uid:
          return uid
        else:
            raise self.LoginError

    """ Gets items from the database by a specific category
    :param uid: User id
    :param category: Category, str (can be None)
    
    :raises CategoryIDError: Category does not exist
    :return A list of items
    """
    def get_iids_by_category(self, category) -> list:
        res = db.get_item_by_category(category)
        if res:
          print(res)
          return res
        else:
            raise self.CategoryError

    """ Gets items from the database by a specific category
    :param uid: User id
    :param item_id: Item id (integer)
    :param count: Item count (optional, 1 by default)
    
    :raises ItemIdError: item does not exist
    :raises ValueError: count is too high or invalid
    :raises ValueError: number of items added exceeds stock
    
    :return if successful
    """
    def add_iid_to_cart(self, uid: int, iid: int, count=1):
      db.add_item_to_cart(uid, iid, count)

    """
    """
    def remove_iid_from_cart(self, uid: int, iid: int, count=1):
      db.remove_item_from_cart(uid, iid, count)

    """ Gets items from user's cart by their id
    :param uid: User id
    
    """
    def get_cart_by_uid(self, uid: int):
      cart = db.get_user_cart(uid)
      if cart:
        return cart
      else:
        return -1
    
    def print_cart(self, uid: int):
      cart = db.get_user_cart(uid)
      if cart:
        contents = db.get_cart_contents(cart.id)
        for cart_item in contents:
          print("id: {}, count: {}, shopping_cart_id: {}, item_id: {}".\
            format(cart_item.id, cart_item.count, cart_item.shopping_cart_id, cart_item.item_id))
      else:
        pass

    def get_item_by_iid(self, iid: int):
      return db.get_item_info(iid)

    def remove_iid_from_cart(self, uid: int, iid: int, count=None):
        pass

    def edit_address(self, uid, name, line1, line2, city, state, zipcode):
        pass

    def get_address_by_uid(self, uid):
        # Return None if none, otherwise return address
        pass

    def list_categories(self, uid):
        return ["Wingus", "Bingus"]

    def verify_card(self, ccd, cvc, exp):
        # lol
        return True

    def checkout(self, ccd, cvc, exp):
        pass

    class UserIdError(Exception):
        pass

    class ItemIdError(Exception):
        pass

    class CategoryError(Exception):
        pass

    class LoginError(Exception):
        pass

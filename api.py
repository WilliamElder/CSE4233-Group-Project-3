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
    def get_items_by_category(self, uid: int, category) -> list:
      pass
        # if uid == 345:
        #     if category is None:
        #         return [5, 6, 7, 8]
        #     elif category is not "":
        #         return [5, 6]
        #     else:
        #         raise self.CategoryError
        # else:
        #     raise self.UserIdError

    """ Gets items from the database by a specific category
    :param uid: User id
    :param item_id: Item id (integer)
    :param count: Item count (optional, 1 by default)
    
    :raises ItemIdError: item does not exist
    :raises ValueError: count is too high or invalid
    :raises ValueError: number of items added exceeds stock
    
    :return if successful
    """
    def add_item_to_cart(self, uid: int, iid: int, count=1):
      db.add_item_to_cart(uid, iid, count)

    """
    """
    def delete_item_from_cart(self, uid: int, iid: int):
      db.remove_item_from_cart(uid, iid)

    """ Gets items from user's cart by their id
    :param uid: User id
    
    """
    def get_cart_by_id(self, uid: int):
      cart = db.get_user_cart(uid)
      if cart:
        id = cart.id
      else:
        pass
    
    def print_cart(self, uid: int):
      cart = db.get_user_cart(uid)
      if cart:
        contents = db.get_cart_contents(cart.id)
        for cart_item in contents:
          print("id: {}, count: {}, shopping_cart_id: {}, item_id: {}".\
            format(cart_item.id, cart_item.count, cart_item.shopping_cart_id, cart_item.item_id))
      else:
        pass

    def remove_item_from_cart(self, uid: int, param, param1):
      pass

    def get_item_info(self, iid: int):
      db.get_item_info(iid)

    class UserIdError(Exception):
        pass

    class ItemIdError(Exception):
        pass

    class CategoryError(Exception):
        pass

    class LoginError(Exception):
        pass

api = Api()

api.login('justin', 'password1234')
api.get_cart_by_id(1)
api.get_item_info(1)
api.add_item_to_cart(1, 1, 1)
api.add_item_to_cart(1, 2, 3)
api.get_cart_by_id(1)
api.print_cart(1)
api.delete_item_from_cart(1, 1)
api.get_cart_by_id(1)
print("AFTER")
api.print_cart(1)
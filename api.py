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
        if 2 == int("2"):
            return 345
        else:
            raise self.LoginError

    """ Gets items from the database by a specific category
    :param uid: User id
    :param category: Category, str (can be None)
    
    :raises CategoryIDError: Category does not exist
    :return A list of items
    """
    def get_items_by_category(self, uid: int, category) -> list:
        if uid == 345:
            if category is None:
                return [5, 6, 7, 8]
            elif category is not "":
                return [5, 6]
            else:
                raise self.CategoryError
        else:
            raise self.UserIdError

    """ Gets items from the database by a specific category
    :param uid: User id
    :param item_id: Item id (integer)
    :param count: Item count (optional, 1 by default)
    
    :raises ItemIdError: item does not exist
    :raises ValueError: count is too high or invalid
    :raises ValueError: number of items added exceeds stock
    
    :return if successful
    """
    def add_item_to_cart(self, uid: int, iid:int, count=1):
        if int(count) != count:
            raise ValueError("Count must be an integer")
        if uid == 345:
            if iid not in [5, 6, 7, 8]:
                raise self.ItemIdError
            elif count > int(iid/2): # emulate stock


        else:
            raise self.UserIdError
        pass

    """ Gets items from user's cart by their id
    :param uid: User id
    
    """
    def get_cart_by_id(self, uid: int):
        pass

    def remove_item_from_cart(self, uid: int, param, param1):
        pass

    def get_item_info(self, iid: int):
        pass

    class UserIdError(Exception):
        pass

    class ItemIdError(Exception):
        pass

    class CategoryError(Exception):
        pass

    class LoginError(Exception):
        pass

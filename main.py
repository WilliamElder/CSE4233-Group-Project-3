import sys
from api import Api

class CLI:
    def __init__(self, api):
        self.api = api
        # Get the username and password from the command line
        uname, pw = "", ""
        try:
            uname, pw = sys.argv[1:]
        except ValueError:
            print(f"Usage: {sys.argv[0]} (username) (password)")
            exit(1)

        # Try to log in with the supplied username or password
        uid = 0
        try:
            uid = self.api.login(uname, pw)
        except ValueError:
            print("Invalid username or password!")
            exit(1)
        self.uid = uid

    def remove_item_from_cart(self, iid:int, count=None):
        try:
            return self.api.remove_item_from_cart(self.uid, iid, count)
        except self.api.UserIdError:
            print("Invalid user ID!")
            return False
        except self.api.ItemIdError:
            print(f"Invalid item ID {iid}!")
            return False

    def print_cart(self) -> None:
        try:
            items = self.api.get_cart_by_id(self.uid)
            items = items if items is not None else ["a"]
            for iid in items:
                print(self.api.get_item_info(iid))
        except self.api.UserIdError:
            print("Invalid user ID!")
            return

    @staticmethod
    def query_yn(prompt_string: str) -> bool:
        fail_count = 0
        while True:
            read = input(
                f"{(prompt_string + 'y/n').strip()} > ")
            if read.lower().strip() == "y":
                return True
            if read.lower().strip() == "n" or fail_count >= 3:
                return False
            fail_count += 1
            print(f'{read} is neither y or n')

    def change_address(self) -> bool:
        try:
            name = input("shipping name > ")
            line1 = input("address line 1 > ")
            line2 = input("address line 2 > ")
            city = input("city > ")
            state = input("state > ")
            zipcode = input("zip > ")
            resp = self.query_yn(f"\nDoes the following look correct?\n\n{name}\n{line1}\n{line2}\n{city}, {state}\n{zipcode}\n\n")
            if resp is False:
                print("Canceling change...")
                return False
            return self.api.edit_address(self.uid, name=name, line1=line1, line2=line2, city=city, state=state, zipcode=zipcode)
        except self.api.UserIdError:
            print("Invalid user ID!")
            return False

    def print_address(self):
        print(self.api.get_address_by_uid(self.uid))

    def get_items(self, category=None):
        items = self.api.get_items_by_category(self.uid, category)
        for item in items:
            print(self.api.get_item_info(item))

    def add_item(self, iid: int, count: int):
        try:
            res = self.api.add_item_to_cart(self.uid, iid, count)
            if not res:
                print(f"Unable to add {count} items to cart! have {self.api.get_item_info(iid).count}")

        except self.api.UserIdError:
            print("Invalid user ID!")
            return False
        except self.api.ItemIdError:
            print(f"Invalid item ID {iid}!")
            return False

    def list_cart(self):
        for item in self.api.get_cart_by_id(self.uid):
            print(item)

    def get_address(self):
        return self.api.get_address_by_uid(self.uid)

    def verify_card(self, ccd, cvc, exp):
        return self.api.verify_card(ccd, cvc, exp)

    def list_categories(self):
        for category in self.api.list_categories(self.uid):
            print(category)

    def checkout(self, ccd, cvc, exp):
        return self.api.checkout(ccd, cvc, exp)


def print_help():
    print("Usage:")
    print("\t* denotes optional arguments")
    print("\t# denotes an integer argument")
    print("\t() denotes function parameter")
    print("General commands:")
    print("\thelp                         Print this message")
    print("\tquit                         Exit the application")
    print("\texit                         Exit the application")
    print("Shopping commands:")
    print("\tlist category                List categories of items")
    print("\tlist item   (*category)      List items available for purchase, by category if specified")
    print("\tadd item    (item#) (*count) Add item to cart")
    print("\tlist cart                    List items in shopping cart")
    print("\tremove item (item#) (*count) Remove item from cart")
    print("\tcheckout                     Check out")
    print("Account commands:")
    print("\tedit address                 Change the default address for checkout")


def main_function():
    api = Api()
    cli = CLI(api)
    running = True  # There's no do-while loop in Python, so we use this instead
    print_help()
    while running:
        # Tokenize the command
        cmd = [i.strip() for i in input(">").strip().split(" ")]
        # Quit or exit
        if len(cmd) >= 1 and cmd[0] == "quit" or cmd[0] == "exit":
            exit(0)
        if len(cmd) >= 1 and cmd[0] == "help":
            print_help()
            continue
        # handle list item
        elif len(cmd) >= 2 and cmd[0] == "list" and cmd[1] == "item":
            if len(cmd) == 2:
                cli.get_items(None)
            elif len(cmd) == 3:
                cli.get_items(cmd[2])
            else:
                print("Invalid number of arguments!")
        # Add items to cart
        elif len(cmd) >= 2 and cmd[0] == "add" and cmd[1] == "item":
            if len(cmd) == 2:
                print("Add requires item id!")
                continue
            elif 2 < len(cmd) < 5:
                iid = None
                try:
                    iid = int(cmd[2])
                except ValueError:
                    print(f"Unable to parse {cmd[2]} as integer!")
                    continue
                count = 1
                if len(cmd) == 4:
                    try:
                        count = int(cmd[3])
                    except ValueError:
                        print(f"Unable to parse {cmd[3]} as integer!")
                        continue
                cli.add_item(iid, count)
            else:
                print("Invalid number of items!")
        # List items in cart
        elif len(cmd) >= 2 and cmd[0] == "list" and cmd[1] == "cart":
            cli.list_cart()
        # Remove item from cart
        elif len(cmd) >= 2 and cmd[0] == "remove" and cmd[1] == "item":
            if len(cmd) <= 2 or len(cmd) > 4:
                print("Remove item requires 1-2 arguments!")
            try:
                iid = int(cmd[2])
            except ValueError:
                print(f"Unable to parse {cmd[2]} as integer!")
                continue
            count = None
            try:
                if len(cmd) > 3:
                    count = int(cmd[3])
            except ValueError:
                print(f"Unable to parse {cmd[3]} as integer!")
                continue
            cli.remove_item_from_cart(iid, count)
        elif len(cmd) >= 2 and cmd[0] == "list" and cmd[1] == "category":
            cli.list_categories()
        elif len(cmd) >= 1 and cmd[0] == "checkout":
            print('Are you sure you want to check out with these items?')
            cli.print_cart()
            if cli.query_yn("") is False:
                continue
            if cli.get_address() is None:
                print("There is no address on record for your account. Would you like to add one?")
                print("Answering no will abort checkout")
                if cli.query_yn("") is False:
                    continue
                cli.change_address()
            print("Is the following address correct?")
            cli.print_address()
            ccd = input("Enter your credit card number > ")
            cvc = input("Enter your CVC (numbers on the back) > ")
            exp = input("Enter your expiration date > ")
            print("Is the following credit card information correct?")
            print(f"Card number: {ccd}")
            print(f"CVC: {cvc}")
            print(f"Expiry: {exp}")
            cli.verify_card(ccd, cvc, exp)
            cli.checkout(ccd, cvc, exp)
        elif cmd[0] == "edit" and cmd[1] == "address":
            cli.change_address()
        else:
            print(f"Unknown command: {cmd}, type \"help\" for a list of commands")





if __name__ == "__main__":
    main_function()

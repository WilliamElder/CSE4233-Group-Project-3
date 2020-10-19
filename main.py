import sys
from api import Api


def login_from_cli(api:Api):
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
        uid = api.login(uname, pw)
    except ValueError:
        print("Invalid username or password!")
        exit(1)
    return uid


def cmd_remove_item_from_cart(api, uid, cmd):
    try:
        if len(cmd) == 0:
            print("Missing argument: ItemID")
            return False
        elif len(cmd) == 1:
            iid = int(cmd[0])
            return api.remove_item_from_cart(uid, iid)
        elif len(cmd) == 2:
            iid = int(cmd[0])
            count = int(cmd[2])
            return api.remove_item_from_cart(uid, iid, count)
    except api.UserIdError:
        print("Invalid user ID!")
        return False
    except api.ItemIdError:
        print(f"Invalid item ID {cmd[0]}!")
        return False


def cmd_print_cart(api, uid) -> None:
    items = api.get_cart_by_id(uid)
    for iid in items:
        print(api.get_item_info(iid))


def cmd_query_yn(prompt:str) -> bool:
    fail_count = 0
    while True:
        read = input(
            f"{prompt} y/n > ")
        if read.lower().strip() == "y":
            return True
        if read.lower().strip() == "n" or fail_count >= 3:
            return False
        fail_count += 1
        print(f'{read} is neither y or n')


def cmd_change_address(api, uid) -> bool:
    name = input("shipping name > ")
    line1 = input("address line 1 > ")
    line2 = input("address line 2 > ")
    city = input("city > ")
    state = input("state > ")
    zip = input("zip > ")
    fail_count = 0
    resp = cmd_query_yn(f"\nDoes the following look correct?\n\n{name}\n{line1}\n{line2}\n{city}, {state}\n{zip}\n\n")
    if resp is False:
        print("Canceling change...")
        return False
    api.edit_address(uid, name=name, line1=line1, line2=line2, city=city, state=state, zip=zip)
    return True

def cmd_print_address(str):
    pass

def print_help():
    print("Usage:")
    print("\t* denotes optional arguments")
    print("General commands:")
    print("\thelp                         Print this message")
    print("\tquit                         Exit the application")
    print("\texit                         Exit the application")
    print("Shopping commands:")
    print("\tlist category                List categories of items")
    print("\tlist item   (category*)      List items available for purchase, by category if specified")
    print("\tadd item    (item#) (count*) Add item to cart")
    print("\tlist cart                    List items in shopping cart")
    print("\tremove item (item#) (count*) Remove item from cart")
    print("\tcheckout                     Check out")
    print("Account commands:")
    print("\tedit address                 Change the default address for checkout")


def main_function():
    api = Api()
    uid = login_from_cli(api)
    running = True  # There's no do-while loop in Python, so we use this instead
    print_help()
    while running:
        cmd = [i.strip() for i in input(">").strip().split(" ")]
        if cmd[0] == "quit" or cmd[0] == "exit":
            exit(1)
        elif cmd[0] == "list" and cmd[1] == "item":
            items = api.get_items_by_category(uid, None if len(cmd) < 3 else cmd[2])
            for item_id in items:
                print(api.get_item_info(item_id))
        elif cmd[0] == "add":
            print(api.add_item_to_cart(uid, int(cmd[1]), cmd[2]))
        elif cmd[0] == "list" and cmd[1] == "cart":
            print(api.get_cart_by_id(uid))

        elif cmd[0] == "remove" and cmd[1] == "item":
            cmd_remove_item_from_cart(api, uid, cmd[2:])
        elif cmd[0] == "checkout":
            print('Are you sure you want to check out with these items?')
            cmd_print_cart(api, uid)
            if cmd_query_yn("") is False:
                continue
            if api.get_address_by_uid(uid) is None:
                print("There is no address on record for your account. Would you like to add one?")
                print("Answering no will abort checkout")
                if cmd_query_yn("") is False:
                    continue
                cmd_change_address(api, uid)
            print("Is the following address correct?")
            cmd_print_address(api, uid)

            ccd = input("Enter your credit card number > ")
            cvc = input("Enter your CVC (numbers on the back) > ")

        elif cmd[0] == "edit" and cmd[1] == "address":
            print(cmd_change_address(api, uid))





if __name__ == "__main__":
    main_function()

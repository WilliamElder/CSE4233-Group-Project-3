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
    uid = login_from_cli()
    running = True  # There's no do-while loop in Python, so we use this instead
    print_help()
    api = Api()
    while running:
        cmd = [i.strip() for i in input(">").strip().split(" ")]
        print(cmd)
        if cmd[0] == "quit" or cmd[0] == "exit":
            exit(1)
        elif cmd[0] == "list" and cmd[1] == "item":
            items = api.get_items_by_category(uid, cmd[2])
            for item_id in items:
                print(api.get_item_info(item_id))
        elif cmd[0] == "add":
            print(api.add_item_to_cart(uid, cmd[1], cmd[2]))
        elif cmd[0] == "list" and cmd[1] == "cart":
            print(api.get_cart_by_id(uid))
        elif cmd[0] == "remove" and cmd[1] == "item":
            print(api.remove_item_from_cart(uid, cmd[2], cmd[3]))
        elif cmd[0] == "checkout":
            pass
        elif cmd[0] == "edit" and cmd[1] == "address":
            read = ""
            name = input("shipping name > ")
            line1 = input("address line 1 > ")
            line2 = input("address line 2 > ")
            city = input("city > ")
            state = input("state > ")
            zip = input("zip > ")
            while True:
                read = input(f"Does the following look correct?\n{name}\n{line1}\n{line2}\n{city}, {state}\n{zip}\ny/n")
                if read.lower().strip() == "y":
                    print(api.edit_address(name=name, line1=line1, line2=line2, city=city, state=state, zip=zip))
                if read.lower().strip() == "n":
                    continue

            print(api.edit_address())




if __name__ == "__main__":
    main_function()

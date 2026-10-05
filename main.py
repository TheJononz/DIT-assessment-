import json
from datetime import datetime

local_array_of_users = []

#constants
BASE_PRICE_INC_GST = 75000
GST_RATE = 0.15
TRADE_DISCOUNT = 0.10

ONE_G_SOCKET_PRICE = 40
TWO_G_SOCKET_PRICE = 50
NETWORK_POINT_PRICE = 50
NETWORK_SWITCH_PRICE = 100

MAX_SOCKETS_TOTAL = 12
MAX_SOCKETS_PER_ROOM = 4
MAX_NETWORK_POINTS = 8
MIN_NETWORK_ROOMS = 2









class Option:
    def __init__(self, name, price):
        self.name = name 
        self.price = price

    def get_total(self):
        return self.price

    def get_as_dict(self):
        return {
            "name": self.name,
            "price": self.price
        }

class Socket:
    def __init__(self, socketType, quantity):
        self.socketType = socketType
        self.quantity = quantity

        if socketType == "1G":
            self.price = ONE_G_SOCKET_PRICE
        elif socketType == "2G":
            self.price = TWO_G_SOCKET_PRICE

    def get_total(self):
        return self.price * self.quantity

    def get_as_dict(self):
        return {
            "type": self.socketType,
            "quantity": self.quantity,
            "price": self.price,
            "total": self.get_total()
        }

class Networkpoints:
    def __init__(self, quantity):
        self.quantity = quantity
        self.price = NETWORK_POINT_PRICE

    def get_total(self):
        return self.price * self.quantity

    def get_as_dict(self):
        return {
            "quantity": self.quantity,
            "price": self.price,
            "total": self.get_total()
        }

class NetworkSwitch:
    def __init__(self):
        self.name = "8-port 10/100/1000 Network Switch"
        self.price = NETWORK_SWITCH_PRICE

    def get_total(self):
        return self.price

    def get_as_dict(self):
        return {
            "name": self.name,
            "price": self.price
        }

class Room:
    def __init__(self, name):
        self.name = name
        self.options = []
        self.sockets = []
        self.network_points = None

    def add_option(self, option):
        self.options.append(option)

    def add_sockets(self, socket):
        self.sockets.append(socket)

    def add_networkPoints(self, networkPoints):
        self.network_points = networkPoints

    def get_socket_total(self):
        total = 0
        for sockets in self.sockets:
            total += sockets.quantity
        return total

    def get_network_points_total(self):
        if self.network_points is None:
            return 0
        return self.network_points.quantity

    def get_total(self):
        total = 0

        for option in self.options:
            total += option.get_total()
        for socket in self.sockets:
            total += socket.get_total()
        if self.network_points is not None:
            total += self.network_points.get_total()

        return total
    
    def get_as_dict(self):
        return {
            "name": self.name,
            "options": [
                option.get_as_dict()
                for option in self.options
            ],
            "sockets": [
                socket.get_as_dict()
                for socket in self.sockets
            ],
            "network_points":
                self.network_points.get_as_dict()
                if self.network_points is not None
                else None,
            "total": self.get_total()
        }

class Tinyhome:
    def __init__(self):
        self.basePriceIncGst = BASE_PRICE_INC_GST
        self.rooms = [
            Room("Bathroom"),
            Room("Kitchen"),
            Room("Living Room"),
            Room("Bedroom 1"),
            Room("Bedroom 2")
        ]

        self.network_switch = None

    def get_room(self, room_name):
        for room in self.rooms:
            if room.name == room_name:
                return room
        return None

    def get_total_sockets(self):
        total = 0
        for room in self.rooms:
            total += room.get_socket_total()
        return total

    def get_total_network_points(self):
        total = 0
        for room in self.rooms:
            total += room.get_network_points_total()
        return total
    
    def get_network_room_count(self):
        total = 0
        for room in self.rooms:
            if room.get_network_points_total() > 0:
                total += 1
        return total

    def get_options_total(self):
        total = 0
        for room in self.rooms:
            total += room.get_total()
        if self.network_switch is not None:
            total += self.network_switch.get_total()
        return total   

class User:
    def __init__(self, fname, lname, address, customerType, phone, email):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.customerType = customerType
        self.phone = phone
        self.email = email

    def get_as_dict(self) -> dict:
        return {
            "fname": self.fname,
            "lname": self.lname,
            "address": self.address,
            "customerType": self.customerType,
            "phone": self.phone,
            "email": self.email
        }

class Users:
    def __init__(self, users: list):
        self.users = users

    def user_dict(self):
        totals = []
        for user in self.users:
            totals.append(user.get_as_dict())
        return totals

class Quotes:
    def __init__(self, quoteNum, quotedate, user, dAddress):
        self.quoteNum = quoteNum
        self.quotedate = quotedate
        self.user = user
        self.dAddress = dAddress
        self.home = Tinyhome()
        self.discountRate = 0
        self.discountValue = 0
        self.totalPriceExcGst = 0
        self.gst = 0
        self.totalPriceIncGst = 0

    def calculate_total(self):
        base_price_exc_gst = (
            self.home.base_price_inc_gst / (1 + GST_RATE)
        )
        options_total = self.home.get_options_total()
        subtotal = base_price_exc_gst + options_total
        if self.user.customerType.lower() == "trade":
            self.discountRate = TRADE_DISCOUNT
        else:
            self.discountRate = 0
        self.discountValue = subtotal * self.discountRate
        self.totalPriceExcGst = subtotal - self.discountValue
        self.gst = self.totalPriceExcGst * GST_RATE
        self.totalPriceIncGst = (
            self.totalPriceExcGst + self.gst
        )

    def get_as_dict(self):
        return {
            "quoteNum": self.quoteNum,
            "quoteDate": self.quoteDate,
            "fname": self.user.fname,
            "lname": self.user.lname,
            "address": self.user.address,
            "dAddress": self.deliveryAddress,
            "customerType": self.user.customerType,
            "discountRate": self.discountRate,
            "discountValue": self.discountValue,
            "totalPriceExcGst": self.totalPriceExcGst,
            "gst": self.gst,
            "totalPriceIncGst": self.totalPriceIncGst,
            "home": {
                "rooms": [
                    room.get_as_dict()
                    for room in self.home.rooms
                ]
            }
        }











def load_from_dict(user_dict:dict) -> User:
    return User(user_dict["fname"], user_dict["lname"], user_dict["address"], user_dict["customerType"], user_dict["phone"], user_dict["email"])

def open_json_file():
    with open("users.json", "r") as fp:
        user_json = json.load(fp)
    uploaded_user_array = []
    for user_dict in user_json:
        uploaded_user_array.append(load_from_dict(user_dict))
    return uploaded_user_array

local_array_of_users = open_json_file()

def dump_local_data():
    with open("users.json", "w") as fp:
       json.dump(Users(local_array_of_users).user_dict(), fp, indent=4)

def remove_user(user_fname, user_lname):
    for User in local_array_of_users:
        if User.fname == user_fname and User.lname == user_lname:
            local_array_of_users.remove(User)
            break

def diplay_all_users():
    for User in local_array_of_users:
        print(f"first name: {User.fname}, last name: {User.lname}, address: {User.address}, customer type: {User.customerType}, phone: {User.phone}, email: {User.email}")

def get_input(message):
    value = input(message)
    if value.lower() == "c":
        raise Exception("CANCEL")
    return value

def create_user():
    try:
        print("Type C at any time to cancel.")

        fname = get_input("First name: ")
        lname = get_input("Last name: ")
        address = get_input("Address: ")
        customerType = get_input("Customer type (Trade/Retail): ")
        customerType = customerType.capitalize()

        while customerType not in ["Trade", "Retail"]:
            print("Please enter Trade or Retail.")
            customerType = get_input(
                "Customer type (Trade/Retail): "
            )
            customerType = customerType.capitalize()

        phone = get_input("Phone number: ")
        email = get_input("Email: ")

        new_user = User(
            fname,
            lname,
            address,
            customerType,
            phone,
            email
        )

        return new_user

    except Exception as error:
        if str(error) == "CANCEL":
            print("User creation cancelled.")
            return None
        raise

def select_user():
    if len(local_array_of_users) == 0:
        print("there are no users")
        return None

    print("CUSTOMERS")

    for index, users in enumerate(local_array_of_users, start=1):
        print(f"{index}. {users.fname} {users.lname}, {users.customerType}")

    while True:
        try:
            choice = get_input(
                "Choose customer number: "
            )
            choice = int(choice)
            if 1 <= choice <= len(local_array_of_users):
                return local_array_of_users[choice - 1]
            
            print("Invalid customer number.")

        except ValueError:
            print("Please enter a number.")

def choose_bathroom_options(room):

    print("\n--- BATHROOM ---")
    print("1. Tiles, spa bath, shower and tapware - $2500")
    print("2. No bathroom upgrade")

    choice = get_input("Choose option: ")

    if choice == "1":
        room.add_option(
            Option("Tiles, spa bath, shower and tapware",2500)
        )

    elif choice != "2":
        print("Invalid choice.")
        choose_bathroom_options(room)

def choose_kitchen_options(room):

    print("\n--- KITCHEN ---")
    print("1. No upgrade - $0")
    print("2. Kitchen Option A - $2000")
    print("3. Kitchen Option B - $3500")
    print("4. Kitchen Option C - $6000")

    choice = get_input("Choose option: ")

    if choice == "1":
        pass
    elif choice == "2":
        room.add_option(
            Option(
                "Kitchen Option A - upgraded units/worktop", 2000
            )
        )
    elif choice == "3":
        room.add_option(
            Option(
                "Kitchen Option B - upgraded units/worktop + induction hob", 3500
            )
        )
    elif choice == "4":
        room.add_option(
            Option(
                "Kitchen Option C - upgraded units/worktop + Deluxe appliance pack", 6000
            )
        )
    else:
        print("Invalid choice.")
        choose_kitchen_options(room)

def choose_living_options(room):

    print("\n--- LIVING ROOM ---")
    print("1. No upgrade - $0")
    print("2. TV point + roof aerial - $250")
    print("3. TV + satellite dish - $250")
    print("4. 4.5KW heat pump - $2500")

    choice = get_input("Choose option: ")

    if choice == "1":
        pass
    elif choice == "2":
        room.add_option(
            Option(
                "TV point + roof aerial", 250
            )
        )
    elif choice == "3":
        room.add_option(
            Option(
                "TV + satellite dish", 250
            )
        )
    elif choice == "4":
        room.add_option(
            Option(
                "4.5KW heat pump", 2500
            )
        )
    else:
        print("Invalid choice.")
        choose_living_options(room)

def choose_bedroom_options(room):

    print(f" {room.name.upper()}")
    print("1. No upgrade - $0")
    print("2. 2.5KW heat pump - $1800")

    choice = get_input("Choose option: ")
    if choice == "1":
        pass
    elif choice == "2":
        room.add_option(
            Option(
                "2.5KW heat pump", 1800
            )
        )

    else:
        print("Invalid choice.")
        choose_bedroom_options(room)

def choose_sockets(room, home):

    print(f"EXTRA SOCKETS: {room.name}")

    print(f"You can have a maximum of {MAX_SOCKETS_PER_ROOM} extra sockets in this room.")
    print("1. No extra sockets")
    print("2. 1G sockets - $40 each")
    print("3. 2G sockets - $50 each")

    choice = get_input("Choose option: ")
    if choice == "1":
        return
    if choice not in ["2", "3"]:
        print("Invalid choice.")
        choose_sockets(room, home)
        return

    try:
        quantity = int(get_input("How many sockets? "))
    except ValueError:

        print("Please enter a number.")
        choose_sockets(room, home)
        return

    if quantity < 1:
        print("Quantity must be at least 1.")
        choose_sockets(room, home)
        return
    if quantity > MAX_SOCKETS_PER_ROOM:
        print(f"You can only have {MAX_SOCKETS_PER_ROOM} sockets in one room.")
        choose_sockets(room, home)
        return

    current_room_sockets = room.get_socket_total()
    if current_room_sockets + quantity > MAX_SOCKETS_PER_ROOM:
        print("This room would have too many extra sockets.")
        choose_sockets(room, home)
        return

    total_house_sockets = home.get_total_sockets()
    if total_house_sockets + quantity > MAX_SOCKETS_TOTAL:
        print(f"The whole house can only have {MAX_SOCKETS_TOTAL} extra sockets.")
        choose_sockets(room, home)
        return

    if choice == "2":
        socket = Socket("1G", quantity)
    else:
        socket = Socket("2G", quantity)
    room.add_socket(socket)

    
def choose_network_points(room, home):

    print(f"NETWORK POINTS: {room.name}")
    print("Network points cost $50 each.")
    print("Minimum of 2 rooms must have network points.")
    print(f"Maximum of {MAX_NETWORK_POINTS} points total.")

    choice = get_input("How many network points in this room? ")
    try:
        quantity = int(choice)
    except ValueError:
        print("Please enter a number.")
        choose_network_points(room, home)
        return

    if quantity < 0:
        print("Quantity cannot be negative.")
        choose_network_points(room, home)
        return
    if quantity == 0:
        return
    
    current_points = home.get_total_network_points()
    if current_points + quantity > MAX_NETWORK_POINTS:
        print(f"You can only have {MAX_NETWORK_POINTS} network points total.")
        choose_network_points(room, home)
        return

    network_points = Networkpoints(quantity)

    room.add_network_points(network_points)


def create_quote():

    try:
        print("\n========================")
        print("CREATE NEW QUOTE")
        print("========================")
        print("Type C at any point to cancel.\n")

        user = select_user()
        if user is None:
            return None

        deliveryAddress = get_input("Delivery address: ")

        quoteNum = (
            user.fname[:2]+ user.lname[:2]+ datetime.now().strftime("%d%m%Y%H%M%S")).upper()
        quoteDate = datetime.now().strftime("%d/%m/%Y %H:%M")

        quote = Quotes(
            quoteNum,
            quoteDate,
            user,
            deliveryAddress
        )
        home = quote.home
        #options for bathroom
        choose_bathroom_options(home.get_room("Bathroom"))
        choose_sockets(home.get_room("Bathroom"),home)
        choose_network_points(home.get_room("Bathroom"),home)

        #options for kitchen
        choose_kitchen_options(home.get_room("Kitchen"))
        choose_sockets(home.get_room("Kitchen"),home)
        choose_network_points(home.get_room("Kitchen"),home)

        #options for living room
        choose_living_options(home.get_room("Living Room"))
        choose_sockets(home.get_room("Living Room"),home)
        choose_network_points(home.get_room("Living Room"),home)

        #options for bedroom one
        choose_bedroom_options(home.get_room("Bedroom 1"))
        choose_sockets(home.get_room("Bedroom 1"),home)
        choose_network_points(home.get_room("Bedroom 1"),home)

        #options for bedroom two
        choose_bedroom_options(home.get_room("Bedroom 2"))
        choose_sockets(home.get_room("Bedroom 2"),home)
        choose_network_points(home.get_room("Bedroom 2"),home)

        #completing network requirements 
        network_rooms = home.get_network_room_count()
        if home.get_total_network_points() > 0:
            if network_rooms < MIN_NETWORK_ROOMS:
                print("You need network points in at least 2 different rooms.")
                print("The quote has been cancelled.")
                return None

            home.network_switch = NetworkSwitch()
        quote.calculate_total()
        return quote

    except Exception as error:
        if str(error) == "CANCEL":
            print("\nQuote cancelled.")
            return None
        raise

"""
def create_array_of_quotes():
    while True:
        print("ALL USERS:")
        for User in local_array_of_users:
            print(f" USER : first name: {User.fname}, last name: {User.lname}")  
        print("choose user")

        while True:
            fname = input("first name: ")
            selectedUser = None
            for user in local_array_of_users:
                if fname == user.fname:
                    selectedUser = user

            if selectedUser:
                lname = selectedUser.lname
                address = selectedUser.address
                customerType = selectedUser.customerType
                break
            else:
                print("not a valid user")
              
        dAddress = input("delivery address: ")
"""
                







    
while True:
    
    choice = int(input("1 = create user , 2 = save data 3 = deleat user, 4 = display all users, 5 = create new quote  "))

    if choice == 1:
        new_user = create_user()
        local_array_of_users.append(new_user)

    elif choice == 2:
        dump_local_data()

    elif choice == 3:
        user_remove_fname = input("user first name: ")
        user_remove_lname = input("user last name: ")
        remove_user(user_remove_fname, user_remove_lname)
    
    elif choice == 4:
        diplay_all_users()

    elif choice == 5:
        create_quote()

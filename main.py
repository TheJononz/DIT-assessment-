
#my librarys that i imported
import json
from datetime import datetime
#where I store my local list of users as objects
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






# in this code i make heay use of objetcs, where if i can have a peice of information as an object i do

#object for all my options
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
#object for the sockets. this is usefull to keep track between 1G and 2G, also creating the price ect
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
#esentaly the same as hte sockets, but for the network
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
#same consept
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
#this object us for the room, where each individual room has its distinct options and socket types, so the user can be asked abut things on a room by room baisis
#like the spesifications say
class Room:
    def __init__(self, name):
        self.name = name
        self.options = []
        self.sockets = []
        self.network_points = None

    def add_option(self, option):
        self.options.append(option)

    def add_socket(self, socket):
        self.sockets.append(socket)

    def add_network_points(self, networkpoints):
        self.network_points = networkpoints

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

#this is an amalgamation of all the room objects into the tinyhome so that total prices can be worked out, as well as the number of sockets and switches 
class Tinyhome:
    def __init__(self):
        self.base_price_inc_gst = BASE_PRICE_INC_GST
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

#this object oid for the users. the way that my users work is they are stored localy as an array of objects, and i can convert this into an array of dictonarys,
#and then this can be saved to a json file. when the program restarts it automaticly pulles all the data from that json file and then it gets converted into the local
#storage. when a user is added or removed they are added or removed to this local storage (called local_array_of_users) and then when that is saved it overrites the json
#file. this is how I manage my users
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


# an objetc for when i create the quote. this is where the calculations for the discounds and stuff happen.
class Quotes:
    def __init__(self, quoteNum, quoteDate, user, dAddress):
        self.quoteNum = quoteNum
        self.quoteDate = quoteDate
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






#creates a user ibject from a dictonary
def load_from_dict(user_dict:dict) -> User:
    return User(user_dict["fname"], user_dict["lname"], user_dict["address"], user_dict["customerType"], user_dict["phone"], user_dict["email"])

#opens the json file and takes that data, turns it into objects and chucks it into local storage
def open_json_file():
    with open("users.json", "r") as fp:
        user_json = json.load(fp)
    uploaded_user_array = []
    for user_dict in user_json:
        uploaded_user_array.append(load_from_dict(user_dict))
    return uploaded_user_array

local_array_of_users = open_json_file()

#saves users by taking the array of objects, converst it into dictonary and writes it to json
def dump_local_data():
    with open("users.json", "w") as fp:
       json.dump(Users(local_array_of_users).user_dict(), fp, indent=4)

#finds spesific user adn then removes them
def remove_user():
    User = select_user()
    local_array_of_users.remove(User)


#loops through array o users and displays them 
def diplay_all_users():
    for User in local_array_of_users:
        print(f"first name: {User.fname}, last name: {User.lname}, address: {User.address}, customer type: {User.customerType}, phone: {User.phone}, email: {User.email}")

# this function is for allowing the user to cancel at any time by taking advantage of raise Exception 
def get_input(message):
    value = input(message)
    if value.lower() == "c":
        raise Exception("CANCEL")
    return value

# creates a user
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

#is able to select a user baised off of there index number in there position in the array of users
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



# all of the next functions are for chosing the options of the room upgrades. alot of code and fairly repetitive but i could not find a better way to do it unfortunetly
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


#creating the quote by calling all the functions up top, and then returning the quote object to be saved to a .txt file
def create_quote():

    try:
        print("CREATE NEW QUOTE")
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

# saving the quote, just made sure it is readable and layed out reasonably
def save_quote(quote):

    with open("QuoteHistory.txt", "a") as file:

        file.write("================================================\n")
        file.write("WAIMAK BUILD CO LTD \n")
        file.write("Unit 3, 93 McKenzie Street \n")
        file.write("Rangiora, North Canterbury \n")
        file.write("Tel: 03 1234567 \n")
        file.write("Email: Office@wbc.co.nz \n")
        file.write(f"Quote Number: {quote.quoteNum} \n")
        file.write(f"Quote Date: {quote.quoteDate} \n")
        file.write(f"Customer: {quote.user.fname} {quote.user.lname} \n")
        file.write(f"Customer Address: {quote.user.address} \n")
        file.write(f"Delivery Address: {quote.dAddress} \n")
        file.write(f"Customer Type: {quote.user.customerType} \n")
        file.write("ROOMS ")

        for room in quote.home.rooms:
            file.write(f"{room.name} \n")

            for option in room.options:
                file.write(f"  {option.name}: ${option.price:,.2f} \n")

            for socket in room.sockets:
                file.write(f"  {socket.quantity} x {socket.socketType} sockets: ${socket.get_total():,.2f}\n" )

            if room.network_points is not None:
                file.write(f"  {room.network_points.quantity} network points: ${room.network_points.get_total():,.2f}\n ")

            file.write(f"  Room total: ${room.get_total():,.2f} \n")

        if quote.home.network_switch is not None:
            file.write(f"Network switch: ${quote.home.network_switch.price:,.2f} \n")

        file.write(f"\nDiscount rate: {quote.discountRate * 100:.0f}% \n")
        file.write(f"Discount value: -${quote.discountValue:,.2f}\n")
        file.write(f"Total excluding GST: ${quote.totalPriceExcGst:,.2f} \n")
        file.write(f"GST: ${quote.gst:,.2f} ")
        file.write(f"Total including GST: ${quote.totalPriceIncGst:,.2f} \n")
        file.write("================================================\n")

    print("\nQuote saved to QuoteHistory.txt.")


def quote_finished_menu(quote):

    while True:
        print("1 = Save quote")
        print("2 = Do not save")

        choice = input("Choose: ")
        if choice == "1":
            save_quote(quote)
            return
        elif choice == "2":

            print("Quote was not saved.")
            return
        else:

            print("Invalid choice.")



#main program 
while True:
    
    choice = int(input("1 = create user , 2 = save data 3 = deleat user, 4 = display all users, 5 = create new quote, 6 = exit program :"))

    if choice == 1:
        new_user = create_user()
        local_array_of_users.append(new_user)

    elif choice == 2:
        dump_local_data()

    elif choice == 3:
        remove_user()
    
    elif choice == 4:
        diplay_all_users()

    elif choice == 5:
        quote = create_quote()
        quote_finished_menu(quote)
    elif choice == 6:
        print("goodbye :) ")
        break
    else:
        print("invalad choice")

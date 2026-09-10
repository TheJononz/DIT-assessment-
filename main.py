import json


local_array_of_users = []

class User:
    def __init__(self, fname, lname, address, dAddress, customerType ):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.dAddress = dAddress
        self.customerType = customerType

    def get_as_dict(self) -> dict:
        return {
            "fname": self.fname,
            "lname": self.lname,
            "address": self.address,
            "dAddress": self.dAddress,
            "customerType": self.customerType
        }

class Users:
    def __init__(self, users: list):
        self.users = users

    def user_dict(self):
        totals = []
        for user in self.users:
            totals.append(user.get_as_dict())
        return totals


def load_from_dict(user_dict:dict) -> User:
    return User(user_dict["fname"], user_dict["lname"], user_dict["address"], user_dict["dAddress"], user_dict["customerType"])

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
        print(f"first name: {User.fname}, last name: {User.lname}, address: {User.address}, delivery address: {User.dAddress}, customer type: {User.customerType}")

def create_array_of_users():
    while True:
        fname = input("first name: ")
        lname = input("last name: ")
        address = input("address: ")
        dAddress = input("delevery address: ")
        customerType = input("customer type: ")

        new_user = User(
            fname,
            lname,
            address,
            dAddress,
            customerType
        )
    
        return new_user

while True:
    
    choice = int(input("1 = create user , 2 = save data 3 = deleat user, 4 = display all users : "))

    if choice == 1:
        new_user = create_array_of_users()
        local_array_of_users.append(new_user)

    elif choice == 2:
        dump_local_data()

    elif choice == 3:
        user_remove_fname = input("user first name: ")
        user_remove_lname = input("user last name: ")
        remove_user(user_remove_fname, user_remove_lname)
    
    elif choice == 4:
        diplay_all_users()

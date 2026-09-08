import json

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


def load_from_dict(user_dict:dict) -> dict:
    return User(user_dict["fname"], user_dict["lname"], user_dict["address"], user_dict["dAddress"], user_dict["customerType"])

def open_json_file():
    with open("users.json", "r") as fp:
        user_json = json.load(fp)
        uploaded_user_array = []
        for user_dict in user_json:
            uploaded_user_array.append(load_from_dict(user_dict))





def create_array_of_users():
    local_user_array = []
    while True:
        fname = input("first name: ")
        lname = input("last name: ")
        address = input("address: ")
        dAddress = input("delevery address: ")
        customerType = input("customer type: ")

        local_user_array.append({
            
            'fname': fname,
            'lname': lname,
            'address': address,
            'dAddress': dAddress,
            'customerType': customerType
            })
        
        status = str(input('break? y/n: '))
        if status == "y":
            return local_user_array
        break

def print_users(local_array_of_users):
    for user in local_array_of_users:
        print(user)

while True:
    choice = int(input("1 = create user , 2 = print dictonarys: "))

    if choice == 1:
        local_array_of_users = create_array_of_users()

    elif choice == 2:
        print_users(local_array_of_users)
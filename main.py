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


with open("users.json", "r") as fp:
    user_json = json.load(fp)
    user_array = []
    for user_dict in user_json:
        user_array.append(load_from_dict(user_dict))





def create_array_of_users():


import json


credentials_file = "data/ui_data/credentials.json"

def get_credentials(user):
    with open(credentials_file) as json_file:
        test_data = json.load(json_file)
        print(test_data)
        user_list = test_data[user]
    return user_list

def get_all_users():
    with open(credentials_file) as json_file:
        test_data = json.load(json_file)
    return list(test_data.values())

def get_all_credentials():
    with open(credentials_file) as json_file:
        test_data = json.load(json_file)
    return test_data

def get_data(file_name):
    data_file = f"data/ui_data/{file_name}.json"
    with open(data_file) as json_file:
        test_data = json.load(json_file)
    return test_data
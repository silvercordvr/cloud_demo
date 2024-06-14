# auth.py
import os

def read_users_from_file():
    users = {}
    file_path = os.path.join(os.path.dirname(__file__), 'users.txt')

    with open(file_path, 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users[username] = password
    return users

def check_auth_file(username, password):
    users = read_users_from_file()
    if username in users and users[username] == password:
        return True
    return False

# For DB in future
def check_auth_db(username, password):
    # Here will be a function for DB verification
    pass

def check_auth(username, password, use_db=False):
    if use_db:
        return check_auth_db(username, password)
    else:
        return check_auth_file(username, password)

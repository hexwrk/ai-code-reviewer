password = "super_secret_123"

def login(username):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return query

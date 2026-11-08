import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/1")

print("Status kodu:", response.status_code)
print("Cavab:", response.json())
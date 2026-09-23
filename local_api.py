import requests

r = requests.get("http://127.0.0.1:8000")

print(f"Status Code: {r.status_code}")
print(f"Result: {r.json()['message']}")


# Log in to get an access token
login_resp = requests.post(
    "http://127.0.0.1:8000/token",
    data={"username": "bob", "password": "testpassword123"},
)
token = login_resp.json()["access_token"]

data = {
    "age": 37,
    "workclass": "Private",
    "fnlgt": 178356,
    "education": "HS-grad",
    "education-num": 10,
    "marital-status": "Married-civ-spouse",
    "occupation": "Prof-specialty",
    "relationship": "Husband",
    "race": "White",
    "sex": "Male",
    "capital-gain": 0,
    "capital-loss": 0,
    "hours-per-week": 40,
    "native-country": "United-States",
}

r = requests.post(
    "http://127.0.0.1:8000/data/",
    headers={"Authorization": f"Bearer {token}"},
    json=data,
)

print(f"Status Code: {r.status_code}")
print(f"Result: {r.json()['result']}")

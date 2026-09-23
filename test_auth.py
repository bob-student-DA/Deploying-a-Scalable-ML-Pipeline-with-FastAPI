import requests

# Log in
r = requests.post(
    "http://127.0.0.1:8000/token",
    data={"username": "bob", "password": "testpassword123"},
)
print("Login status:", r.status_code)
token = r.json()["access_token"]
print("Token received.")

# Use token to call protected endpoint
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
print("Prediction status:", r.status_code)
print("Raw response:", r.text)
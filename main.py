import os
from datetime import datetime, timedelta

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

from ml.data import apply_label, process_data
from ml.model import inference, load_model

# --- Auth setup ---
SECRET_KEY = "a-demo-secret-key-change-this-in-real-production"
ALGO = "HS256"
TOKEN_EXPIRE_MIN = 30

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_db = {
    "bob": {
        "username": "bob",
        "hashed_pw": "$2b$12$jiVw6XUotgTfa0wcxgZ58e9YwdpSRhkAJAgjxzRP6DekWsJl4s.k.",
    }
}


def verify_pw(plain_pw, hashed_pw):
    return pwd_ctx.verify(plain_pw, hashed_pw)


def auth_user(username: str, password: str):
    user = users_db.get(username)
    if not user:
        return False
    if not verify_pw(password, user["hashed_pw"]):
        return False
    return user


def make_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MIN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)


def get_current_user(token: str = Depends(oauth2_scheme)):
    bad_creds = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        username: str = payload.get("sub")
        if username is None:
            raise bad_creds
    except JWTError:
        raise bad_creds
    user = users_db.get(username)
    if user is None:
        raise bad_creds
    return user


# DO NOT MODIFY
class Data(BaseModel):
    age: int = Field(..., example=37)
    workclass: str = Field(..., example="Private")
    fnlgt: int = Field(..., example=178356)
    education: str = Field(..., example="HS-grad")
    education_num: int = Field(..., example=10, alias="education-num")
    marital_status: str = Field(
        ..., example="Married-civ-spouse", alias="marital-status"
    )
    occupation: str = Field(..., example="Prof-specialty")
    relationship: str = Field(..., example="Husband")
    race: str = Field(..., example="White")
    sex: str = Field(..., example="Male")
    capital_gain: int = Field(..., example=0, alias="capital-gain")
    capital_loss: int = Field(..., example=0, alias="capital-loss")
    hours_per_week: int = Field(..., example=40, alias="hours-per-week")
    native_country: str = Field(
        ..., example="United-States", alias="native-country"
    )


path = os.path.join("model", "encoder.pkl")
encoder = load_model(path)

path = os.path.join("model", "model.pkl")
model = load_model(path)


app = FastAPI()


@app.get("/")
async def get_root():
    """ Say hello!"""
    return {"message": "Hello from the API!"}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = make_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/data/")
async def post_inference(
    data: Data, current_user: dict = Depends(get_current_user)
):
    # DO NOT MODIFY: turn the Pydantic model into a dict.
    data_dict = data.dict()
    # DO NOT MODIFY: clean up the dict to turn it into a Pandas DataFrame.
    # The data has names with hyphens and Python does not allow those
    # as variable names. Here it uses the functionality of
        # FastAPI/Pydantic/etc to deal with this.
    data = {k.replace("_", "-"): [v] for k, v in data_dict.items()}
    data = pd.DataFrame.from_dict(data)

    cat_features = [
        "workclass",
        "education",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "native-country",
    ]
    data_processed, _, _, _ = process_data(
        data,
        categorical_features=cat_features,
        label=None,
        training=False,
        encoder=encoder,
        lb=None,
    )
    _inference = inference(model, data_processed)
    return {"result": apply_label(_inference)}
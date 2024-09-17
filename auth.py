# authentication and authorization

from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "c2e3e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {}

app = FastAPI()

def get_password_hash(password):
  return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
    
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def decode_token(token:str):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid token")

# endpoint register
@app.post("/register/")
def register_user(username:str, password:str):
  if username in fake_users_db:
    raise HTTPException(status_code=400, detail="User already exists")
  # make new user
  fake_users_db[username] = {
    "username": username,
    "password": get_password_hash(password)
  }
  
  return {"message": "User created"}

# endpoint login
@app.post("/login/")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
  user_dict = fake_users_db.get(form_data.username)
  # check validation
  if user_dict is None or not verify_password(form_data.password, user_dict["password"]):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
  # access token
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data={"sub": user_dict["username"]}, expires_delta=access_token_expires)
  return {"access_token": access_token, "token_type": "bearer"}

# endpoint secure
@app.get("/secure/")
def secure_route(token: str = Depends(oauth2_scheme)):
    print(f"Token received: {token}")  # Debug statement
    user = decode_token(token)
    return {"message": f"Welcome, {user['sub']}!"}
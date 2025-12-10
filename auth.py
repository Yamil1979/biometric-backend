# routers/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from supabase_client import supabase
from config import JWT_SECRET

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

class RegisterIn(BaseModel):
    email: str
    password: str
    full_name: str | None = None

class LoginIn(BaseModel):
    email: str
    password: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return token

@router.post("/register")
def register(payload: RegisterIn):
    existing = supabase.table("user_profiles").select("*").eq("email", payload.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="User exists")
    hashed = pwd_context.hash(payload.password)
    res = supabase.table("user_profiles").insert({
        "email": payload.email,
        "password": hashed,
        "full_name": payload.full_name
    }).execute()
    if res.error:
        raise HTTPException(status_code=500, detail="Error creating user")
    token = create_access_token({"email": payload.email, "id": res.data[0]["id"]})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(payload: LoginIn):
    r = supabase.table("user_profiles").select("*").eq("email", payload.email).execute()
    if not r.data:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    user = r.data[0]
    if not pwd_context.verify(payload.password, user.get("password", "")):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"email": user["email"], "id": user["id"]})
    return {"access_token": token, "token_type": "bearer"}

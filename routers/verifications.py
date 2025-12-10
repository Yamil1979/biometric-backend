# routers/verifications.py
from fastapi import APIRouter, HTTPException
from supabase_client import supabase

router = APIRouter(prefix="/verifications", tags=["verifications"])

@router.post("/create")
def create_verification(payload: dict):
    r = supabase.table("verification_requests").insert(payload).execute()
    if r.error:
        raise HTTPException(status_code=500, detail="Insert failed")
    return r.data[0]

@router.get("/pending")
def pending():
    r = supabase.table("verification_requests").select("*").eq("status", "pending").execute()
    return r.data

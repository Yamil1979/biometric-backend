from fastapi import APIRouter
from supabase_client import supabase

router = APIRouter(prefix="/users")

@router.get("/{id}")
def get_user(id: str):
    return supabase.table("user_profiles").select("*").eq("id", id).execute()

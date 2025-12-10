from fastapi import APIRouter
from supabase_client import supabase

router = APIRouter()

@router.get("/")
def list_animals():
    return supabase.table("animals").select("*").execute().data

@router.post("/")
def create_animal(data: dict):
    return supabase.table("animals").insert(data).execute().data

@router.get("/{animal_id}")
def get_animal(animal_id: str):
    res = supabase.table("animals").select("*").eq("id", animal_id).single().execute()
    return res.data

from supabase_client import supabase
def create_animal(payload: dict):
    r = supabase.table("animales").insert(payload).execute()
    if r.error:
        return None
    return r.data[0]
def list_animals():
    r = supabase.table("animales").select("*").execute()
    if r.error:
        return []
    return r.data
def get_animal(animal_id: str):
    r = supabase.table("animales").select("*").eq("id", animal_id).maybe_single().execute()
    if r.error:
        return None
    return r.data

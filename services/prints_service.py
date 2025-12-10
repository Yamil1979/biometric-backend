from supabase_client import supabase
from services.biometrics_service import get_embedding
import uuid
def upload_image_to_storage(bucket: str, filename: str, image_bytes: bytes):
    res = supabase.storage.from_(bucket).upload(filename, image_bytes)
    if res.get("error"):
        return None
    public = supabase.storage.from_(bucket).get_public_url(filename)
    return public
def register_print(animal_id: str, image_bytes: bytes, registered_by: str | None = None, bucket: str = "nasal-prints"):
    filename = f"{animal_id}_{uuid.uuid4().hex}.jpg"
    public_url = upload_image_to_storage(bucket, filename, image_bytes)
    if not public_url:
        return None
    emb = get_embedding(image_bytes)
    data = {
        "animal_id": animal_id,
        "image_url": public_url,
        "embedding": emb
    }
    if registered_by:
        data["registered_by"] = registered_by
    r = supabase.table("nasal_prints").insert(data).execute()
    if r.error:
        return None
    return r.data[0]

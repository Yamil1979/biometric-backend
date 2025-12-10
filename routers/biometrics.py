from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from supabase_client import supabase
from utils.embeddings import generate_embedding
import uuid

router = APIRouter()

# -----------------------------
# INSCRIBIR HUELLA NASAL
# -----------------------------
@router.post("/enroll")
async def enroll_biometric(
    animal_id: str = Form(...),
    file: UploadFile = File(...)
):
    image_bytes = await file.read()

    # Generar embedding
    embedding = generate_embedding(image_bytes)
    if embedding is None:
        raise HTTPException(400, "No se pudo generar el embedding")

    # Subir imagen
    file_name = f"prints/{uuid.uuid4()}.jpg"
    supabase.storage.from_("animals").upload(file_name, image_bytes)
    image_url = supabase.storage.from_("animals").get_public_url(file_name)

    # Guardar en tabla nasal_prints
    data = {
        "animal_id": animal_id,
        "image_url": image_url,
        "embedding": embedding
    }

    result = supabase.table("nasal_prints").insert(data).execute()

    return {
        "status": "success",
        "image_url": image_url,
        "embedding_saved": True
    }

# -----------------------------
# VERIFICAR HUELLA NASAL
# -----------------------------
@router.post("/verify")
async def verify_biometric(
    file: UploadFile = File(...)
):
    image_bytes = await file.read()

    embedding = generate_embedding(image_bytes)
    if embedding is None:
        raise HTTPException(400, "No se pudo generar embedding")

    # Consulta vectorial usando pgvector
    query = supabase.rpc(
        "match_nasal_prints",
        {"query_embedding": embedding, "match_threshold": 0.80, "match_count": 1}
    ).execute()

    if not query.data:
        return {"match": False}

    match = query.data[0]

    return {
        "match": True,
        "animal_id": match.get("animal_id"),
        "distance": match.get("distance")
    }

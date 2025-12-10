from supabase_client import supabase
from services.biometrics_service import get_embedding
def rpc_match(embedding: list, threshold: float = 0.30, count: int = 5):
    r = supabase.rpc("match_nasal_prints", {"query_embedding": embedding, "match_threshold": threshold, "match_count": count}).execute()
    if r.error:
        return None
    return r.data
def verify_image(image_bytes: bytes, threshold: float = 0.30, count: int = 5):
    emb = get_embedding(image_bytes)
    if not emb:
        return {"match": False, "results": []}
    matches = rpc_match(emb, threshold, count)
    if not matches:
        return {"match": False, "results": []}
    results = []
    for m in matches:
        results.append({"animal_id": m.get("animal_id"), "distance": m.get("distance")})
    if len(results) == 0:
        return {"match": False, "results": []}
    return {"match": True, "results": results}
def log_match(request_id: str | None, animal_id: str | None, distance: float | None):
    data = {"request_id": request_id, "animal_id": animal_id, "distance": distance}
    supabase.table("match_logs").insert(data).execute()

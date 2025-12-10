from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.verify_service import verify_image, log_match
router = APIRouter()
@router.post("/compare")
async def compare_print(file: UploadFile = File(...), match_threshold: float = Form(0.30), match_count: int = Form(5)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="file must be image")
    image_bytes = await file.read()
    res = verify_image(image_bytes, match_threshold, match_count)
    if res.get("match"):
        first = res["results"][0]
        log_match(None, first.get("animal_id"), first.get("distance"))
    return res

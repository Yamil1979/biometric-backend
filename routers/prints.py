from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.prints_service import register_print
router = APIRouter()
@router.post("/register")
async def register_print_endpoint(animal_id: str = Form(...), file: UploadFile = File(...), registered_by: str | None = Form(None)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="file must be image")
    image_bytes = await file.read()
    res = register_print(animal_id, image_bytes, registered_by)
    if not res:
        raise HTTPException(status_code=500, detail="failed to register print")
    return {"status": "ok", "data": res}

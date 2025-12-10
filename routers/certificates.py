from fastapi import APIRouter, HTTPException, Depends
from models.schemas import CertificateIn, CertificateOut
from services.pdf_service import issue_certificate
from services.animals_service import get_animal
router = APIRouter()

@router.post("/issue", response_model=CertificateOut)
def issue_certificate_endpoint(payload: CertificateIn):
    animal = get_animal(payload.animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="animal not found")
    res = issue_certificate(animal, payload.tipo, payload.metadata)
    if not res:
        raise HTTPException(status_code=500, detail="failed to issue certificate")
    return {
        "id": res.get("id"),
        "animal_id": res.get("animal_id"),
        "tipo": res.get("tipo"),
        "qr_hash": res.get("qr_hash"),
        "url_pdf": res.get("url_pdf"),
        "fecha_emision": res.get("fecha_emision"),
        "activo": res.get("activo")
    }

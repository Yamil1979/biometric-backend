from pydantic import BaseModel
from typing import Optional, List

class AnimalIn(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[int] = None
    sexo: Optional[str] = None
    color: Optional[str] = None
    senas_particulares: Optional[str] = None
    propietario_actual: Optional[str] = None

class AnimalOut(AnimalIn):
    id: str
    fecha_registro: Optional[str] = None

class RegisterPrintIn(BaseModel):
    animal_id: str

class VerifyIn(BaseModel):
    threshold: Optional[float] = 0.30
    count: Optional[int] = 5

class MatchResult(BaseModel):
    animal_id: Optional[str]
    distance: Optional[float]

class VerifyOut(BaseModel):
    match: bool
    results: List[MatchResult]

class CertificateIn(BaseModel):
    animal_id: str
    tipo: Optional[str] = "identidad"
    metadata: Optional[dict] = None

class CertificateOut(BaseModel):
    id: str
    animal_id: str
    tipo: str
    qr_hash: str
    url_pdf: str
    fecha_emision: Optional[str] = None
    activo: bool

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from routers.animals import router as animals_router
from routers.prints import router as prints_router
from routers.verify import router as verify_router
from routers.verifications import router as verifications_router
from routers.biometrics import router as biometrics_router

# Detecta si está corriendo en Railway
ENV = os.getenv("RAILWAY_ENVIRONMENT", "local")

app = FastAPI(
    title="Animal Biometrics API",
    description="API para registro y verificación de huellas nasales de animales.",
    version="1.0.0"
)

# CORS flexible (Flutter necesita wildcard completo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringir luego si quieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(animals_router, prefix="/animals", tags=["Animales"])
app.include_router(prints_router, prefix="/prints", tags=["Huellas Nasales"])
app.include_router(verify_router, prefix="/verify", tags=["Verificación"])
app.include_router(verifications_router, prefix="/verifications", tags=["Solicitudes"])
app.include_router(biometrics_router, prefix="/biometrics", tags=["Biometría"])

# Ruta principal
@app.get("/")
def root():
    return {
        "status": "OK",
        "environment": ENV,
        "message": "Animal Biometrics API funcionando correctamente en Railway." if ENV != "local" else "API funcionando en entorno local."
    }

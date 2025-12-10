# utils/embeddings.py
import numpy as np
from PIL import Image
import io

def generate_embedding(image_bytes: bytes) -> list:
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("L")
        img = img.resize((64, 64))
        arr = np.array(img).astype(np.float32).flatten()
        vec = np.interp(
            np.linspace(0, len(arr)-1, 256),
            np.arange(len(arr)),
            arr
        )
        vec = vec / 255.0
        # normalizar
        norm = np.linalg.norm(vec)
        if norm == 0:
            return (vec).tolist()
        vec = vec / norm
        return vec.tolist()
    except Exception:
        return None

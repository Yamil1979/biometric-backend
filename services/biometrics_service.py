from pathlib import Path
import numpy as np
from PIL import Image
import io
from utils.embeddings import generate_embedding as fallback_embedding
try:
    from transformers import CLIPProcessor, CLIPModel
    import torch
    _has_clip = True
except Exception:
    _has_clip = False
_model = None
_processor = None
def _load_clip(model_name: str = "openai/clip-vit-base-patch32"):
    global _model, _processor
    if _model is None and _has_clip:
        _model = CLIPModel.from_pretrained(model_name)
        _processor = CLIPProcessor.from_pretrained(model_name)
        if torch.cuda.is_available():
            _model = _model.to("cuda")
def _clip_embedding(image_bytes: bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = _processor(images=img, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}
    with torch.no_grad():
        out = _model.get_image_features(**inputs)
    vec = out[0].cpu().numpy()
    return vec.flatten().astype(float)
def _resample_vector(vec: np.ndarray, target_dim: int = 256):
    vec = np.asarray(vec, dtype=float)
    if vec.size == target_dim:
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec.tolist()
        return (vec / norm).tolist()
    idx_old = np.linspace(0, len(vec) - 1, len(vec))
    idx_new = np.linspace(0, len(vec) - 1, target_dim)
    vec_resampled = np.interp(idx_new, idx_old, vec)
    norm = np.linalg.norm(vec_resampled)
    if norm == 0:
        return vec_resampled.tolist()
    return (vec_resampled / norm).tolist()
def get_embedding(image_bytes: bytes, use_clip: bool = True, clip_model_name: str = "openai/clip-vit-base-patch32") -> list:
    if use_clip and _has_clip:
        try:
            _load_clip(clip_model_name)
            vec = _clip_embedding(image_bytes)
            return _resample_vector(vec, 256)
        except Exception:
            emb = fallback_embedding(image_bytes)
            return emb
    emb = fallback_embedding(image_bytes)
    return emb

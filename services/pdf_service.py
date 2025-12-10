import io
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from supabase_client import supabase
from datetime import datetime
import uuid
from PIL import Image

def _generate_qr_image(data: str, size: int = 300) -> bytes:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = io.BytesIO()
    img = img.resize((size, size))
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()

def _create_pdf_bytes(animal: dict, qr_bytes: bytes, tipo: str, metadata: dict | None) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    title = f"CERTIFICADO - {tipo.upper()}"
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-80, title)
    c.setFont("Helvetica", 12)
    lines = [
        f"ID Animal: {animal.get('id')}",
        f"Nombre: {animal.get('nombre')}",
        f"Especie: {animal.get('especie')}",
        f"Raza: {animal.get('raza') or ''}",
        f"Sexo: {animal.get('sexo') or ''}",
        f"Color: {animal.get('color') or ''}",
        f"Propietario actual: {animal.get('propietario_actual') or ''}",
        f"Fecha emisión: {datetime.utcnow().isoformat()} UTC"
    ]
    y = height - 120
    for ln in lines:
        c.drawString(60, y, ln)
        y -= 20
    if metadata:
        c.drawString(60, y-10, "Metadata:")
        y -= 30
        for k, v in metadata.items():
            c.drawString(80, y, f"{k}: {v}")
            y -= 18
    qr_img = ImageReader(io.BytesIO(qr_bytes))
    qr_size = 160
    c.drawImage(qr_img, width - qr_size - 60, 120, qr_size, qr_size)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()

def upload_pdf_to_storage(bucket: str, filename: str, pdf_bytes: bytes):
    res = supabase.storage.from_(bucket).upload(filename, pdf_bytes, {"content-type":"application/pdf"})
    if res.get("error"):
        return None
    public = supabase.storage.from_(bucket).get_public_url(filename)
    return public

def issue_certificate(animal: dict, tipo: str = "identidad", metadata: dict | None = None, bucket: str = "certificados"):
    qr_payload = {"animal_id": animal.get("id"), "tipo": tipo, "issued_at": datetime.utcnow().isoformat()}
    qr_hash = uuid.uuid5(uuid.NAMESPACE_URL, str(qr_payload)).hex
    qr_bytes = _generate_qr_image(qr_hash)
    pdf_bytes = _create_pdf_bytes(animal, qr_bytes, tipo, metadata)
    filename = f"certificate_{animal.get('id')}_{qr_hash}.pdf"
    public_url = upload_pdf_to_storage(bucket, filename, pdf_bytes)
    if not public_url:
        return None
    data = {
        "animal_id": animal.get("id"),
        "tipo": tipo,
        "qr_hash": qr_hash,
        "url_pdf": public_url,
        "fecha_emision": datetime.utcnow().isoformat(),
        "activo": True
    }
    r = supabase.table("certificados").insert(data).execute()
    if r.error:
        return None
    return r.data[0]

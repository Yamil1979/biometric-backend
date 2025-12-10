from PIL import Image
import io

def load_image(image_file):
    contents = image_file.file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    return img, contents

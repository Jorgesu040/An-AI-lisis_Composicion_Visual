import base64

def encode_image(image_path):
    """
    Codifica un archivo de imagen a una cadena base64.
    """
    with open(image_path, "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode('utf-8')
    return image
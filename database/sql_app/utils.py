import uuid

def generate_random_filename(extension: str) -> str:
    unique_filename = str(uuid.uuid4())
    return f"{unique_filename}.{extension}"
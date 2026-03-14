import os
from src.upload_handler import allowed_file

def scan_repository(path):
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            files.append(str(os.path.join(root, filename)))
    return files

def save_uploaded_file(path, content):
    """
    Test-friendly wrapper: save raw bytes to a given path.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(content)
    return str(path)

def scan_repository_top_files(path, top_n=5):
    """
    Return metadata for the top N files in a repository.
    For simplicity, just take the first N files found.
    """
    files = scan_repository(path)
    top_files = []
    for f in files[:top_n]:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
        except Exception:
            content = ""
        top_files.append({"filename": os.path.basename(f), "content": content})
    return top_files

def score_file(file_data):
    """
    Very basic scoring function.
    For now, score by length of content.
    """
    content = file_data.get("content", "")
    return len(content)

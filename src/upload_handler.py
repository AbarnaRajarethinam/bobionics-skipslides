import os
import uuid
import zipfile
from werkzeug.utils import secure_filename

# ------------------------------
# Project folders
# ------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "uploads")
EXTRACT_FOLDER = os.path.join(PROJECT_ROOT, "extracted")

ALLOWED_EXTENSIONS = {
    "zip", "py", "ipynb", "js", "md", "txt", "json", "yaml", "yml", "csv"
}

# ------------------------------
# Helpers
# ------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def create_project_folder():
    project_id = str(uuid.uuid4())
    path = os.path.join(EXTRACT_FOLDER, project_id)
    os.makedirs(path, exist_ok=True)
    return path

# ------------------------------
# Save uploaded file
# ------------------------------
def save_uploaded_file(file):
    if not allowed_file(file.filename):
        raise ValueError("File type not allowed")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    print(f"[Upload Handler] File saved: {filepath}")
    return filepath

# ------------------------------
# Extract ZIP
# ------------------------------
def extract_zip(filepath):
    project_path = create_project_folder()
    print(f"[Upload Handler] Extracting ZIP to: {project_path}")

    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(project_path)

    print(f"[Upload Handler] Extraction complete")
    return project_path

# ------------------------------
# Normalize single file
# ------------------------------
def normalize_single_file(filepath):
    project_path = create_project_folder()
    filename = os.path.basename(filepath)
    new_path = os.path.join(project_path, filename)
    os.rename(filepath, new_path)

    print(f"[Upload Handler] Single file moved to: {new_path}")
    return project_path

import os
import uuid
import zipfile
from werkzeug.utils import secure_filename

# ------------------------------
# Make folders relative to project root
# ------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "uploads")
EXTRACT_FOLDER = os.path.join(PROJECT_ROOT, "extracted")

ALLOWED_EXTENSIONS = {
    "zip",
    "py",
    "ipynb",
    "js",
    "md",
    "txt",
    "json",
    "yaml",
    "yml",
    "csv"
}

# ------------------------------
# Check if file type is allowed
# ------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------------------
# Create a new project folder in extracted/
# ------------------------------
def create_project_folder():
    project_id = str(uuid.uuid4())
    path = os.path.join(EXTRACT_FOLDER, project_id)
    os.makedirs(path, exist_ok=True)
    return path

# ------------------------------
# Save uploaded file to uploads/
# ------------------------------
def save_uploaded_file(file):

    if not allowed_file(file.filename):
        raise ValueError("File type not allowed")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    return filepath

# ------------------------------
# Extract a ZIP into extracted/project_id/
# ------------------------------
def extract_zip(filepath):

    project_path = create_project_folder()

    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(project_path)

    return project_path

# ------------------------------
# Move a single file into a project folder
# ------------------------------
def normalize_single_file(filepath):

    project_path = create_project_folder()

    filename = os.path.basename(filepath)
    new_path = os.path.join(project_path, filename)

    os.rename(filepath, new_path)

    return project_path

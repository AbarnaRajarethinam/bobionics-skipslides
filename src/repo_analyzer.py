import os

# ------------------------------
# Constants
# ------------------------------
IGNORED_FOLDERS = {
    "venv",
    "node_modules",
    "__pycache__",
    ".git",
    "dist",
    "build"
}

ALLOWED_FILES = {
    ".py",
    ".ipynb",
    ".js",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml"
}

# ------------------------------
# Scan project folder and return allowed files
# ------------------------------
def scan_repository(project_path):

    file_list = []

    for root, dirs, files in os.walk(project_path):

        # remove ignored folders
        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]

        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in ALLOWED_FILES:
                file_path = os.path.join(root, file)
                file_list.append(file_path)

    return file_list

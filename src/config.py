UPLOAD_FOLDER = "uploads"
EXTRACT_FOLDER = "extracted"

MAX_UPLOAD_SIZE = 50 * 1024 * 1024

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

IGNORED_FOLDERS = {
    "venv",
    "node_modules",
    "__pycache__",
    ".git",
    "dist",
    "build"
}

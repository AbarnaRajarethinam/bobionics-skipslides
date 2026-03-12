import os
from src.utils import read_file

IGNORED_FOLDERS = {
    "venv",
    "__pycache__",
    ".git",
    ".pytest_cache",

    # JS / Web
    "node_modules",
    ".next",
    "dist",
    "build",
    "coverage",

    # Python environments
    "env",
    ".venv",

    # misc
    ".idea",
    ".vscode",
    "logs"
}

TOP_N_FILES = 10  # number of important files to keep
CONTENT_PREVIEW_LEN = 120  # how many chars to show in terminal preview


def score_file(file_path, project_path):
    score = 0

    filename = os.path.basename(file_path).lower()
    ext = os.path.splitext(filename)[1]
    relative_path = os.path.relpath(file_path, project_path).lower()

    # ------------------------------
    # Documentation
    # ------------------------------
    if filename == "readme.md":
        score += 120

    if filename.startswith("readme"):
        score += 100

    if "docs" in relative_path:
        score += 40

    # ------------------------------
    # Dependency / config files
    # ------------------------------
    if filename in {
        "requirements.txt",
        "environment.yml",
        "pyproject.toml",
        "package.json"
    }:
        score += 80

    if filename.endswith((".yaml", ".yml", ".json")):
        score += 20

    # ------------------------------
    # Entry points
    # ------------------------------
    if filename in {"main.py", "app.py", "run.py", "server.py"}:
        score += 70

    # ------------------------------
    # ML / model related
    # ------------------------------
    if any(word in filename for word in ["model", "train", "predict", "inference"]):
        score += 60

    if "model" in relative_path or "training" in relative_path:
        score += 40

    # ------------------------------
    # Notebooks
    # ------------------------------
    if ext == ".ipynb":
        score += 50

    # ------------------------------
    # Source code priority
    # ------------------------------
    if ext == ".py":
        score += 25

    if ext in {".js", ".ts"}:
        score += 20

    # ------------------------------
    # Root level importance
    # ------------------------------
    if "/" not in relative_path and "\\" not in relative_path:
        score += 30

    # ------------------------------
    # Architecture / pipeline hints
    # ------------------------------
    if "pipeline" in filename or "workflow" in filename:
        score += 40

    if "api" in filename:
        score += 30

    return score


def scan_repository(project_path):
    """
    Walk through repo and return top N important files (with paths)
    Also print scores and content previews for all files to terminal.
    """
    scored_files = []

    print(f"[Repo Analyzer] Scanning repository: {project_path}\n")

    all_files = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]

        for i, file in enumerate(files, start=1):
            file_path = os.path.join(root, file)
            score = score_file(file_path, project_path)
            scored_files.append((score, file_path))
            all_files.append((score, file_path))
            print(f"[Repo Analyzer] ({i}) Processing: {file_path} | Score: {score}")

    # Sort by score descending
    scored_files.sort(reverse=True)

    # Select top N files
    top_files = scored_files[:TOP_N_FILES]

    # Print top files
    print("\n[Repo Analyzer] =====================")
    print(f"[Repo Analyzer] Top {len(top_files)} files selected:")
    for rank, (score, path) in enumerate(top_files, start=1):
        try:
            content = read_file(path)
            preview = content[:CONTENT_PREVIEW_LEN].replace("\n", "\\n")
        except Exception:
            preview = "<Unable to read content>"

        print(f"\n[{rank}] {os.path.relpath(path, project_path)} | Score: {score}")
        print(f"Preview: {preview} ...")

    # Print files NOT selected (score=0 or below top N)
    print("\n[Repo Analyzer] Other files (not selected in top files):")
    for score, path in all_files:
        if (score, path) not in top_files:
            try:
                content = read_file(path)
                preview = content[:CONTENT_PREVIEW_LEN].replace("\n", "\\n")
            except Exception:
                preview = "<Unable to read content>"
            print(f"\n[0] {os.path.relpath(path, project_path)} | Score: {score}")
            print(f"Preview: {preview} ...")

    print("\n[Repo Analyzer] =====================\n")

    # Return only the top file paths for the AI pipeline
    return [file_path for score, file_path in top_files]


def extract_file_contents(files):
    """
    Given a list of file paths, read their contents and return
    a structured list suitable for AI analysis.
    """
    structured_files = []

    for file_path in files:
        try:
            content = read_file(file_path)
        except Exception:
            content = ""
        structured_files.append({
            "filename": os.path.basename(file_path),
            "content": content
        })

    return structured_files

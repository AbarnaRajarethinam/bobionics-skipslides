import os


IGNORED_FOLDERS = {
    "venv",
    "node_modules",
    "__pycache__",
    ".git",
    "dist",
    "build",
    ".pytest_cache"
}


TOP_N_FILES = 10


def score_file(file_path, project_path):
    score = 0
    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1]

    relative_path = os.path.relpath(file_path, project_path)

    # Important filenames
    if filename.lower() == "readme.md":
        score += 100

    if filename.lower() == "requirements.txt":
        score += 80

    if filename.lower() in {"main.py", "app.py"}:
        score += 70

    if filename.lower() in {"dockerfile", "docker-compose.yml"}:
        score += 60

    # Root level files
    if "/" not in relative_path and "\\" not in relative_path:
        score += 30

    # Extension scoring
    if ext == ".ipynb":
        score += 25

    if ext == ".py":
        score += 20

    if ext in {".js", ".ts"}:
        score += 15

    # Folder signals
    if "src" in relative_path:
        score += 10

    if "model" in relative_path:
        score += 10

    return score


def scan_repository(project_path):

    scored_files = []

    for root, dirs, files in os.walk(project_path):

        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]

        for file in files:

            file_path = os.path.join(root, file)

            score = score_file(file_path, project_path)

            if score > 0:
                scored_files.append((score, file_path))

    # sort by score descending
    scored_files.sort(reverse=True)

    # select top N
    top_files = [file for score, file in scored_files[:TOP_N_FILES]]

    print(f"Top {len(top_files)} important files selected")

    return top_files
import os
from flask import Flask, request, jsonify, render_template

from upload_handler import (
    save_uploaded_file,
    extract_zip,
    normalize_single_file
)

from repo_analyzer import scan_repository, extract_file_contents
from config import MAX_UPLOAD_SIZE

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    try:
        # Save uploaded file
        filepath = save_uploaded_file(file)
        print(f"[App] Uploaded file saved at: {filepath}")

        # Extract zip or normalize single file
        if filepath.endswith(".zip"):
            project_path = extract_zip(filepath)
        else:
            project_path = normalize_single_file(filepath)

        print(f"[App] Project path ready: {project_path}")

        # Scan repository and select top files
        files = scan_repository(project_path)

        # Extract file contents and structure for AI
        file_contents = extract_file_contents(files)

        print(f"[App] Upload processing complete. {len(file_contents)} files selected.")

        return jsonify({
            "message": "Upload successful",
            "project_path": project_path,
            "files": file_contents
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

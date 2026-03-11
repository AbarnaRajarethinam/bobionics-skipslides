import os
from flask import Flask, request, jsonify, render_template

from upload_handler import (
    save_uploaded_file,
    extract_zip,
    normalize_single_file
)

from repo_analyzer import scan_repository
from config import MAX_UPLOAD_SIZE


app = Flask(
    __name__,
    template_folder="../frontend/templates"
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

        filepath = save_uploaded_file(file)

        if filepath.endswith(".zip"):

            project_path = extract_zip(filepath)

        else:

            project_path = normalize_single_file(filepath)

        files = scan_repository(project_path)

        return jsonify({
            "message": "Upload successful",
            "project_path": project_path,
            "files_found": files
        })

    except Exception as e:

        return jsonify({"error": str(e)}), 500

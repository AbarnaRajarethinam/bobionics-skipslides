import os
from flask import Flask, request, send_file, render_template

from slide_generator import create_slides_from_ai

from upload_handler import (
    save_uploaded_file,
    extract_zip,
    normalize_single_file
)

from repo_analyzer import scan_repository, extract_file_contents
from ai_analyzer import analyze_repository

from config import MAX_UPLOAD_SIZE


# -----------------------------
# Flask setup
# -----------------------------
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE


# -----------------------------
# Homepage
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# Upload endpoint
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    try:

        # -----------------------------
        # Save uploaded file
        # -----------------------------
        filepath = save_uploaded_file(file)
        print(f"[App] Uploaded file saved at: {filepath}")

        # -----------------------------
        # Extract ZIP or normalize
        # -----------------------------
        if filepath.endswith(".zip"):
            project_path = extract_zip(filepath)
        else:
            project_path = normalize_single_file(filepath)

        print(f"[App] Project path ready: {project_path}")

        # -----------------------------
        # Scan repository
        # -----------------------------
        files = scan_repository(project_path)

        # -----------------------------
        # Extract file contents
        # -----------------------------
        file_contents = extract_file_contents(files)

        print(f"[App] {len(file_contents)} files prepared for AI analysis")

        # -----------------------------
        # AI analysis
        # -----------------------------
        explanation = analyze_repository(file_contents)

        print("[App] AI explanation generated")

        # -----------------------------
        # Generate slides
        # -----------------------------
        project_name = os.path.basename(project_path)

        ppt_stream = create_slides_from_ai(
            explanation,
            project_name=project_name
        )

        print("[App] Slides generated successfully")

        # -----------------------------
        # Send PPT to browser
        # -----------------------------
        return send_file(
            ppt_stream,
            as_attachment=True,
            download_name=f"{project_name}_slides.pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

    except Exception as e:
        print("[App ERROR]", str(e))
        return str(e), 500


# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
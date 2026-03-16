import os
import re
from pptx import Presentation
from pptx.util import Inches

# Folder to store generated slides
OUTPUT_FOLDER = "generated_slides"


def parse_ai_slides(ai_text):
    """
    Convert AI explanation text into structured slides.
    Looks for [SLIDE: Title] tags and bullet points.
    """

    slides = []

    pattern = r"\[SLIDE:\s*(.*?)\](.*?)(?=\[SLIDE:|\Z)"
    matches = re.findall(pattern, ai_text, re.S)

    for title, content in matches:
        bullets = []

        for line in content.splitlines():
            line = line.strip()

            if line.startswith("•"):
                bullets.append(line.replace("•", "").strip())

        slides.append({
            "title": title.strip(),
            "bullets": bullets
        })

    return slides


def generate_ppt(slides, filename="project_slides.pptx"):
    """
    Generate PowerPoint slides from structured slide data.
    """

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    prs = Presentation()

    # Limit slides to 7 (recommended presentation size)
    slides = slides[:7]

    for slide_data in slides:

        layout = prs.slide_layouts[1]  # Title + Content
        slide = prs.slides.add_slide(layout)

        title = slide.shapes.title
        content = slide.placeholders[1]

        title.text = slide_data["title"]

        tf = content.text_frame
        tf.clear()

        for i, bullet in enumerate(slide_data["bullets"]):

            if i == 0:
                tf.text = bullet
            else:
                p = tf.add_paragraph()
                p.text = bullet
                p.level = 0

    filepath = os.path.join(OUTPUT_FOLDER, filename)

    prs.save(filepath)

    print(f"[Slide Generator] Slides saved at: {filepath}")

    return filepath


def create_slides_from_ai(ai_text):
    """
    Full pipeline:
    AI text → structured slides → PPT file
    """

    slides = parse_ai_slides(ai_text)

    if not slides:
        raise ValueError("No slides detected in AI output")

    ppt_path = generate_ppt(slides)

    return ppt_path
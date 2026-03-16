import re
from io import BytesIO

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

MAX_BULLETS = 5
MAX_CODE_LINES = 10
MAX_CODE_LINE_LENGTH = 55
MAX_DIAGRAM_STEPS = 6


# COLORS
BG_COLOR = RGBColor(12, 12, 18)
TITLE_BAR = RGBColor(25, 140, 255)
BULLET_COLOR = RGBColor(230, 230, 230)

CODE_BG = RGBColor(15, 15, 15)
CODE_TEXT = RGBColor(0, 255, 120)

DIAGRAM_BOX = RGBColor(60, 160, 255)
DIAGRAM_TEXT = RGBColor(255, 255, 255)


# -------------------------
# PARSE AI OUTPUT
# -------------------------
def parse_ai_slides(ai_text):

    slides = []

    slide_pattern = r"\[SLIDE:\s*(.*?)\](.*?)(?=\[SLIDE:|\Z)"
    matches = re.findall(slide_pattern, ai_text, re.S)

    for title, content in matches:

        bullets = []
        codes = []
        diagrams = []

        codes = re.findall(r"\[CODE\](.*?)\[/CODE\]", content, re.S)
        diagrams = re.findall(r"\[DIAGRAM\](.*?)\[/DIAGRAM\]", content, re.S)

        for line in content.splitlines():
            line = line.strip()
            if line.startswith("•"):
                bullets.append(line.replace("•", "").strip())

        slides.append({
            "title": title.strip(),
            "bullets": bullets[:MAX_BULLETS],
            "code": [c.strip() for c in codes],
            "diagram": [d.strip() for d in diagrams]
        })

    return slides


# -------------------------
# BACKGROUND
# -------------------------
def add_background(slide, prs):

    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        prs.slide_width,
        prs.slide_height
    )

    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR
    bg.line.fill.background()


# -------------------------
# TITLE
# -------------------------
def add_title(slide, title, prs):

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        prs.slide_width,
        Inches(1)
    )

    fill = bar.fill
    fill.solid()
    fill.fore_color.rgb = TITLE_BAR
    bar.line.fill.background()

    title_box = slide.shapes.add_textbox(
        Inches(0.5),
        Inches(0.2),
        prs.slide_width - Inches(1),
        Inches(0.7)
    )

    tf = title_box.text_frame
    tf.text = title

    p = tf.paragraphs[0]
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)


# -------------------------
# BULLETS
# -------------------------
def add_bullets(slide, bullets):

    box = slide.shapes.add_textbox(
        Inches(0.7),
        Inches(1.3),
        Inches(5.3),
        Inches(3.8)
    )

    tf = box.text_frame
    tf.word_wrap = True

    if not bullets:
        return

    tf.text = bullets[0]

    p = tf.paragraphs[0]
    p.level = 0
    p.font.size = Pt(22)
    p.font.color.rgb = BULLET_COLOR

    for bullet in bullets[1:]:

        p = tf.add_paragraph()
        p.text = bullet
        p.level = 0
        p.font.size = Pt(22)
        p.font.color.rgb = BULLET_COLOR


# -------------------------
# CODE BLOCK
# -------------------------
def add_code_block(slide, code):

    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.2),
        Inches(1.3),
        Inches(6.4),
        Inches(3.8)
    )

    fill = box.fill
    fill.solid()
    fill.fore_color.rgb = CODE_BG

    box.line.color.rgb = RGBColor(0, 255, 120)

    tf = box.text_frame
    tf.word_wrap = False

    lines = code.split("\n")[:MAX_CODE_LINES]

    lines = [
        line[:MAX_CODE_LINE_LENGTH] + ("…" if len(line) > MAX_CODE_LINE_LENGTH else "")
        for line in lines
    ]

    tf.text = lines[0] if lines else ""

    for line in lines[1:]:
        p = tf.add_paragraph()
        p.text = line

    for p in tf.paragraphs:
        p.font.name = "Courier New"
        p.font.size = Pt(16)
        p.font.color.rgb = CODE_TEXT


# -------------------------
# HORIZONTAL DIAGRAM
# -------------------------
def add_diagram(slide, diagram_text):

    steps = [s.strip() for s in diagram_text.split("→")][:MAX_DIAGRAM_STEPS]

    step_width = Inches(1.8)
    step_height = Inches(0.8)
    spacing = Inches(0.5)

    start_x = Inches(0.7)
    top = Inches(5.3)

    for i, step in enumerate(steps):

        left = start_x + i * (step_width + spacing)

        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left,
            top,
            step_width,
            step_height
        )

        fill = box.fill
        fill.solid()
        fill.fore_color.rgb = DIAGRAM_BOX

        box.line.color.rgb = RGBColor(0, 255, 200)

        tf = box.text_frame
        tf.text = step

        p = tf.paragraphs[0]
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = DIAGRAM_TEXT

        # Add arrow between boxes
        if i < len(steps) - 1:

            arrow_box = slide.shapes.add_textbox(
                left + step_width,
                top + Inches(0.25),
                spacing,
                Inches(0.5)
            )

            arrow_tf = arrow_box.text_frame
            arrow_tf.text = "→"

            arrow_p = arrow_tf.paragraphs[0]
            arrow_p.font.size = Pt(24)
            arrow_p.font.bold = True
            arrow_p.font.color.rgb = RGBColor(0, 255, 200)


# -------------------------
# GENERATE PPT
# -------------------------
def generate_ppt(slides):

    prs = Presentation()

    for slide_data in slides:

        slide = prs.slides.add_slide(prs.slide_layouts[6])

        add_background(slide, prs)
        add_title(slide, slide_data["title"], prs)

        add_bullets(slide, slide_data["bullets"])

        if slide_data["code"]:
            add_code_block(slide, slide_data["code"][0])

        if slide_data["diagram"]:
            add_diagram(slide, slide_data["diagram"][0])

    ppt_stream = BytesIO()

    prs.save(ppt_stream)
    ppt_stream.seek(0)

    return ppt_stream


# -------------------------
# ENTRY FUNCTION
# -------------------------
def create_slides_from_ai(ai_text, project_name="project"):

    slides = parse_ai_slides(ai_text)

    if not slides:
        raise ValueError("No slides detected")

    return generate_ppt(slides)
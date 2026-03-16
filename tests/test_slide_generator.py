from src.slide_generator import parse_ai_slides, generate_ppt
import os


def test_parse_ai_slides():
    ai_text = """
    [SLIDE: Project Overview]
    • AI tool for generating slides
    • Uses OpenAI API
    • Built with Flask
    • Supports ZIP uploads

    [SLIDE: Key Features]
    • Upload repository
    • Analyze code
    • Generate slides
    • Export PowerPoint
    """

    slides = parse_ai_slides(ai_text)

    assert len(slides) == 2
    assert slides[0]["title"] == "Project Overview"
    assert "AI tool for generating slides" in slides[0]["bullets"]


def test_generate_ppt(tmp_path):
    slides = [
        {
            "title": "Test Slide",
            "bullets": [
                "Bullet one",
                "Bullet two",
                "Bullet three",
                "Bullet four"
            ]
        }
    ]

    filename = tmp_path / "test_slides.pptx"

    path = generate_ppt(slides, filename=str(filename))

    assert os.path.exists(path)
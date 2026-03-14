import pytest
from unittest.mock import patch, MagicMock

from src.ai_analyzer import build_prompt, analyze_repository


# ----------------------------------------
# Test build_prompt
# ----------------------------------------
def test_build_prompt_basic():
    files = [
        {"filename": "main.py", "content": "print('hello world')"},
        {"filename": "utils.py", "content": "def helper(): pass"}
    ]

    prompt = build_prompt(files)

    assert "FILE: main.py" in prompt
    assert "FILE: utils.py" in prompt
    assert "print('hello world')" in prompt
    assert "def helper()" in prompt


# ----------------------------------------
# Test build_prompt truncation
# ----------------------------------------
def test_build_prompt_truncates_large_files():
    long_content = "a" * 5000

    files = [{"filename": "large.py", "content": long_content}]

    prompt = build_prompt(files)

    # Should truncate to 2000 characters
    assert "a" * 2000 in prompt
    assert "a" * 3000 not in prompt


# ----------------------------------------
# Test analyze_repository with mocked OpenAI
# ----------------------------------------
@patch("src.ai_analyzer.client")
def test_analyze_repository(mock_client):

    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content="[SLIDE: Project Overview]\n• Example bullet"
            )
        )
    ]

    mock_client.chat.completions.create.return_value = mock_response

    files = [{"filename": "main.py", "content": "print('hello')"}]

    result = analyze_repository(files)

    assert "[SLIDE:" in result
    assert "Example bullet" in result


# ----------------------------------------
# Ensure OpenAI API was called correctly
# ----------------------------------------
@patch("src.ai_analyzer.client")
def test_openai_called(mock_client):

    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="test output"))
    ]

    mock_client.chat.completions.create.return_value = mock_response

    files = [{"filename": "file.py", "content": "x=1"}]

    analyze_repository(files)

    mock_client.chat.completions.create.assert_called_once()


# ----------------------------------------
# Test empty file list
# ----------------------------------------
def test_build_prompt_empty_files():

    prompt = build_prompt([])

    assert "Repository files:" in prompt
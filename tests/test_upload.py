from src.upload_handler import allowed_file

def test_allowed_file():
    assert allowed_file("test.py") == True
    assert allowed_file("notebook.ipynb") == True
    assert allowed_file("project.zip") == True
    assert allowed_file("image.png") == False

from src.repo_analyzer import scan_repository

def test_scan_repository(tmp_path):

    file1 = tmp_path / "main.py"
    file1.write_text("print('hello')")

    file2 = tmp_path / "README.md"
    file2.write_text("project")

    files = scan_repository(tmp_path)

    assert len(files) == 2
    assert str(file1) in files
    assert str(file2) in files

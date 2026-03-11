def read_file(filepath):

    try:

        with open(filepath, "r", encoding="utf-8") as f:

            return f.read()

    except Exception:

        return ""

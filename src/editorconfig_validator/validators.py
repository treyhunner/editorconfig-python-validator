from io import BytesIO, SEEK_END
from tokenize import tokenize, INDENT

UTF_8_BOM = "\ufeff"

LINE_ENDINGS = {
    "crlf": "\r\n",
    "lf": "\n",
    "cr": "\r",
}


def validate_file(path, properties, is_python=True):
    errors = 0
    indent_style = properties.get("indent_style")
    indent_size = properties.get("indent_size")
    end_of_line = properties.get("end_of_line")
    trim_trailing_whitespace = properties.get("trim_trailing_whitespace")
    charset = properties.get("charset")
    insert_final_newline = properties.get("insert_final_newline")
    if charset not in ("utf-8", "utf-8-bom"):
        print("Only UTF-8 and UTF-8-BOM charsets supported")
        errors += 1

    try:
        indent_size = int(indent_size)
    except (ValueError, TypeError):
        print("Invalid indent_size: {indent_size!r}")
        errors += 1
    if end_of_line and end_of_line not in LINE_ENDINGS:
        print("Invalid end_of_line value: {end_of_line!r}")
        errors += 1
        end_of_line = None

    with open(path, mode="rt", newline="", encoding="utf-8") as f:
        has_bom = f.readline().startswith(UTF_8_BOM)
        if charset == "utf-8" and has_bom:
            print("UTF-8 byte order mark found")
            errors += 1
        elif charset == "utf-8-bom" and not has_bom:
            print("UTF-8 byte order mark not found")
            errors += 1
        f.seek(0)
        indentation = set()
        for line in f:
            if trim_trailing_whitespace == "true":
                if line.rstrip() != line.rstrip("\r\n"):
                    print("Trailing whitespace found")
                    errors += 1
        if end_of_line is not None:
            if isinstance(f.newlines, tuple):
                print("Mixed line endings found")
                errors += 1
            elif f.newlines != LINE_ENDINGS[end_of_line]:
                print("Incorrect line endings found")
                errors += 1

    if is_python:
        with open(path, mode="rb") as binary_file:
            for token in tokenize(binary_file.readline):
                if token.type == INDENT:
                    indentation.add(token.string)

        if indent_style == "tab":
            if any(" " in indent for indent in indentation):
                print("Space indentation found in file (expected tabs)")
                errors += 1
        elif indent_style == "space":
            if any(len(indent) % indent_size != 0 for indent in indentation):
                print("Indentation size inconsistent")
                errors += 1

    if insert_final_newline:
        with open(path, mode="rb") as binary_file:
            binary_file.seek(-2, SEEK_END)
            last_couple_bytes = binary_file.read()
            if not last_couple_bytes.endswith((b"\r", b"\n")):
                print("No final newline found")
                errors += 1
    return errors

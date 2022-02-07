"""Command-line interface."""
import mimetypes
from pathlib import Path
import sys

from editorconfig import get_properties, EditorConfigError
import click

from .validators import validate_file


mimetypes.add_type("text/rst", ".rst")
mimetypes.add_type("text/toml", ".toml")


def is_text_file(path):
    mime, encoding = mimetypes.guess_type(path)
    return mime and mime.startswith("text/")


def is_python_file(path):
    mime, encoding = mimetypes.guess_type(path)
    return mime and mime.endswith("python")


@click.command()
@click.version_option()
def main() -> None:
    """EditorConfig Python Validator."""
    errors = 0
    for path in Path.cwd().rglob("*"):
        if not is_text_file(path):
            continue
        try:
            properties = get_properties(path)
        except EditorConfigError as e:
            print(e)
            errors += 1
        else:
            print(f"Checking {path}")
            errors += validate_file(path, properties, is_python_file(path))
    print(f"{errors} errors found")
    sys.exit(errors)


if __name__ == "__main__":
    main(prog_name="editorconfig-python-validator")  # pragma: no cover

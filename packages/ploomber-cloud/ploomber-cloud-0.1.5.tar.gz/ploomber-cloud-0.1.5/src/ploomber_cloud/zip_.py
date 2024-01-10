import zipfile
from pathlib import Path
from contextlib import contextmanager
from uuid import uuid4

import click


IGNORED = {".DS_Store", ".ipynb_checkpoints", "ploomber-cloud.json"}


def _is_git(path):
    """Return True if path is in a .git directory"""
    return ".git" in Path(path).parts


def _is_pyc(path):
    """Return True if path is a .pyc file"""
    return Path(path).suffix == ".pyc"


def _is_blacklisted_file(path):
    return Path(path).name in IGNORED


def _is_ignored_file(path):
    return _is_git(path) or _is_pyc(path) or _is_blacklisted_file(path)


def _generate_random_suffix():
    return str(uuid4()).replace("-", "")[:8]


@contextmanager
def zip_app(verbose, base_dir=None):
    """Compress app in a zip file"""
    base_dir = Path(base_dir or "")

    suffix = _generate_random_suffix()
    path_to_zip = base_dir / f"app-{suffix}.zip"

    if path_to_zip.exists():
        if verbose:
            click.echo(f"Deleting existing {path_to_zip}...")

        path_to_zip.unlink()

    if verbose:
        click.secho("Compressing app...", fg="green")

    files = [f for f in Path(base_dir).glob("**/*") if Path(f).is_file()]

    with zipfile.ZipFile(path_to_zip, "w", zipfile.ZIP_DEFLATED) as zip:
        for path in files:
            if _is_ignored_file(path) or Path(path).name == path_to_zip.name:
                continue

            click.echo(f"Adding {path}...")
            arcname = Path(path).relative_to(base_dir)
            zip.write(path, arcname=arcname)

    if verbose:
        click.secho("App compressed successfully!", fg="green")

    try:
        yield path_to_zip
    finally:
        if path_to_zip.exists():
            path_to_zip.unlink()

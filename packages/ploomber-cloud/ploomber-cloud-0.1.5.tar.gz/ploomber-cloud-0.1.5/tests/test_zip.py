from pathlib import Path
import zipfile
from functools import partial

import pytest

from ploomber_cloud import zip_


def _git_directory(base_dir):
    Path("a").touch()
    Path("b").touch()
    Path(".env").touch()
    somehiddendir = Path(".somehiddendir")
    somehiddendir.mkdir()
    (somehiddendir / "somefile").touch()

    somedir = Path("somedir")
    somedir.mkdir()
    (somedir / "anotherfile").touch()

    dot_git = Path(base_dir, ".git")
    dot_git.mkdir(parents=True)
    (dot_git / "somegitfile").touch()
    (dot_git / "anothergitfile").touch()

    Path("somefile.pyc").touch()
    pycache = Path("__pycache__")
    pycache.mkdir()
    (pycache / "somefile.pyc").touch()


git_directory_root = partial(_git_directory, base_dir="")
git_directory_subdir = partial(_git_directory, base_dir="subdir")


@pytest.mark.parametrize(
    "init_function",
    [
        git_directory_root,
        git_directory_subdir,
    ],
)
def test_zip_app(tmp_empty, init_function):
    init_function()

    with zip_.zip_app(verbose=True) as path_to_zip:
        with zipfile.ZipFile(path_to_zip) as app_zip:
            namelist = app_zip.namelist()

    assert not Path(path_to_zip).exists()
    assert set(namelist) == {
        "a",
        "b",
        ".env",
        ".somehiddendir/somefile",
        "somedir/anotherfile",
    }

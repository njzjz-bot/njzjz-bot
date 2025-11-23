from packaging.version import VERSION_PATTERN
import re
import os

def regex_certain_package(package: str):
    specifiers = r"(~=|==|>=|<=|>|<|!=|===)"
    return re.compile(package + r"(\s*" + specifiers + r"\s*" + VERSION_PATTERN + r")?", re.VERBOSE | re.IGNORECASE)

for path in (
    "pyproject.toml",
    "setup.py",
    "doc/requirements.txt",
    "docs/requirements.txt",
    "requirements.txt", 
):
    if not os.path.isfile(path):
        continue
    with open(path) as f:
        old_content = f.read()

    new_content = regex_certain_package(r"sphinx(-|_)rtd(-|_)theme").sub("sphinx-book-theme", old_content)
    new_content = regex_certain_package(r"deepmodeling(-|_)sphinx").sub("deepmodeling-sphinx>=0.3.0", new_content)
    if old_content == new_content:
        continue

    with open(path, "w") as f:
        f.write(new_content)
for path in (
    "doc/conf.py",
    "docs/conf.py",
    "conf.py",
):

    if not os.path.isfile(path):
        continue
    with open(path) as f:
        old_content = f.read()

    new_content = old_content.replace("sphinx_rtd_theme", "sphinx_book_theme")
    if old_content == new_content:
        continue

    with open(path, "w") as f:
        f.write(new_content)

#! /usr/bin/env python3
"""
Allure static files combiner.

Create single html files with all the allure report data, that can be opened from everywhere.

Example:
    python3 ./combine.py ../allure_gen [--dest xxx] [--auto-create-folders]

    or

    pip install allure-combine
    allure-combine allure_report_dir [--dest xxx] [--auto-create-folders]
    ac allure_report_dir [--dest xxx] [--auto-create-folders]

"""
# pylint: disable=line-too-long

import json
import base64
import typing
from pathlib import Path

import bs4
from bs4 import BeautifulSoup


HERE_DIR = Path(__file__).parent
SINON_JS = HERE_DIR/"sinon-9.2.4.js"
SERVER_JS = HERE_DIR/"server.js"
DEFAULT_HTML = "complete.html"
DEFAULT_CONTENT_TYPE = "text/plain;charset=UTF-8"
CONTENT_TYPES = {
    "svg": "image/svg",
    "txt": "text/plain;charset=UTF-8",
    "js": "application/javascript",
    "json": "application/json",
    "csv": "text/csv",
    "css": "text/css",
    "html": "text/html",
    "xml": "text/xml",
    "htm": "text/html",
    "png": "image/png",
    "jpeg": "image/jpeg",
    "jpg": "image/jpg",
    "gif": "image/gif",
    "mp4": "video/mp4",
    "avi": "video/avi",
    "webm": "video/webm"
}
BASE64_EXTENSIONS = ["png", "jpeg", "jpg", "gif", "html", "htm", "mp4", "avi"]
ALLOWED_EXTENSIONS = list(CONTENT_TYPES.keys())


def _render_server_template(template: str, data: typing.Iterable[typing.Dict[str, typing.Union[str, bytes]]]) -> str:
    print(f"> Building fake js server", end="... ")

    responses = [r'''server.respondWith(
    "GET", "%(url)s", [200, { "Content-Type": "%(mime)s", }, server_data["%(url)s"],]
);''' % d for d in data]
    jsondata = {d["url"]: ("data:{mime};base64,{content}" if d["base64"] else "{content}").format(**d) for d in data}

    server_js = (
        template
        .replace('"{{jsondata}}"', json.dumps(jsondata, indent=4))
        .replace('"{{responses}}"', "\n".join(responses))
    )

    print(f"Done, size is {len(server_js)}b")

    return server_js


def _read(file: Path):
    contents = file.read_text(encoding="utf-8")
    print("Done")
    return contents


def _check_allure_dir(folder: Path):
    print(f"> Checking {folder} for allure contents", end="... ")
    for file in [folder / name for name in ["index.html", "app.js", "styles.css"]]:
        if not file.exists():
            raise FileNotFoundError(f"ERROR: File {file} doesnt exists, but it should!")
    print("Done")


def _insert_code_before(soup: bs4.BeautifulSoup, code: str, tag: bs4.Tag):
    script = soup.new_tag("script")
    script.string = code
    tag.insert_before(script)
    return script


def _replace_tag_with_content(old_tag: bs4.Tag, new_tag: bs4.Tag, file: Path):
    print(f"  {old_tag} -> {file}")
    new_tag.string = file.read_text(encoding="utf8")
    old_tag.replaceWith(new_tag)
    return new_tag


def _load_allure_data(folder: Path, ignore_utf8_errors=False):
    print("> Scanning folder for data files", end="... ")
    data = []
    skipped = []
    for filepath in folder.glob("**/*.*"):
        ext = filepath.suffix.replace('.', '')
        if filepath.parent == folder:
            continue
        elif ext not in ALLOWED_EXTENSIONS:
            skipped.append(filepath)
            continue

        try:
            content = filepath.read_bytes()
            if ext in BASE64_EXTENSIONS:
                content = base64.b64encode(content)
            data.append({
                "content": content.decode(encoding="utf8", errors='ignore' if ignore_utf8_errors else "strict"),
                "url": str(filepath.relative_to(folder)).replace("\\", "/"),
                "mime": CONTENT_TYPES.get(ext, DEFAULT_CONTENT_TYPE),
                "base64": ext in BASE64_EXTENSIONS
            })
        except UnicodeDecodeError as e:
            print(f"Error on reading file {filepath}: {e}. Use --ignore-utf8-errors argument to skip this type of errors")
    if skipped:
        print(f"  WARNING: Found {len(skipped)} file{'s' if len(skipped)> 1 else''} with unsupported extensions"
              f" (supported: {ALLOWED_EXTENSIONS}). Skipped files: {', '.join(str(s) for s in skipped)}")
    print(f"Done, found {len(data)} files")
    return data


def combine_allure_to_str(
    folder: typing.Union[str, Path],
    ignore_utf8_errors=False,
    sinon_js_path=SINON_JS,
    server_js_path=SERVER_JS,
) -> str:
    folder = Path(folder)
    _check_allure_dir(folder)

    index_html = folder / "index.html"
    print(f"> Reading contents of {index_html}", end="... ")
    html = index_html.read_text(encoding="utf8")
    soup = BeautifulSoup(html, features="html.parser")
    print("Done")

    print("> Replacing script tags with their files contents")
    for old_tag in soup.findAll('script'):
        _replace_tag_with_content(old_tag, soup.new_tag("script"), folder / old_tag['src'])

    print("> Replacing link tags with their files contents")
    for old_tag in soup.findAll("link", rel="stylesheet"):
        _replace_tag_with_content(old_tag, soup.new_tag("style"), folder / old_tag['href'])

    server_code = _render_server_template(
        server_js_path.read_text(encoding="utf8"),
        _load_allure_data(folder, ignore_utf8_errors)
    )
    print(f"> Injecting sinonjs and server code into index html", end="... ")
    app_script = soup.find("script")
    _insert_code_before(soup, sinon_js_path.read_text("utf8"), app_script)
    _insert_code_before(soup, server_code, app_script)
    print("Done")

    return str(soup)


def combine_allure(folder: typing.Union[str, Path], destination: typing.Union[str, Path] = None, auto_create_folders=False, ignore_utf8_errors=False):
    if not destination:
        destination = folder
    destination = Path(destination)

    if destination.suffix != ".html":
        destination = Path(destination) / DEFAULT_HTML

    if not destination.parent.exists() and not auto_create_folders:
        raise FileNotFoundError(
            "Dest folder does not exists, please create it first, "
            "or you can use --auto-create-folders argument if in the command line.")
    elif auto_create_folders:
        destination.parent.mkdir(parents=True, exist_ok=True)

    combined_html = combine_allure_to_str(folder, ignore_utf8_errors=ignore_utf8_errors)

    print(f"> Saving result as {destination}", end="... ")
    destination.write_text(combined_html, encoding="utf8")
    print(f"Done, Complete file size is:{destination.stat().st_size}b")

    return combined_html

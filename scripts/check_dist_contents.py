from __future__ import annotations

import argparse
import stat
import tarfile
import zipfile
from dataclasses import dataclass
from email.parser import BytesParser
from pathlib import PurePosixPath, PureWindowsPath
from typing import Iterable


PACKAGE_PY_FILES = {
    "__init__.py",
    "_version.py",
    "allowance.py",
    "loaders.py",
    "models.py",
    "validation.py",
}
CSV_FILES = {
    "allowance_rules.csv",
    "payment_schedule.csv",
    "reform_history.csv",
    "schema.csv",
    "sources.csv",
}
JSON_FILES = {
    "allowance_rules.json",
    "payment_schedule.json",
    "reform_history.json",
    "sources.json",
}
DIST_INFO_FILES = {"METADATA", "WHEEL", "RECORD", "top_level.txt"}
REQUIRED_WHEEL_FILES = {
    "METADATA",
    "WHEEL",
    "RECORD",
    "licenses/LICENSE",
}
REQUIRED_SDIST_FILES = {
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "MANIFEST.in",
    "pyproject.toml",
    "PKG-INFO",
}
PROJECT_URLS = {
    "Homepage": "https://github.com/fp-fuyutsuki/jp-child-allowance-data",
    "Repository": "https://github.com/fp-fuyutsuki/jp-child-allowance-data",
    "Issues": "https://github.com/fp-fuyutsuki/jp-child-allowance-data/issues",
    "Changelog": "https://github.com/fp-fuyutsuki/jp-child-allowance-data/blob/main/CHANGELOG.md",
}
DENY_SUFFIXES = (".pem", ".key", ".p12", ".pfx")
DENY_NAMES = {".env", ".env.local", ".env.production", "credentials.json"}
WHEEL_FILENAME = "jp_child_allowance_data-0.3.0-py3-none-any.whl"
SDIST_FILENAME = "jp_child_allowance_data-0.3.0.tar.gz"


@dataclass(frozen=True)
class Member:
    name: str
    kind: str
    size: int


def _archive_basename(path: str) -> str:
    """Return a basename for either POSIX or Windows path spelling."""
    return PurePosixPath(path.replace("\\", "/")).name


def _normalize_archive_name(name: str) -> str:
    if "\\" in name or name.startswith("/"):
        raise ValueError(f"unsafe archive path: {name!r}")
    raw_name = name.rstrip("/")
    raw_parts = raw_name.split("/")
    path = PurePosixPath(raw_name)
    if (
        not raw_name
        or PureWindowsPath(name).drive
        or path.is_absolute()
        or not path.parts
        or any(part in {"", ".", ".."} for part in raw_parts)
    ):
        raise ValueError(f"unsafe archive path: {name!r}")
    return "/".join(path.parts)


def _print_members(archive_name: str, members: Iterable[Member]) -> None:
    for member in sorted(members, key=lambda item: item.name):
        print(f"{archive_name}\t{member.kind}\t{member.size}\t{member.name}")


def _check_denylist(members: Iterable[Member]) -> list[str]:
    errors: list[str] = []
    for member in members:
        basename = PurePosixPath(member.name).name.lower()
        if basename in DENY_NAMES or basename.endswith(DENY_SUFFIXES):
            errors.append(f"denylisted archive member: {member.name}")
    return errors


def _collect_wheel(path: str) -> tuple[list[Member], dict[str, bytes], list[str]]:
    members: list[Member] = []
    contents: dict[str, bytes] = {}
    errors: list[str] = []
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            try:
                name = _normalize_archive_name(info.filename)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            mode = (info.external_attr >> 16) & 0o170000
            if mode == stat.S_IFLNK:
                errors.append(f"wheel symlink is not allowed: {name}")
            kind = "dir" if info.is_dir() else "file"
            data = b"" if kind == "dir" else archive.read(info)
            members.append(Member(name=name, kind=kind, size=len(data)))
            if kind == "file":
                contents[name] = data
    return members, contents, errors


def _collect_sdist(path: str) -> tuple[list[Member], dict[str, bytes], list[str]]:
    members: list[Member] = []
    contents: dict[str, bytes] = {}
    errors: list[str] = []
    with tarfile.open(path, "r:gz") as archive:
        for info in archive.getmembers():
            try:
                name = _normalize_archive_name(info.name)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if info.isdir():
                kind = "dir"
                data = b""
            elif info.isfile():
                kind = "file"
                extracted = archive.extractfile(info)
                data = extracted.read() if extracted is not None else b""
            else:
                errors.append(f"sdist non-regular member is not allowed: {name}")
                kind = "other"
                data = b""
            members.append(Member(name=name, kind=kind, size=len(data)))
            if kind == "file":
                contents[name] = data
    return members, contents, errors


def _parent_directories(paths: Iterable[str]) -> set[str]:
    directories: set[str] = set()
    for path in paths:
        current = PurePosixPath(path).parent
        while str(current) != ".":
            directories.add(str(current))
            current = current.parent
    return directories


def _wheel_allowlist(dist_info: str) -> tuple[set[str], set[str]]:
    files = {
        *(f"jp_child_allowance_data/{name}" for name in PACKAGE_PY_FILES),
        *(f"jp_child_allowance_data/data/csv/{name}" for name in CSV_FILES),
        *(f"jp_child_allowance_data/data/json/{name}" for name in JSON_FILES),
        *(f"{dist_info}/{name}" for name in DIST_INFO_FILES),
        f"{dist_info}/licenses/LICENSE",
    }
    return files, _parent_directories(files)


def _sdist_allowlist(root: str) -> tuple[set[str], set[str]]:
    relative_files = {
        *REQUIRED_SDIST_FILES,
        "setup.cfg",
        *(f"jp_child_allowance_data/{name}" for name in PACKAGE_PY_FILES),
        *(f"jp_child_allowance_data/data/csv/{name}" for name in CSV_FILES),
        *(f"jp_child_allowance_data/data/json/{name}" for name in JSON_FILES),
        "jp_child_allowance_data.egg-info/PKG-INFO",
        "jp_child_allowance_data.egg-info/SOURCES.txt",
        "jp_child_allowance_data.egg-info/dependency_links.txt",
        "jp_child_allowance_data.egg-info/requires.txt",
        "jp_child_allowance_data.egg-info/top_level.txt",
    }
    files = {f"{root}/{path}" for path in relative_files}
    return files, _parent_directories(files)


def _validate_members(
    archive_name: str,
    members: list[Member],
    allowed_files: set[str],
    allowed_directories: set[str],
    required_files: set[str],
) -> list[str]:
    errors = _check_denylist(members)
    actual_files = {member.name for member in members if member.kind == "file"}
    for member in members:
        if member.kind == "file" and member.name not in allowed_files:
            errors.append(f"{archive_name}: member outside allowlist: {member.name}")
        if member.kind == "dir" and member.name not in allowed_directories:
            errors.append(f"{archive_name}: directory outside allowlist: {member.name}")
        if member.kind == "other":
            errors.append(f"{archive_name}: non-file member: {member.name}")
    for required in required_files:
        if required not in actual_files:
            errors.append(f"{archive_name}: missing required member: {required}")
    return errors


def _validate_metadata(data: bytes, label: str) -> list[str]:
    metadata = BytesParser().parsebytes(data)
    errors: list[str] = []
    if metadata.get("Name") != "jp-child-allowance-data":
        errors.append(f"{label}: unexpected Name")
    if metadata.get("Version") != "0.3.0":
        errors.append(f"{label}: unexpected Version")
    if metadata.get("License-Expression") != "Apache-2.0":
        errors.append(f"{label}: unexpected License-Expression")
    if metadata.get("License-File") != "LICENSE":
        errors.append(f"{label}: missing License-File: LICENSE")
    if not metadata.get_payload().strip():
        errors.append(f"{label}: README-derived Description is empty")
    project_urls = {
        key: value
        for key, value in (
            line.split(", ", 1)
            for line in metadata.get_all("Project-URL", [])
            if ", " in line
        )
    }
    for key, expected in PROJECT_URLS.items():
        if project_urls.get(key) != expected:
            errors.append(f"{label}: Project-URL {key!r} is missing or incorrect")
    return errors


def _validate_wheel(path: str) -> list[str]:
    if _archive_basename(path) != WHEEL_FILENAME:
        return [f"unexpected wheel filename: {path}"]
    members, contents, errors = _collect_wheel(path)
    _print_members(path, members)
    dist_info_candidates = [
        name.split("/", 1)[0]
        for name in contents
        if name.endswith(".dist-info/METADATA")
    ]
    if len(dist_info_candidates) != 1:
        return errors + ["wheel must contain exactly one dist-info/METADATA"]
    dist_info = dist_info_candidates[0]
    allowed_files, allowed_dirs = _wheel_allowlist(dist_info)
    errors.extend(_validate_members(path, members, allowed_files, allowed_dirs, {
        f"{dist_info}/{name}" for name in REQUIRED_WHEEL_FILES
    }))
    errors.extend(_validate_metadata(contents[f"{dist_info}/METADATA"], f"{path}:{dist_info}/METADATA"))
    return errors


def _validate_sdist(path: str) -> list[str]:
    if _archive_basename(path) != SDIST_FILENAME:
        return [f"unexpected sdist filename: {path}"]
    members, contents, errors = _collect_sdist(path)
    _print_members(path, members)
    roots = {member.name.split("/", 1)[0] for member in members}
    if len(roots) != 1:
        return errors + ["sdist must contain exactly one top-level directory"]
    root = roots.pop()
    if root.replace("_", "-") != "jp-child-allowance-data-0.3.0":
        errors.append(f"unexpected sdist root: {root}")
    allowed_files, allowed_dirs = _sdist_allowlist(root)
    errors.extend(_validate_members(path, members, allowed_files, allowed_dirs, {
        f"{root}/{name}" for name in REQUIRED_SDIST_FILES
    }))
    metadata_name = f"{root}/PKG-INFO"
    if metadata_name in contents:
        errors.extend(_validate_metadata(contents[metadata_name], f"{path}:{metadata_name}"))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect wheel and sdist contents.")
    parser.add_argument("dist_dir")
    args = parser.parse_args()

    from pathlib import Path

    dist_dir = Path(args.dist_dir)
    wheels = sorted(dist_dir.glob("*.whl"))
    sdists = sorted(dist_dir.glob("*.tar.gz"))
    errors: list[str] = []
    if len(wheels) != 1:
        errors.append(f"expected exactly one wheel, found {len(wheels)}")
    if len(sdists) != 1:
        errors.append(f"expected exactly one sdist, found {len(sdists)}")
    if wheels:
        errors.extend(_validate_wheel(str(wheels[0])))
    if sdists:
        errors.extend(_validate_sdist(str(sdists[0])))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("distribution contents: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

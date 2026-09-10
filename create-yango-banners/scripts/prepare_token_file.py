#!/usr/bin/env python3
"""Create a blank private credential file; never read or overwrite a user's token."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def prepare_token_file(path: Path, kind: str = "mcp") -> dict[str, object]:
    path = path.expanduser().absolute()
    skill_root = Path(__file__).resolve().parents[1]
    if path.is_symlink():
        raise ValueError("Choose a regular personal file, not a symbolic link.")
    resolved = path.resolve()
    if resolved.is_relative_to(skill_root) or any(
        (parent / ".git").exists() for parent in resolved.parents
    ):
        raise ValueError("Choose a personal location outside repositories and this skill.")
    if path.exists():
        if not path.is_file():
            raise ValueError("The selected path is not a regular file.")
        return {"path": str(path), "created": False, "status": "existing_file_preserved"}
    template_name = (
        "creative-machine-download.env.example" if kind == "download"
        else "creative-machine-token.env.example"
    )
    template = (skill_root / "assets" / template_name).read_bytes()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise ValueError("The file appeared during setup; inspect its path before continuing.") from None
    with os.fdopen(fd, "wb") as output:
        output.write(template)
    status = "awaiting_credentials" if kind == "download" else "awaiting_token"
    return {"path": str(path), "created": True, "status": status}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=["mcp", "download"], default="mcp")
    parser.add_argument("--path", type=Path)
    args = parser.parse_args()
    try:
        path = args.path or Path.home() / ".config" / "creative-machine" / (
            "download.env" if args.kind == "download" else "token.env"
        )
        result = prepare_token_file(path, args.kind)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "file_not_prepared", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

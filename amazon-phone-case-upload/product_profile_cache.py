#!/usr/bin/env python3
"""Small JSON cache helpers for incremental phone-case listing runs."""

import hashlib
import json
from pathlib import Path


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_profile(path):
    path = Path(path)
    if not path.exists():
        return {"schema_version": 1, "product": {}, "content": {}, "assets": {}}
    with path.open("r", encoding="utf-8") as handle:
        profile = json.load(handle)
    if profile.get("schema_version") != 1:
        raise ValueError("Unsupported product profile schema_version")
    return profile


def save_profile(path, profile):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(profile, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    temporary.replace(path)


def reusable_asset_url(source_path, cached_asset):
    if not cached_asset or not cached_asset.get("verified") or not cached_asset.get("url"):
        return None
    if cached_asset.get("sha256") != file_sha256(source_path):
        return None
    return cached_asset["url"]

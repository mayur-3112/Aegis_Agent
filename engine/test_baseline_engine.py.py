import os
import json
import tempfile
from pathlib import Path

import pytest

import baseline_engine as be


@pytest.fixture
def temp_dir_with_files(tmp_path: Path):
    """Create a temporary directory with test files."""
    d = tmp_path
    f1 = d / "file1.txt"
    f1.write_text("hello world")

    f2 = d / "file2.txt"
    f2.write_text("another file")

    subdir = d / "sub"
    subdir.mkdir()
    f3 = subdir / "nested.txt"
    f3.write_text("deep file")

    return d, [f1, f2, f3]


def test_compute_file_hash_basic(tmp_path: Path):
    f = tmp_path / "sample.txt"
    content = "abc123"
    f.write_text(content)

    path, hexhash, size, mtime, mode, uid, gid, typ = be.compute_file_hash(str(f), "sha256")
    assert path == str(f)
    assert hexhash is not None and len(hexhash) == 64
    assert size == len(content)
    assert typ == "file"


def test_make_snapshot_returns_entries(temp_dir_with_files):
    d, files = temp_dir_with_files
    results = be.make_snapshot([str(d)], workers=1)

    # Ensure all expected files are present
    paths = {r["path"] for r in results}
    for f in files:
        assert str(f) in paths

    # All should have valid hashes
    for r in results:
        assert r["hash"] is not None
        assert r["type"] == "file"


def test_exclude_pattern(temp_dir_with_files):
    d, files = temp_dir_with_files
    exclude_file = files[0]  # exclude first file
    results = be.make_snapshot([str(d)], workers=1, exclude_patterns=[exclude_file.name])

    paths = {r["path"] for r in results}
    assert str(exclude_file) not in paths


def test_min_size_filter(tmp_path: Path):
    f_small = tmp_path / "small.txt"
    f_small.write_text("tiny")
    f_large = tmp_path / "large.txt"
    f_large.write_text("x" * 1024)

    results = be.make_snapshot([str(tmp_path)], workers=1, min_size=100)
    paths = {r["path"] for r in results}

    assert str(f_small) not in paths
    assert str(f_large) in paths


def test_jsonl_output(temp_dir_with_files, tmp_path: Path):
    d, _ = temp_dir_with_files
    out_file = tmp_path / "snapshot.jsonl"

    results = be.make_snapshot([str(d)], workers=1, out_file=str(out_file))

    assert out_file.exists()
    lines = out_file.read_text().splitlines()
    assert len(lines) == len(results)

    parsed = [json.loads(l) for l in lines]
    assert all("path" in r for r in parsed)
    assert all("hash" in r for r in parsed)

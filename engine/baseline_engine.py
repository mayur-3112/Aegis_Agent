#!/usr/bin/env python3
"""
baseline_engine.py

Baseline Engine for Project Aegis — produces cryptographic snapshots of filesystem objects.

Design goals implemented here:
- Portable, dependency-light (standard library only)
- Fast, parallel hashing with bounded worker pool
- Configurable hash algorithm (sha256 default) and metadata captured
- Exclude/include patterns, symlink control, file size cutoff
- Outputs JSONL (one JSON object per entry) or returns Python list
- Progress callback support for integration with benchmarking harness
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from dataclasses import dataclass, asdict
from multiprocessing import Pool, cpu_count
from pathlib import Path
from typing import Callable, Iterable, Iterator, List, Optional, Sequence, Tuple, Dict

# --- Configuration ---
READ_CHUNK = 1024 * 1024  # 1 MiB
DEFAULT_ALGORITHM = "sha256"


@dataclass
class SnapshotEntry:
    path: str
    hash: Optional[str]
    size: Optional[int]
    mtime: Optional[float]
    mode: Optional[int]
    uid: Optional[int]
    gid: Optional[int]
    type: str  # 'file', 'dir', 'symlink', 'other', 'error'
    error: Optional[str] = None


def _is_excluded(path: Path, exclude_patterns: Optional[Sequence[str]]) -> bool:
    if not exclude_patterns:
        return False
    s = str(path)
    for pat in exclude_patterns:
        if pat and pat in s:
            return True
    return False


def iter_target_files(paths: Sequence[str], exclude_patterns: Optional[Sequence[str]] = None,
                      follow_symlinks: bool = False, min_size: int = 0) -> Iterator[Path]:
    """Yield Path objects for files to snapshot.

    - Skips items that match an exclude pattern (simple substring match by default).
    - If a path is a directory, recursively walk it.
    - Yields only regular files with size >= min_size.
    """
    for p in paths:
        pth = Path(p)
        if _is_excluded(pth, exclude_patterns):
            continue
        try:
            if pth.is_dir():
                for root, dirs, files in os.walk(pth, followlinks=follow_symlinks):
                    rootp = Path(root)
                    if _is_excluded(rootp, exclude_patterns):
                        # skip descending into this directory
                        dirs[:] = []
                        continue
                    for f in files:
                        fp = rootp / f
                        if _is_excluded(fp, exclude_patterns):
                            continue
                        try:
                            st = fp.lstat() if not follow_symlinks else fp.stat()
                        except Exception:
                            continue
                        if not stat.S_ISREG(st.st_mode):
                            continue
                        if st.st_size < min_size:
                            continue
                        yield fp
            else:
                # single file or symlink
                try:
                    st = pth.lstat() if not follow_symlinks else pth.stat()
                except Exception:
                    continue
                if stat.S_ISREG(st.st_mode) and st.st_size >= min_size:
                    yield pth
        except Exception:
            continue


def compute_file_hash(path: str, algorithm: str = DEFAULT_ALGORITHM) -> Tuple[str, Optional[str], Optional[int], Optional[float], Optional[int], Optional[int], Optional[int], str]:
    """Compute the hash for a single file and return a tuple suitable for building SnapshotEntry.

    Returns (path, hexhash or None, size, mtime, mode, uid, gid, type_or_error)
    If an error occurs, hash will be None and type_or_error will contain an error description.
    """
    p = Path(path)
    try:
        st = p.stat()
        size = st.st_size
        mtime = st.st_mtime
        mode = st.st_mode
        uid = getattr(st, "st_uid", None)
        gid = getattr(st, "st_gid", None)

        # Initialize hasher
        try:
            hasher = hashlib.new(algorithm)
        except Exception as exc:
            return (str(p), None, size, mtime, mode, uid, gid, f"error: unsupported algorithm: {exc}")

        # Read file in chunks
        with p.open("rb") as f:
            while True:
                chunk = f.read(READ_CHUNK)
                if not chunk:
                    break
                hasher.update(chunk)
        return (str(p), hasher.hexdigest(), size, mtime, mode, uid, gid, "file")

    except Exception as exc:
        # On error, return entry with None hash and error in type field for downstream handling
        return (str(p), None, None, None, None, None, None, f"error: {exc}")


def _worker_hash(args: Tuple[str, str]) -> Dict:
    path, algorithm = args
    tup = compute_file_hash(path, algorithm=algorithm)
    path_s, hexhash, size, mtime, mode, uid, gid, typ = tup
    entry = SnapshotEntry(
        path=path_s,
        hash=hexhash,
        size=size,
        mtime=mtime,
        mode=mode,
        uid=uid,
        gid=gid,
        type=(typ if not typ.startswith("error") else "error"),
        error=(typ if typ.startswith("error") else None),
    )
    return asdict(entry)


def make_snapshot(paths: Sequence[str], *, out_file: Optional[str] = None, algorithm: str = DEFAULT_ALGORITHM,
                  workers: Optional[int] = None, follow_symlinks: bool = False,
                  exclude_patterns: Optional[Sequence[str]] = None, min_size: int = 0,
                  progress: Optional[Callable[[int, int], None]] = None) -> List[Dict]:
    """Create a snapshot for the given paths.

    - paths: list of files/directories
    - out_file: if provided, write results as JSONL (one JSON object per line)
    - algorithm: hashlib algorithm name (e.g., 'sha256', 'sha1', 'md5', 'blake2b')
    - workers: number of parallel worker processes (defaults to cpu_count())
    - follow_symlinks: whether to follow symlinks while walking
    - exclude_patterns: sequence of substring patterns to exclude
    - min_size: ignore files smaller than this many bytes
    - progress: optional callback(progress_done, total)

    Returns list of dictionaries (SnapshotEntry as dict).
    """
    if workers is None:
        workers = max(1, min(32, cpu_count()))

    files = list(iter_target_files(paths, exclude_patterns=exclude_patterns,
                                   follow_symlinks=follow_symlinks, min_size=min_size))
    total = len(files)

    results: List[Dict] = []

    if total == 0:
        # Return directory and non-regular entries metadata too
        # Walk once more to include directories / symlinks info
        for p in paths:
            pth = Path(p)
            try:
                st = pth.lstat()
                typ = 'dir' if stat.S_ISDIR(st.st_mode) else 'symlink' if stat.S_ISLNK(st.st_mode) else 'other'
                entry = SnapshotEntry(path=str(pth), hash=None, size=getattr(st, 'st_size', None),
                                      mtime=getattr(st, 'st_mtime', None), mode=st.st_mode,
                                      uid=getattr(st, 'st_uid', None), gid=getattr(st, 'st_gid', None), type=typ)
                results.append(asdict(entry))
            except Exception:
                continue
        if out_file:
            with open(out_file, 'w', encoding='utf-8') as fh:
                for r in results:
                    fh.write(json.dumps(r, ensure_ascii=False) + '\n')
        return results

    # Use multiprocessing Pool for CPU-bound hashing tasks
    pool_args = ((str(p), algorithm) for p in files)

    # If only one worker, compute inline to avoid process overhead
    if workers == 1:
        for idx, arg in enumerate(pool_args, start=1):
            r = _worker_hash(arg)
            results.append(r)
            if progress:
                progress(idx, total)
    else:
        with Pool(processes=workers) as pool:
            for idx, r in enumerate(pool.imap_unordered(_worker_hash, pool_args), start=1):
                results.append(r)
                if progress:
                    progress(idx, total)

    if out_file:
        with open(out_file, 'w', encoding='utf-8') as fh:
            for r in results:
                fh.write(json.dumps(r, ensure_ascii=False) + '\n')

    return results


# --- CLI convenience ---

def _parse_cli_args(argv: Optional[Sequence[str]] = None) -> Dict:
    import argparse
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(prog='baseline_engine', description='Project Aegis baseline snapshot engine')
    parser.add_argument('paths', nargs='+', help='Files or directories to snapshot')
    parser.add_argument('-a', '--algorithm', default=DEFAULT_ALGORITHM, help='Hash algorithm (sha256, sha1, md5, blake2b)')
    parser.add_argument('-o', '--out', help='Write JSONL output to file')
    parser.add_argument('-w', '--workers', type=int, help='Number of parallel workers (default: CPU count)')
    parser.add_argument('--follow-symlinks', action='store_true')
    parser.add_argument('--min-size', type=int, default=0, help='Ignore files smaller than MIN_SIZE bytes')
    parser.add_argument('--exclude', action='append', help='Exclude paths containing this substring (can be repeated)')
    args = parser.parse_args(argv)
    return vars(args)


def _simple_progress(done: int, total: int) -> None:
    print(f"[{done}/{total}] hashed", end='\r', file=sys.stderr)


def main(argv: Optional[Sequence[str]] = None) -> int:
    cli = _parse_cli_args(argv)
    paths = cli.pop('paths')
    out = cli.pop('out')
    workers = cli.pop('workers')
    algorithm = cli.pop('algorithm')
    follow_symlinks = cli.pop('follow_symlinks')
    min_size = cli.pop('min_size')
    exclude = cli.pop('exclude')

    res = make_snapshot(paths, out_file=out, algorithm=algorithm, workers=workers,
                        follow_symlinks=follow_symlinks, exclude_patterns=exclude,
                        min_size=min_size, progress=_simple_progress)
    # print summary
    good = sum(1 for r in res if r.get('hash'))
    bad = len(res) - good
    print(f"\nSnapshot complete: {len(res)} entries ({good} hashed, {bad} errors)")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

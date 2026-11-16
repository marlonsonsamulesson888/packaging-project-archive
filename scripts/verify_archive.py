#!/usr/bin/env python3
"""Read-only regular-file archive comparison; stdout is JSON, never acceptance."""
import argparse
import hashlib
import json
import os
from pathlib import Path


def scan(root):
    found, errors = {}, []
    def walk_error(exc):
        errors.append(str(exc))
    for base, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        for name in list(dirs):
            p = Path(base) / name
            if p.is_symlink():
                errors.append('symlink directory: ' + str(p.relative_to(root)))
                dirs.remove(name)
        for name in sorted(files):
            p = Path(base) / name
            rel = p.relative_to(root).as_posix()
            try:
                if p.is_symlink() or not p.is_file():
                    raise ValueError('not a regular non-symlink file')
                before = p.stat()
                h = hashlib.sha256()
                with p.open('rb') as stream:
                    while True:
                        chunk = stream.read(1024 * 1024)
                        if not chunk:
                            break
                        h.update(chunk)
                after = p.stat()
                if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
                    raise ValueError('file changed during hashing')
                found[rel] = {'size': after.st_size, 'sha256': h.hexdigest()}
            except (OSError, ValueError) as exc:
                errors.append(rel + ': ' + str(exc))
    return found, errors


def compare(source, copy):
    source, copy = Path(source).resolve(), Path(copy).resolve()
    if not source.is_dir() or not copy.is_dir():
        raise ValueError('both roots must exist as directories')
    if source == copy or source in copy.parents or copy in source.parents:
        raise ValueError('roots must be distinct and not nested')
    a, ea = scan(source)
    b, eb = scan(copy)
    missing, extra = sorted(a.keys() - b.keys()), sorted(b.keys() - a.keys())
    changed = sorted(k for k in a.keys() & b.keys() if a[k] != b[k])
    matched = len(a.keys() & b.keys()) - len(changed)
    return {'source_count': len(a), 'copy_count': len(b), 'matched_count': matched,
            'missing': missing, 'extra': extra, 'changed': changed,
            'source_errors': ea, 'copy_errors': eb,
            'regular_file_bytes_match': not (missing or extra or changed or ea or eb),
            'scope': 'regular-file paths and bytes only; document dependencies and restore untested'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('copy')
    args = parser.parse_args()
    try:
        result = compare(args.source, args.copy)
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['regular_file_bytes_match'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

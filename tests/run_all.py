#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_all.py — jalankan SEMUA tests.py di repo (E2E gate sebelum push).

    python tests/run_all.py           # semua tool
    python tests/run_all.py jsonc     # cuma tool yang namanya cocok filter

Exit 0 hanya kalau semua suite lulus.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def temukan_suite(filter_nama):
    suite = []
    for akar, _, nama in os.walk(os.path.join(ROOT, "tools")):
        for n in nama:
            if n == "tests.py":
                rel = os.path.relpath(akar, ROOT)
                if not filter_nama or filter_nama in rel.lower():
                    suite.append(os.path.join(akar, n))
    return sorted(suite)


def main():
    filter_nama = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    suite = temukan_suite(filter_nama)
    if not suite:
        print(f"[!] tidak ada suite cocok filter {filter_nama!r}")
        return 2

    gagal = []
    for t in suite:
        rel = os.path.relpath(os.path.dirname(t), ROOT)
        print(f"\n=== {rel} ===")
        r = subprocess.run([sys.executable, t], timeout=300)
        if r.returncode != 0:
            gagal.append(rel)

    print("\n" + "=" * 60)
    if gagal:
        print(f"  GAGAL: {len(gagal)} suite: {', '.join(gagal)}")
    else:
        print(f"  SEMUA LULUS: {len(suite)} suite")
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())

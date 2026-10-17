#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""env_report.py — snapshot lingkungan Windows development (read-only).

Laporan: OS, versi python/node/npm/git, disk per drive, jumlah entri PATH.
Berguna buat cek cepat mesin baru / handoff antar mesin.

    python env_report.py            # laporan teks
    python env_report.py --json     # output JSON (buat agent/CI)

Exit 0 selama laporan bisa dibuat. Tidak ada dependensi eksternal.
"""
import argparse
import json
import os
import platform
import shutil
import string
import subprocess
import sys


def versi_komando(cmd, args):
    """Versi pertama baris output komando, atau None kalau tidak ada."""
    exe = shutil.which(cmd)
    if not exe:
        return None
    try:
        r = subprocess.run([exe, *args], capture_output=True, text=True,
                           timeout=15)
        baris = (r.stdout or r.stderr).strip().splitlines()
        return baris[0].strip() if baris else "?"
    except Exception:
        return None


def info_disk():
    out = {}
    for huruf in string.ascii_uppercase:
        drive = f"{huruf}:\\"
        if os.path.isdir(drive):
            try:
                total, _, bebas = shutil.disk_usage(drive)
                out[drive] = {
                    "total_gb": round(total / 2 ** 30, 1),
                    "free_gb": round(bebas / 2 ** 30, 1),
                    "free_pct": round(bebas / total * 100, 1),
                }
            except OSError:
                continue
    return out


def kumpulkan():
    return {
        "hostname": platform.node(),
        "os": platform.platform(),
        "python": sys.version.split()[0],
        "node": versi_komando("node", ["--version"]),
        "npm": versi_komando("npm", ["--version"]),
        "git": versi_komando("git", ["--version"]),
        "disks": info_disk(),
        "path_jumlah": len(os.environ.get("PATH", "").split(os.pathsep)),
    }


def cetak(laporan):
    print(f"hostname : {laporan['hostname']}")
    print(f"os       : {laporan['os']}")
    print(f"python   : {laporan['python']}")
    for k in ("node", "npm", "git"):
        print(f"{k:<9}: {laporan[k] or '(tidak terpasang)'}")
    print(f"PATH     : {laporan['path_jumlah']} entri")
    print("disk     :")
    for drive, info in laporan["disks"].items():
        print(f"  {drive} {info['free_gb']:>7} GB bebas "
              f"({info['free_pct']}%) dari {info['total_gb']} GB")
        if info["free_pct"] < 10:
            print(f"  [!] {drive} sisa <10% — bersihkan space")


def main():
    ap = argparse.ArgumentParser(description="snapshot lingkungan Windows")
    ap.add_argument("--json", action="store_true",
                    help="output JSON, bukan teks")
    a = ap.parse_args()

    laporan = kumpulkan()
    if a.json:
        print(json.dumps(laporan, indent=2, ensure_ascii=False))
    else:
        cetak(laporan)
    return 0


if __name__ == "__main__":
    sys.exit(main())

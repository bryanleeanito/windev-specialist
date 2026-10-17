#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests.py - uji E2E env_report.py (tanpa jaringan, read-only).

    python tests.py [-v]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "env_report.py")


def jalankan(*args):
    r = subprocess.run([sys.executable, REPORT, *args],
                       capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout + r.stderr


def _json():
    code, out = jalankan("--json")
    assert code == 0, f"exit {code}: {out}"
    return json.loads(out)


TES = []


def tes(fn):
    TES.append(fn)
    return fn


@tes
def json_valid_dan_lengkap():
    d = _json()
    for k in ("hostname", "os", "python", "node", "npm", "git", "disks",
              "path_jumlah"):
        assert k in d, f"kunci hilang: {k}"
    assert d["python"] == sys.version.split()[0], "versi python tidak cocok"
    assert d["path_jumlah"] > 0, "PATH kosong"


@tes
def disk_c_ada():
    d = _json()
    assert "C:\\" in d["disks"], "drive C: tidak terlapor"
    info = d["disks"]["C:\\"]
    assert info["free_gb"] > 0 and info["total_gb"] > 0
    assert 0 < info["free_pct"] <= 100


@tes
def versi_komado_masuk_akal():
    d = _json()
    if d["node"] is not None:
        assert d["node"].startswith("v"), f"node aneh: {d['node']}"
    if d["npm"] is not None:
        assert d["npm"][0].isdigit(), f"npm aneh: {d['npm']}"
    if d["git"] is not None:
        assert "git" in d["git"].lower(), f"git aneh: {d['git']}"


@tes
def mode_teks_jalan():
    code, out = jalankan()
    assert code == 0, f"exit {code}: {out}"
    for kata in ("hostname", "os", "python", "disk"):
        assert kata in out.lower(), f"'{ kata}' tidak ada di output"


def main():
    gagal = 0
    for fn in TES:
        nama = fn.__name__
        try:
            fn()
            print(f"  [PASS] {nama}")
        except AssertionError as e:
            gagal += 1
            print(f"  [FAIL] {nama}: {e}")
    print(f"\n  HASIL: {len(TES) - gagal}/{len(TES)} PASS")
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())

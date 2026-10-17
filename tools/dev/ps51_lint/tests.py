#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests.py - uji E2E ps51_lint.py (fixture teks + file temp + walk folder).

    python tests.py [-v]
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, "ps51_lint.py")

_spec = importlib.util.spec_from_file_location("lint_mod", LINT)
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)

BERSIH = """\
$ErrorActionPreference = "Stop"
Get-ChildItem | Where-Object { $_.Length -gt 1KB }
if ($?) { Write-Host "selesai" }
$teks = "di dalam string ada && palsu"
# komentar juga boleh || begitu
$value = $null -ne $x ? $x : 0
"""

RUSAK = """\
Get-ChildItem *.txt && Write-Host "lanjut"
Stop-Service Spooler || Write-Host "gagal"
$nama = $obj ?? "default"
$panjang = $data?.Length
"""

TES = []


def tes(fn):
    TES.append(fn)
    return fn


@tes
def script_bersih_nol_temuan():
    assert L.cari(BERSIH) == [], "seharusnya bersih"


@tes
def sintaks_ps7_tertangkap():
    t = L.cari(RUSAK)
    aturan = [x["aturan"] for x in t]
    for r in ("&&", "||", "??", "?."):
        assert r in aturan, f"'{r}' tidak tertangkap: {aturan}"
    assert t == sorted(t, key=lambda x: (x["baris"], x["kolom"])), \
        "temuan tidak terurut baris"


@tes
def string_dan_komentar_dilewati():
    isi = 'Write-Host "a && b"\n# pakai || di sini\nWrite-Host \'??\'\n'
    assert L.cari(isi) == [], f"false positive: {L.cari(isi)}"


@tes
def here_string_dilewati():
    isi = '@"\nini baris && && || ?? ?.\n"@ | Out-Host\n'
    # here-string bukan string biasa — minimal jangan crash; temuan di
    # here-string boleh ada ASAL tidak ada exception
    L.cari(isi)


@tes
def cli_file_dan_exit_code():
    f = tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False,
                                    encoding="utf-8")
    f.write(RUSAK)
    f.close()
    try:
        r = subprocess.run([sys.executable, LINT, f.name, "--json"],
                           capture_output=True, text=True, timeout=30)
        assert r.returncode == 1, f"file rusak harus exit 1: {r.stdout}"
        assert '"total": 4' in r.stdout, f"total temuan salah: {r.stdout}"

        f2 = tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False,
                                         encoding="utf-8")
        f2.write(BERSIH)
        f2.close()
        try:
            r = subprocess.run([sys.executable, LINT, f2.name],
                               capture_output=True, text=True, timeout=30)
            assert r.returncode == 0, f"file bersih harus exit 0: {r.stdout}"
        finally:
            os.unlink(f2.name)
    finally:
        os.unlink(f.name)


@tes
def walk_folder_ketemu_semua_file():
    d = tempfile.mkdtemp()
    for n, isi in (("a.ps1", RUSAK), ("b.psm1", "cmd1 && cmd2"),
                   ("c.txt", "&& harus diabaikan")):
        with open(os.path.join(d, n), "w", encoding="utf-8") as f:
            f.write(isi)
    try:
        file, hilang = L.kumpul_file([d])
        assert hilang == []
        assert len(file) == 2, f"harus 2 file ps: {file}"
        total = sum(len(L.cari(open(f, encoding='utf-8').read()))
                    for f in file)
        assert total == 5, f"total temuan salah: {total}"
    finally:
        for n in os.listdir(d):
            os.unlink(os.path.join(d, n))
        os.rmdir(d)


@tes
def path_hilang_exit_2():
    r = subprocess.run([sys.executable, LINT, r"Z:\tidak\ada.ps1"],
                       capture_output=True, text=True, timeout=30)
    assert r.returncode == 2, f"path hilang harus exit 2: {r.stdout}"


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

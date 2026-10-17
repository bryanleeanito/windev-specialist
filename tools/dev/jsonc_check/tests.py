#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests.py - uji E2E jsonc_check.py (fixture di memori + file temp).

    python tests.py [-v]
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "jsonc_check.py")

_spec = importlib.util.spec_from_file_location("jsonc_mod", CHECK)
J = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(J)


def file_temp(isi):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                   encoding="utf-8")
    f.write(isi)
    f.close()
    return f.name


TES = []


def tes(fn):
    TES.append(fn)
    return fn


@tes
def json_polos_valid():
    assert J.cek('{"a": 1, "b": [1, 2]}') is None


@tes
def komentar_line_dan_block():
    isi = ('{\n'
           '  // komentar baris\n'
           '  "a": 1, /* komentar block */\n'
           '  "b": "http://contoh.com/path" // url di nilai tidak disentuh\n'
           '}\n')
    assert J.cek(isi) is None


@tes
def trailing_comma_dihapus():
    assert J.cek('{"a": 1, "b": 2,}') is None
    assert J.cek('{"a": [1, 2,], }') is None


@tes
def json_rusak_ketahuan_line_akurat():
    # ',' setelah "b" bukan trailing (diikuti '"') -> error asli di baris 3
    isi = ('{\n'
           '  "a": 1,\n'
           '  "b": ,\n'
           '  "c": 2\n'
           '}\n')
    err = J.cek(isi)
    assert err is not None, "seharusnya invalid"
    assert err["baris"] == 3, f"baris salah: {err}"


@tes
def string_dengan_slash_diremehkan():
    assert J.cek('{"pesan": "komentar // palsu /* juga */"}') is None


@tes
def escape_kutip_di_string():
    assert J.cek('{"p": "nilai \\"kutip\\" // tetap string"}') is None


@tes
def cli_exit_code():
    ok = file_temp('{"x": 1, /* ok */}\n')
    rusak = file_temp('{"x": ,\n')
    try:
        r = subprocess.run([sys.executable, CHECK, ok], capture_output=True,
                           text=True, timeout=30)
        assert r.returncode == 0, f"file valid harus exit 0: {r.stdout}"
        r = subprocess.run([sys.executable, CHECK, rusak],
                           capture_output=True, text=True, timeout=30)
        assert r.returncode == 1, "file rusak harus exit 1"
        assert "baris 1" in r.stdout, f"posisi error tidak dicetak: {r.stdout}"
    finally:
        os.unlink(ok)
        os.unlink(rusak)


@tes
def opencode_json_asli_tervalidasi():
    """Smoke test config nyata kalau ada — skip kalau tidak ada."""
    cfg = os.path.expandvars(
        r"%USERPROFILE%\.config\opencode\opencode.json")
    if not os.path.isfile(cfg):
        print("       (opencode.json tidak ada — skip)")
        return
    err = J.cek(open(cfg, encoding="utf-8-sig").read())
    assert err is None, f"config live rusak: {err}"


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

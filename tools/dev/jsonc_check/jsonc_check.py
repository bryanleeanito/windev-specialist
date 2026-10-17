#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jsonc_check.py — validasi file JSONC (JSON + komentar + trailing comma).

Khusus buat config OpenCode (opencode.json): file-nya pakai komentar dan
trailing comma yang bikin `json.loads` biasa gagal.

    python jsonc_check.py "%USERPROFILE%\\.config\\opencode\\opencode.json"
    python jsonc_check.py --json a.json b.json   # agregat mesin-readable

Exit 0 = semua valid, 1 = ada yang invalid. Komentar di-BLANK (bukan dihapus)
dan trailing comma diganti spasi — nomor baris/kolom error tetap akurat.
"""
import argparse
import json
import sys


def _lewati_string(s, i):
    """i menunjuk kutip pembuka; return indeks kutip penutup."""
    n = len(s)
    i += 1
    while i < n:
        if s[i] == "\\":
            i += 2
            continue
        if s[i] == '"':
            return i
        i += 1
    return n - 1


def blank_komentar(s):
    """Ganti komentar jadi spasi; newline dipertahankan (baris stabil)."""
    out = list(s)
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c == '"':
            i = _lewati_string(s, i)
        elif c == "/" and i + 1 < n and s[i + 1] == "/":
            while i < n and s[i] != "\n":
                out[i] = " "
                i += 1
            continue
        elif c == "/" and i + 1 < n and s[i + 1] == "*":
            out[i] = out[i + 1] = " "
            i += 2
            while i < n and not (s[i] == "*" and i + 1 < n and s[i + 1] == "/"):
                if s[i] != "\n":
                    out[i] = " "
                i += 1
            if i < n:
                out[i] = out[i + 1] = " "
                i += 1
        i += 1
    return "".join(out)


def hapus_trailing_comma(s):
    """Kosongkan ',' yang diikuti '}' atau ']' (di luar string)."""
    out = list(s)
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c == '"':
            i = _lewati_string(s, i)
        elif c == ",":
            j = i + 1
            while j < n and s[j] in " \t\r\n":
                j += 1
            if j < n and s[j] in "}]":
                out[i] = " "
        i += 1
    return "".join(out)


def cek(teks):
    """Return None kalau valid, atau dict baris/kolom/pesan kalau invalid."""
    bersih = hapus_trailing_comma(blank_komentar(teks))
    try:
        json.loads(bersih)
        return None
    except json.JSONDecodeError as e:
        return {"baris": e.lineno, "kolom": e.colno, "pesan": e.msg}


def main():
    ap = argparse.ArgumentParser(description="validasi file JSONC")
    ap.add_argument("file", nargs="+")
    ap.add_argument("--json", action="store_true", help="output JSON")
    a = ap.parse_args()

    hasil = []
    for f in a.file:
        try:
            teks = open(f, encoding="utf-8-sig").read()
        except OSError as ex:
            hasil.append({"file": f, "valid": False,
                          "error": f"gagal baca: {ex}"})
            continue
        err = cek(teks)
        if err:
            hasil.append({"file": f, "valid": False, **err})
        else:
            hasil.append({"file": f, "valid": True})

    if a.json:
        print(json.dumps(hasil, indent=2, ensure_ascii=False))
    else:
        for h in hasil:
            if h["valid"]:
                print(f"[OK]   {h['file']}")
            else:
                detail = (f"baris {h.get('baris')}, kolom {h.get('kolom')}: "
                          f"{h.get('pesan') or h.get('error')}")
                print(f"[FAIL] {h['file']} — {detail}")
    return 0 if all(h["valid"] for h in hasil) else 1


if __name__ == "__main__":
    sys.exit(main())

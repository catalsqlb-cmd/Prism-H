#!/usr/bin/env python3
"""
Prism PDF → Markdown extractor — OPTIONAL MinerU adapter.

Prism-H's core is zero-dependency (stdlib only). PDF reading is normally done
by the agent's own multimodal Read tool. This helper is a *thin, optional*
bridge to MinerU (https://github.com/opendatalab/MinerU), which produces much
cleaner Markdown for the hard cases the agent struggles with: scanned court
judgments, multi-column legal/academic layouts, table-dense pages, and
formula-heavy text.

Design rules:
  - stdlib only (subprocess / pathlib / shutil / argparse) — no new deps here.
  - MinerU itself is NOT a Prism dependency. If it is not installed, this
    script exits cleanly with a clear message and a non-zero code, so callers
    can fall back to agent-native PDF reading.
  - Detects either the new `mineru` CLI (MinerU 2.x) or the legacy
    `magic-pdf` CLI (MinerU 1.x / magic-pdf).

Usage:
    python3 pdf_extract.py <input.pdf> [--out <dir>] [--print] [--backend auto|mineru|magic-pdf]
    python3 pdf_extract.py --check        # report whether a backend is available

Exit codes:
    0  success (markdown produced) OR --check found a backend
    3  no MinerU backend installed (caller should fall back)
    1  a backend was found but extraction failed
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# CLI name -> argv builder. Each returns (argv, expected_output_root_hint).
_BACKENDS = ("mineru", "magic-pdf")


def find_backend(prefer: str = "auto") -> str | None:
    """Return the name of an available MinerU CLI, or None."""
    if prefer != "auto":
        return prefer if shutil.which(prefer) else None
    for name in _BACKENDS:
        if shutil.which(name):
            return name
    return None


def _build_argv(backend: str, pdf: Path, out_dir: Path) -> list[str]:
    """Construct the CLI invocation for the detected backend.

    MinerU 2.x:   mineru -p <pdf> -o <out_dir> -m auto
    magic-pdf:    magic-pdf -p <pdf> -o <out_dir> -m auto
    Both default to 'auto' method (OCR when needed, else text extraction).
    """
    return [backend, "-p", str(pdf), "-o", str(out_dir), "-m", "auto"]


def _find_markdown(out_dir: Path, stem: str) -> Path | None:
    """Locate the Markdown file MinerU emitted under out_dir.

    Typical layout: <out_dir>/<stem>/auto/<stem>.md  (plus images/).
    We search broadly and prefer a file whose name matches the PDF stem.
    """
    candidates = sorted(out_dir.rglob("*.md"))
    if not candidates:
        return None
    for c in candidates:
        if c.stem == stem:
            return c
    # fall back to the largest .md (most likely the body)
    return max(candidates, key=lambda p: p.stat().st_size)


def extract(pdf: Path, out_dir: Path, backend: str) -> Path:
    """Run the backend and return the path to the produced Markdown file."""
    out_dir.mkdir(parents=True, exist_ok=True)
    argv = _build_argv(backend, pdf, out_dir)
    try:
        subprocess.run(argv, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"{backend} failed (exit {e.returncode}) on {pdf}")
    md = _find_markdown(out_dir, pdf.stem)
    if md is None:
        raise RuntimeError(
            f"{backend} produced no .md under {out_dir} for {pdf.name}"
        )
    return md


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Optional MinerU bridge: PDF -> clean Markdown. "
                    "Falls back (exit 3) when MinerU is not installed."
    )
    ap.add_argument("pdf", nargs="?", help="input PDF path")
    ap.add_argument("--out", help="output directory (default: <pdf_dir>/.mineru)")
    ap.add_argument("--backend", default="auto",
                    choices=["auto", "mineru", "magic-pdf"],
                    help="which MinerU CLI to use (default: auto-detect)")
    ap.add_argument("--print", dest="do_print", action="store_true",
                    help="print the extracted Markdown to stdout")
    ap.add_argument("--check", action="store_true",
                    help="report whether a MinerU backend is installed, then exit")
    args = ap.parse_args()

    backend = find_backend(args.backend)

    if args.check:
        if backend:
            print(f"mineru-backend: {backend} ({shutil.which(backend)})")
            return 0
        print("mineru-backend: none "
              "(install with `pip install mineru` — optional)", file=sys.stderr)
        return 3

    if not args.pdf:
        ap.error("the following argument is required: pdf")

    pdf = Path(args.pdf).expanduser().resolve()
    if not pdf.is_file():
        print(f"error: no such file: {pdf}", file=sys.stderr)
        return 1

    if not backend:
        print(
            "MinerU is not installed; no PDF backend available.\n"
            "Fall back to the agent's native PDF reading, or install MinerU "
            "(optional): pip install mineru\n"
            "See: https://github.com/opendatalab/MinerU",
            file=sys.stderr,
        )
        return 3

    out_dir = Path(args.out).expanduser().resolve() if args.out \
        else pdf.parent / ".mineru"

    try:
        md = extract(pdf, out_dir, backend)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.do_print:
        sys.stdout.write(md.read_text(encoding="utf-8", errors="replace"))
    else:
        print(str(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

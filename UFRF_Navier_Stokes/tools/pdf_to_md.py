#!/usr/bin/env python3
import argparse
from pathlib import Path
from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams


def extract_text(pdf_path: Path) -> str:
    output = StringIO()
    laparams = LAParams()
    with pdf_path.open('rb') as fp:
        extract_text_to_fp(fp, output, laparams=laparams, output_type='text', codec=None)
    return output.getvalue()


def sanitize_to_markdown(text: str) -> str:
    # Minimal cleanup: normalize whitespace, preserve headings if detected
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped = line.rstrip()
        # Collapse multiple spaces, keep code blocks or equations untouched heuristically
        cleaned_lines.append(stripped)
    return "\n".join(cleaned_lines)


def main():
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown-ish text using pdfminer")
    parser.add_argument("pdf", type=Path, help="Input PDF path")
    parser.add_argument("out", type=Path, help="Output Markdown path")
    args = parser.parse_args()

    text = extract_text(args.pdf)
    md = sanitize_to_markdown(text)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(md, encoding='utf-8')
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()



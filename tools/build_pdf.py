#!/usr/bin/env python3
"""Render a markdown document to a clean, review-ready PDF (and HTML).

Usage:  python3 tools/build_pdf.py paper/draft.md   ->  paper/draft.pdf + paper/draft.html

Uses python-markdown + weasyprint (pure-python HTML/CSS -> PDF, full Unicode). The CSS
below gives an academic single-column layout with page numbers; the body font is DejaVu
Serif, which covers the Greek letters / sub- & super-scripts used in the converted math.
"""
import sys, os, markdown

CSS = """
@page { size: A4; margin: 2.2cm 2.0cm 2.0cm 2.0cm;
        @bottom-center { content: counter(page); font: 9pt "DejaVu Serif"; color: #666; } }
body { font-family: "DejaVu Serif", Georgia, serif; font-size: 10.5pt; line-height: 1.45;
       text-align: justify; hyphens: auto; color: #111; }
h1 { font-size: 17pt; text-align: center; line-height: 1.25; margin: 0 0 0.3em; }
h2 { font-size: 12.5pt; margin: 1.3em 0 0.4em; padding-bottom: 2px;
     border-bottom: 1px solid #bbb; }
h3 { font-size: 10.8pt; margin: 1.0em 0 0.3em; color: #222; }
p { margin: 0 0 0.55em; }
a { color: #1a4b8c; text-decoration: none; }
code, tt { font-family: "DejaVu Sans Mono", monospace; font-size: 0.88em; background: #f4f4f4;
           padding: 0 2px; border-radius: 2px; }
strong { font-weight: bold; }
em { font-style: italic; }
blockquote { border-left: 3px solid #bbb; margin: 0.6em 0; padding: 0.1em 0 0.1em 1em;
             color: #333; }
hr { border: none; border-top: 1px solid #999; margin: 1.1em 0; }
table { border-collapse: collapse; width: 100%; font-size: 9.6pt; margin: 0.5em 0; }
th, td { border: 1px solid #ccc; padding: 3px 6px; text-align: left; vertical-align: top; }
th { background: #f0f0f0; }
ul, ol { margin: 0.2em 0 0.6em 1.2em; padding: 0; }
li { margin: 0.15em 0; }
h2, h3 { page-break-after: avoid; }
figure { margin: 1.1em auto; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; height: auto; border: 1px solid #ddd; }
figcaption { font-size: 9pt; color: #333; text-align: left; margin-top: 0.45em;
             line-height: 1.35; }
"""


def main():
    src_path = sys.argv[1] if len(sys.argv) > 1 else "paper/draft.md"
    base = os.path.splitext(src_path)[0]
    md = open(src_path, encoding="utf-8").read()
    body = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists", "smarty"])
    html = (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>{CSS}</style></head><body>{body}</body></html>")
    open(base + ".html", "w", encoding="utf-8").write(html)
    from weasyprint import HTML
    base_url = os.path.dirname(os.path.abspath(src_path))   # so ../figures/* resolves
    HTML(string=html, base_url=base_url).write_pdf(base + ".pdf")
    print(f"wrote {base}.pdf ({os.path.getsize(base+'.pdf')//1024} KB) and {base}.html")


if __name__ == "__main__":
    main()

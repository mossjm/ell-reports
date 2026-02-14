#!/usr/bin/env python3
"""Build professional HTML reports from markdown and convert to PDF via weasyprint."""

import os
import re
import html as html_module
import markdown
import subprocess

OUTPUT_DIR = "/Users/henry/Projects/ell-reports"

def get_css():
    return """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Merriweather:wght@300;400;700&display=swap');

@page {
    size: letter;
    margin: 2.5cm 2.5cm 3cm 2.5cm;
    @bottom-center {
        content: counter(page);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 9pt;
        color: #6b7280;
    }
    @bottom-right {
        content: "Elm Lake Labs";
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 8pt;
        color: #9ca3af;
    }
}

@page :first {
    margin: 0;
    @bottom-center { content: none; }
    @bottom-right { content: none; }
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Merriweather', Georgia, 'Times New Roman', serif;
    font-size: 10.5pt;
    line-height: 1.7;
    color: #1f2937;
    -webkit-font-smoothing: antialiased;
}

/* Cover Page */
.cover-page {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 3cm;
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
    color: white;
    text-align: center;
}

.cover-logo {
    font-family: 'Inter', sans-serif;
    font-size: 14pt;
    font-weight: 300;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    margin-bottom: 3cm;
}

.cover-title {
    font-family: 'Merriweather', Georgia, serif;
    font-size: 28pt;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 0.8cm;
    color: white;
    max-width: 18cm;
}

.cover-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 12pt;
    font-weight: 300;
    color: rgba(255,255,255,0.7);
    margin-bottom: 3cm;
    max-width: 14cm;
}

.cover-divider {
    width: 4cm;
    height: 2px;
    background: rgba(255,255,255,0.3);
    margin: 0 auto 1.5cm auto;
}

.cover-meta {
    font-family: 'Inter', sans-serif;
    font-size: 10pt;
    font-weight: 400;
    color: rgba(255,255,255,0.6);
    line-height: 1.8;
}

.cover-meta strong {
    color: rgba(255,255,255,0.85);
    font-weight: 600;
}

/* Table of Contents */
.toc-page {
    page-break-after: always;
    padding-top: 1cm;
}

.toc-page h2 {
    font-family: 'Inter', sans-serif;
    font-size: 18pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 1cm;
    padding-bottom: 0.3cm;
    border-bottom: 3px solid #1e3a5f;
}

.toc-list {
    list-style: none;
    padding: 0;
}

.toc-list li {
    font-family: 'Inter', sans-serif;
    font-size: 11pt;
    padding: 0.3cm 0;
    border-bottom: 1px solid #e5e7eb;
    color: #1e3a5f;
    font-weight: 500;
}

.toc-list li:last-child {
    border-bottom: none;
}

.toc-list .toc-sub {
    padding-left: 1.5cm;
    font-size: 10pt;
    font-weight: 400;
    color: #4b5563;
}

/* Content Headings */
h1 {
    font-family: 'Inter', sans-serif;
    font-size: 22pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 1.5cm;
    margin-bottom: 0.5cm;
    page-break-before: always;
    padding-bottom: 0.3cm;
    border-bottom: 3px solid #1e3a5f;
}

h1:first-of-type {
    page-break-before: auto;
}

h2 {
    font-family: 'Inter', sans-serif;
    font-size: 16pt;
    font-weight: 600;
    color: #1e3a5f;
    margin-top: 1cm;
    margin-bottom: 0.4cm;
    padding-bottom: 0.2cm;
    border-bottom: 1px solid #d1d5db;
}

h3 {
    font-family: 'Inter', sans-serif;
    font-size: 13pt;
    font-weight: 600;
    color: #374151;
    margin-top: 0.7cm;
    margin-bottom: 0.3cm;
}

h4 {
    font-family: 'Inter', sans-serif;
    font-size: 11pt;
    font-weight: 600;
    color: #4b5563;
    margin-top: 0.5cm;
    margin-bottom: 0.2cm;
}

/* Paragraphs */
p {
    margin-bottom: 0.4cm;
    text-align: justify;
    hyphens: auto;
}

/* Lists */
ul, ol {
    margin-bottom: 0.4cm;
    padding-left: 1cm;
}

li {
    margin-bottom: 0.15cm;
}

li > ul, li > ol {
    margin-top: 0.1cm;
    margin-bottom: 0.1cm;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.5cm 0;
    font-family: 'Inter', sans-serif;
    font-size: 9pt;
    line-height: 1.4;
    page-break-inside: avoid;
}

thead {
    background: #0f172a;
    color: white;
}

th {
    padding: 0.25cm 0.3cm;
    text-align: left;
    font-weight: 600;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

td {
    padding: 0.2cm 0.3cm;
    border-bottom: 1px solid #e5e7eb;
    vertical-align: top;
}

tr:nth-child(even) {
    background: #f9fafb;
}

tr:hover {
    background: #f3f4f6;
}

/* Code blocks */
pre {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #1e3a5f;
    padding: 0.4cm;
    margin: 0.4cm 0;
    font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 8.5pt;
    line-height: 1.5;
    overflow-wrap: break-word;
    white-space: pre-wrap;
    page-break-inside: avoid;
}

code {
    font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 9pt;
    background: #f1f5f9;
    padding: 0.05cm 0.15cm;
    border-radius: 3px;
}

pre code {
    background: none;
    padding: 0;
}

/* Blockquotes */
blockquote {
    border-left: 4px solid #1e3a5f;
    padding: 0.3cm 0.6cm;
    margin: 0.5cm 0;
    background: #f8fafc;
    font-style: italic;
    color: #374151;
}

blockquote p {
    margin-bottom: 0.2cm;
}

/* Strong/Bold */
strong {
    font-weight: 700;
    color: #111827;
}

/* Horizontal Rule */
hr {
    border: none;
    border-top: 1px solid #d1d5db;
    margin: 0.8cm 0;
}

/* Links */
a {
    color: #1e3a5f;
    text-decoration: none;
}

/* Section break helper */
.section-break {
    page-break-before: always;
}

/* Emoji handling */
.emoji {
    font-style: normal;
}

/* Print adjustments */
@media print {
    body { font-size: 10pt; }
    h1 { font-size: 20pt; }
    h2 { font-size: 14pt; }
    h3 { font-size: 12pt; }
    table { font-size: 8pt; }
}
"""

def md_to_html_body(md_content):
    """Convert markdown to HTML body, stripping the first H1 (used on cover)."""
    # Use python-markdown with tables extension
    extensions = ['tables', 'fenced_code', 'toc', 'smarty']
    body = markdown.markdown(md_content, extensions=extensions)
    return body

def extract_toc_items(md_content):
    """Extract section headings for TOC from markdown."""
    items = []
    for line in md_content.split('\n'):
        line = line.strip()
        if line.startswith('## ') and not line.startswith('## Table of Contents'):
            title = line.lstrip('#').strip()
            # Remove markdown link syntax
            title = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', title)
            items.append(('main', title))
        elif line.startswith('### '):
            title = line.lstrip('#').strip()
            title = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', title)
            items.append(('sub', title))
    return items

def strip_existing_toc(md_content):
    """Remove the existing Table of Contents section from markdown."""
    lines = md_content.split('\n')
    result = []
    in_toc = False
    for line in lines:
        if line.strip().startswith('## Table of Contents'):
            in_toc = True
            continue
        if in_toc:
            if line.strip().startswith('## ') or (line.strip().startswith('#') and not line.strip().startswith('##')):
                in_toc = False
                result.append(line)
            elif line.strip() == '---':
                in_toc = False
                continue
            continue
        result.append(line)
    return '\n'.join(result)

def strip_first_heading(md_content):
    """Remove the first H1 heading and any immediately following subtitle/metadata lines."""
    lines = md_content.split('\n')
    result = []
    found_h1 = False
    skip_meta = False
    for i, line in enumerate(lines):
        if not found_h1 and line.strip().startswith('# ') and not line.strip().startswith('## '):
            found_h1 = True
            skip_meta = True
            continue
        if skip_meta:
            stripped = line.strip()
            # Skip blank lines, italicized metadata, and dividers after the title
            if stripped == '' or stripped.startswith('*') or stripped == '---':
                continue
            else:
                skip_meta = False
        result.append(line)
    return '\n'.join(result)

def build_html(title, subtitle, org, md_content):
    """Build a complete HTML document with cover page, TOC, and content."""
    
    css = get_css()
    toc_items = extract_toc_items(md_content)
    
    # Clean the markdown
    clean_md = strip_existing_toc(md_content)
    clean_md = strip_first_heading(clean_md)
    
    # Convert to HTML
    body_html = md_to_html_body(clean_md)
    
    # Build TOC HTML
    toc_html = '<div class="toc-page">\n<h2>Table of Contents</h2>\n<ul class="toc-list">\n'
    for kind, item in toc_items:
        cls = ' class="toc-sub"' if kind == 'sub' else ''
        toc_html += f'<li{cls}>{html_module.escape(item)}</li>\n'
    toc_html += '</ul>\n</div>\n'
    
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_module.escape(title)}</title>
<style>
{css}
</style>
</head>
<body>

<!-- Cover Page -->
<div class="cover-page">
    <div class="cover-logo">{html_module.escape(org)}</div>
    <h1 class="cover-title">{html_module.escape(title)}</h1>
    <p class="cover-subtitle">{html_module.escape(subtitle)}</p>
    <div class="cover-divider"></div>
    <div class="cover-meta">
        <strong>Prepared for</strong> {html_module.escape(org)}<br>
        <strong>Date</strong> February 14, 2026<br>
        <strong>Prepared by</strong> Henry Clawson
    </div>
</div>

<!-- Table of Contents -->
{toc_html}

<!-- Report Content -->
<div class="content">
{body_html}
</div>

</body>
</html>"""
    return doc


# Report definitions
reports = [
    {
        "md_path": "/Users/henry/clawd/memory/projects/ell/ag-tech-landscape-2026.md",
        "title": "Ag Tech Competitive Landscape",
        "subtitle": "Market analysis, key players, and opportunity gaps for Elm Lake Labs in the precision agriculture industry",
        "org": "Elm Lake Labs",
        "html_name": "ag-tech-landscape.html",
        "pdf_name": "ag-tech-landscape.pdf",
        "description": "Comprehensive analysis of 50+ ag tech companies across autosteer, farm management, drones, AI analytics, and scouting — with identified opportunity gaps.",
    },
    {
        "md_path": "/Users/henry/clawd/memory/projects/ell/ai-sales-funnel-design.md",
        "title": "AI Sales Funnel Design",
        "subtitle": "A complete playbook for selling FJD Dynamics precision ag products through an AI-powered online sales funnel",
        "org": "Elm Lake Labs",
        "html_name": "ai-sales-funnel.html",
        "pdf_name": "ai-sales-funnel.pdf",
        "description": "Full sales funnel architecture: tractor compatibility tool, AI chatbot, content strategy, paid ads, ROI calculator, and 6-month implementation budget.",
    },
    {
        "md_path": "/Users/henry/clawd/memory/projects/ell/ai-trading-research.md",
        "title": "AI Trading Research",
        "subtitle": "Comprehensive analysis of AI crypto trading bots, commodity hedging strategies, and realistic expectations for retail investors",
        "org": "Elm Lake Labs",
        "html_name": "ai-trading-research.html",
        "pdf_name": "ai-trading-research.pdf",
        "description": "Deep dive into Stoic.ai, Pionex, 3Commas, and 15+ platforms — plus agricultural commodity hedging strategies for cranberry operations.",
    },
    {
        "md_path": "/Users/henry/clawd/memory/projects/elc/hiring-process-improvement.md",
        "title": "Farm Hiring Process Improvement",
        "subtitle": "Wisconsin labor market analysis, recruiting channels, pay benchmarks, and a 90-day action plan for Elm Lake Cranberry",
        "org": "Elm Lake Cranberry",
        "html_name": "hiring-process.html",
        "pdf_name": "hiring-process.pdf",
        "description": "Complete hiring playbook: pay benchmarks, MSTC partnership strategy, H-2A analysis, AI hiring tools, job postings, retention bonuses, and 90-day action plan.",
    },
    {
        "md_path": "/Users/henry/clawd/memory/projects/ell/company-rename-research.md",
        "title": "Company Rename Research",
        "subtitle": "Domain availability analysis, naming patterns, and top 10 recommended company names for Elm Lake Labs",
        "org": "Elm Lake Labs",
        "html_name": "company-rename.html",
        "pdf_name": "company-rename.pdf",
        "description": "300+ domains checked, 10 finalists evaluated — from premium .com acquisitions (Fallow, Tillage, Swath) to free coined alternatives (Culteon, Callivar).",
    },
    {
        "md_path": "/Users/henry/clawd/memory/projects/ell/fjd-dealer-territory-map.md",
        "title": "FJD Dealer Territory Map",
        "subtitle": "Complete US dealer database, competitor analysis, state-by-state territory map, and negotiation strategy for FJD Dynamics dealership expansion",
        "org": "Elm Lake Labs",
        "html_name": "fjd-dealer-map.html",
        "pdf_name": "fjd-dealer-map.pdf",
        "description": "All 50 states mapped — 37 open territories identified. Deep competitive analysis of DST, plus negotiation playbook for claiming 6-state Midwest exclusive.",
    },
]

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # First, try installing markdown if needed
    try:
        import markdown
    except ImportError:
        subprocess.run(["pip3", "install", "--break-system-packages", "markdown"], check=True)
        import markdown
    
    results = []
    
    for report in reports:
        print(f"\n{'='*60}")
        print(f"Processing: {report['title']}")
        print(f"{'='*60}")
        
        # Read markdown
        with open(report["md_path"], "r") as f:
            md_content = f.read()
        
        # Build HTML
        html_content = build_html(
            title=report["title"],
            subtitle=report["subtitle"],
            org=report["org"],
            md_content=md_content,
        )
        
        # Write HTML
        html_path = os.path.join(OUTPUT_DIR, report["html_name"])
        with open(html_path, "w") as f:
            f.write(html_content)
        print(f"  ✅ HTML written: {html_path}")
        
        # Convert to PDF
        pdf_path = os.path.join(OUTPUT_DIR, report["pdf_name"])
        try:
            result = subprocess.run(
                ["weasyprint", html_path, pdf_path],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                size = os.path.getsize(pdf_path)
                size_mb = size / (1024 * 1024)
                print(f"  ✅ PDF generated: {pdf_path} ({size_mb:.1f} MB)")
                results.append((report, size))
            else:
                print(f"  ❌ PDF failed: {result.stderr[:200]}")
                results.append((report, 0))
        except Exception as e:
            print(f"  ❌ PDF error: {e}")
            results.append((report, 0))
    
    # Build index page
    print(f"\n{'='*60}")
    print("Building index page...")
    print(f"{'='*60}")
    build_index(results)
    print("  ✅ Index written")
    
    print("\n🎉 All done!")
    for report, size in results:
        status = f"({size/(1024*1024):.1f} MB)" if size > 0 else "(FAILED)"
        print(f"  • {report['title']} {status}")

def build_index(results):
    """Build the GitHub Pages index.html with a professional dark theme."""
    
    ell_reports = []
    elc_reports = []
    
    for report, size in results:
        entry = {
            "title": report["title"],
            "description": report["description"],
            "pdf": report["pdf_name"],
            "size": f"{size/(1024*1024):.1f} MB" if size > 0 else "N/A",
        }
        if report["org"] == "Elm Lake Cranberry":
            elc_reports.append(entry)
        else:
            ell_reports.append(entry)
    
    def render_cards(entries):
        cards = ""
        for e in entries:
            cards += f"""
            <div class="card">
                <h3>{html_module.escape(e['title'])}</h3>
                <p>{html_module.escape(e['description'])}</p>
                <div class="card-footer">
                    <a href="{e['pdf']}" class="download-btn">📄 Download PDF</a>
                    <span class="file-size">{e['size']}</span>
                </div>
            </div>
            """
        return cards
    
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Elm Lake Labs — Research Reports • February 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0a0f1a;
    color: #e2e8f0;
    min-height: 100vh;
}}

.container {{
    max-width: 900px;
    margin: 0 auto;
    padding: 4rem 2rem;
}}

header {{
    text-align: center;
    margin-bottom: 4rem;
}}

header h1 {{
    font-size: 2.2rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
}}

header .subtitle {{
    font-size: 1rem;
    font-weight: 300;
    color: #94a3b8;
    margin-bottom: 1.5rem;
}}

header .divider {{
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #1e3a5f);
    margin: 0 auto;
    border-radius: 2px;
}}

.section-title {{
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #64748b;
    margin-bottom: 1.5rem;
    margin-top: 3rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e293b;
}}

.card {{
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    transition: all 0.2s ease;
}}

.card:hover {{
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(59, 130, 246, 0.1);
}}

.card h3 {{
    font-size: 1.15rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 0.6rem;
}}

.card p {{
    font-size: 0.9rem;
    color: #94a3b8;
    line-height: 1.6;
    margin-bottom: 1.2rem;
}}

.card-footer {{
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.download-btn {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.5rem 1.2rem;
    background: #1e3a5f;
    color: #e2e8f0;
    border-radius: 8px;
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 500;
    transition: all 0.2s ease;
}}

.download-btn:hover {{
    background: #2563eb;
    color: white;
}}

.file-size {{
    font-size: 0.8rem;
    color: #475569;
    font-weight: 400;
}}

footer {{
    text-align: center;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid #1e293b;
    color: #475569;
    font-size: 0.8rem;
}}

footer a {{
    color: #64748b;
    text-decoration: none;
}}

@media (max-width: 640px) {{
    .container {{ padding: 2rem 1rem; }}
    header h1 {{ font-size: 1.6rem; }}
    .card {{ padding: 1.2rem; }}
    .card-footer {{ flex-direction: column; gap: 0.5rem; align-items: flex-start; }}
}}
</style>
</head>
<body>

<div class="container">
    <header>
        <h1>Elm Lake Labs — Research Reports</h1>
        <p class="subtitle">February 2026 &nbsp;·&nbsp; Prepared by Henry Clawson, Executive Assistant</p>
        <div class="divider"></div>
    </header>

    <div class="section-title">Elm Lake Labs Reports</div>
    {render_cards(ell_reports)}

    <div class="section-title">Elm Lake Cranberry Reports</div>
    {render_cards(elc_reports)}

    <footer>
        <p>© 2026 Elm Lake Labs &nbsp;·&nbsp; Reports compiled February 14, 2026</p>
    </footer>
</div>

</body>
</html>"""
    
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, "w") as f:
        f.write(index_html)


if __name__ == "__main__":
    main()

"""
Phase 6: Learning Loop — HTML Rendering
Authorized: FD #28 (24 July 2026)

Renders self-reflection logs and coverage gap reports as HTML.
Claude warm minimalism design — matches existing queue/radar style.
"""
import os, json, re
from jinja2 import Environment, FileSystemLoader, select_autoescape

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
LEARNING_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "learning")
os.makedirs(LEARNING_OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html"]))


def _md_to_html_blocks(md_text: str) -> list:
    """Convert markdown sections to HTML block dicts for Jinja2 rendering.
    Simple V0 parser — handles headings, paragraphs, lists, bold, italic."""
    blocks = []
    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Heading
        if stripped.startswith("# "):
            blocks.append({"type": "h1", "content": stripped[2:]})
        elif stripped.startswith("## "):
            blocks.append({"type": "h2", "content": stripped[3:]})
        elif stripped.startswith("### "):
            blocks.append({"type": "h3", "content": stripped[4:]})

        # Horizontal rule
        elif stripped == "---":
            blocks.append({"type": "hr"})

        # List items
        elif stripped.startswith("- ") or stripped.startswith("* "):
            items = []
            while i < len(lines) and lines[i].strip().startswith(("- ", "* ")):
                item_text = lines[i].strip()[2:]
                # Handle bold: **text**
                item_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item_text)
                # Handle italic: _text_
                item_text = re.sub(r'_(.+?)_', r'<em>\1</em>', item_text)
                # Handle inline code: `text`
                item_text = re.sub(r'`(.+?)`', r'<code>\1</code>', item_text)
                items.append(item_text)
                i += 1
            blocks.append({"type": "list", "items": items})
            continue

        # Metadata line (key: value)
        elif "**" in stripped and ":**" in stripped:
            parts = stripped.split(":**", 1)
            if len(parts) == 2:
                key = parts[0].replace("**", "").strip()
                val = parts[1].strip()
                blocks.append({"type": "meta", "key": key, "value": val})

        # Code block
        elif stripped.startswith("```"):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            blocks.append({"type": "code", "content": "\n".join(code_lines)})

        # Regular paragraph
        else:
            para_lines = []
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(("#", "-", "*", "```", "---")):
                para_lines.append(lines[i].strip())
                i += 1
            para = " ".join(para_lines)
            para = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para)
            para = re.sub(r'_(.+?)_', r'<em>\1</em>', para)
            para = re.sub(r'`(.+?)`', r'<code>\1</code>', para)
            blocks.append({"type": "p", "content": para})
            continue

        i += 1

    return blocks


def render_self_reflection(md_path: str, output_dir: str = None) -> str:
    """Render a self-reflection log markdown file as HTML.

    Args:
        md_path: Path to the markdown file
        output_dir: Output directory (default: output/learning/)

    Returns:
        Path to the generated HTML file.
    """
    if output_dir is None:
        output_dir = LEARNING_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    blocks = _md_to_html_blocks(md_text)

    # Build HTML content
    html_parts = []
    for block in blocks:
        t = block["type"]
        if t == "h1":
            html_parts.append(f'<h1>{block["content"]}</h1>')
        elif t == "h2":
            html_parts.append(f'<h2>{block["content"]}</h2>')
        elif t == "h3":
            html_parts.append(f'<h3>{block["content"]}</h3>')
        elif t == "hr":
            html_parts.append('<hr>')
        elif t == "meta":
            html_parts.append(f'<div class="meta"><strong>{block["key"]}:</strong> {block["value"]}</div>')
        elif t == "list":
            items_html = "".join(f"<li>{item}</li>" for item in block["items"])
            html_parts.append(f"<ul>{items_html}</ul>")
        elif t == "code":
            html_parts.append(f'<pre><code>{block["content"]}</code></pre>')
        elif t == "p":
            html_parts.append(f'<p>{block["content"]}</p>')

    content_html = "\n".join(html_parts)

    # Use base template
    base_template = env.get_template("base.html")
    html = base_template.render(
        pipeline_version="learning-v0.1.0",
        run_id=os.path.basename(md_path).replace(".md", ""),
        point_in_time="",
        fixture_category="LEARNING LOOP — AI-generated draft",
    )
    # Inject content after <main> or <body>
    html = html.replace("{% block content %}{% endblock %}",
                         f"<div class=\"page\">{content_html}</div>")
    html = html.replace("{% block title %}{% endblock %}",
                         "Self-Reflection Log | Learning Loop")

    filename = os.path.basename(md_path).replace(".md", ".html")
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath


def render_learning_dashboard(reflection_md_path: str, gap_report_md_path: str = None,
                               output_dir: str = None) -> dict:
    """Render the full learning dashboard: reflection + gaps.

    Returns dict with file paths.
    """
    outputs = {}

    # Reflection
    if reflection_md_path and os.path.exists(reflection_md_path):
        outputs["reflection"] = render_self_reflection(reflection_md_path, output_dir)

    # Gap report
    if gap_report_md_path and os.path.exists(gap_report_md_path):
        outputs["gaps"] = render_self_reflection(gap_report_md_path, output_dir)

    return outputs

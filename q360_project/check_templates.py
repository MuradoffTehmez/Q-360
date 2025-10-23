from pathlib import Path
import re
base = Path(r"C:/lahiyeler/q360/q360_project")
templates_dir = base / 'templates'
missing = set()
for py in base.rglob('*.py'):
    try:
        text = py.read_text(encoding='utf-8')
    except Exception:
        continue
    for match in re.finditer(r"render\(\s*request\s*,\s*['\"]([^'\"]+)['\"]", text):
        template = match.group(1)
        if not (templates_dir / Path(template)).exists():
            missing.add((str(py.relative_to(base)), template))
    for match in re.finditer(r"TemplateView\.as_view\(template_name=['\"]([^'\"]+)['\"]", text):
        template = match.group(1)
        if not (templates_dir / Path(template)).exists():
            missing.add((str(py.relative_to(base)), template))
for src, tmpl in sorted(missing):
    print(f"{src}: {tmpl}")

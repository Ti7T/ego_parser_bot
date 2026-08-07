from jinja2 import Template

def load_svg_text(path : str):
  with open(path, "r", encoding="utf-8") as f:
    return Template(f.read())
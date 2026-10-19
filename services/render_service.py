from templates import load_template
from io import BytesIO
from pathlib import Path
from typing import Any
import resvg_py

BASE_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = BASE_DIR / "fonts" / "Inter.ttf"

def svg_to_png(svg: str) -> BytesIO:
    png_bytes = resvg_py.svg_to_bytes(
        svg_string=svg,
        font_files=[str(FONT_PATH)],
    )
    return BytesIO(png_bytes)

def render_svg(template_name: str, data: dict[str, Any]) -> str:
    template = load_template(template_name)
    return template.render(**data)
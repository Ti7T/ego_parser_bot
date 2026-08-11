from jinja2 import Environment, FileSystemLoader, Template

envir = Environment(
    loader=FileSystemLoader("templates"), 
    auto_reload=True
)

def load_template(template_name: str) -> Template:
    """Возвращает шаблон из папки templates с кэшированием."""
    try:
        return envir.get_template(template_name)
    except Exception as e:
        raise RuntimeError(f"Не удалось загрузить шаблон {template_name}") from e

if __name__ == "__main__":
    template = load_template("profile_card.svg")
    svg_content = template.render(username="Alice", level=42)
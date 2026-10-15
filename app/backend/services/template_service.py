import os
from pathlib import Path, PurePosixPath

from jinja2 import Environment, FileSystemLoader, StrictUndefined

MODULE_PATH = Path(__file__).resolve()

if len(MODULE_PATH.parents) > 2:
    DEFAULT_TEMPLATE_DIR = MODULE_PATH.parents[2] / "data" / "network" / "templates"
else:
    DEFAULT_TEMPLATE_DIR = Path("/data/network/templates")

TEMPLATE_DIR = Path(os.getenv("TEMPLATE_DIR", str(DEFAULT_TEMPLATE_DIR)))

template_environment = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    undefined=StrictUndefined,
    autoescape=False,
    keep_trailing_newline=True,
)


def render_template(
    template_name: str,
    variables: dict,
) -> str:
    """Render a Jinja2 network configuration template."""

    path = PurePosixPath(template_name)

    if (
        path.is_absolute()
        or ".." in path.parts
        or path.suffix != ".j2"
        or not path.parts
    ):
        raise ValueError("Invalid template path.")

    template = template_environment.get_template(path.as_posix())

    return template.render(**variables)

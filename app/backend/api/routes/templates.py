from typing import Any

from fastapi import APIRouter, HTTPException
from jinja2.exceptions import TemplateError, TemplateNotFound
from pydantic import BaseModel, Field
from services.template_service import render_template

router = APIRouter()


class TemplateRenderRequest(BaseModel):
    template_name: str = Field(min_length=1, max_length=200)
    variables: dict[str, Any]


@router.post("/templates/render")
def render_network_template(request: TemplateRenderRequest):
    try:
        configuration = render_template(
            request.template_name,
            request.variables,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except TemplateNotFound as exc:
        raise HTTPException(
            status_code=404,
            detail="Template not found.",
        ) from exc
    except TemplateError as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Template rendering failed: {exc}",
        ) from exc

    return {
        "template_name": request.template_name,
        "configuration": configuration,
    }

from flask import Blueprint

mental_health = Blueprint(
    "mental_health",
    __name__,
    template_folder="templates",
    static_folder="static"
)

from . import routes

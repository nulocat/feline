
from jinja2 import Environment, FileSystemLoader, Template

from feline.http.response import Response
from feline.context import context


def render(template_name, **template_vars) -> Response:
    template_root = str(object=context.config.templates_path)

    env = Environment(loader=FileSystemLoader(searchpath=template_root))

    template: Template = env.get_template(name=template_name)

    return Response().html(template.render(request=context.request,**template_vars))

from inspect import Signature, signature, Parameter
from typing import get_args, get_origin, Annotated
from feline.routing.parameters import Body, Form, Query
from feline.http.request import Request
from feline.context import context
from feline.exceptions import InvalidParameterResolution


def get_params(fn) -> dict[str, Parameter]:
    sig: Signature = signature(fn)
    return dict(sig.parameters)


def extract_annotation(param: Parameter):
    """Retorna o tipo real e os metadados, caso Annotated seja usado."""
    annotation = param.annotation
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        real_type = args[0]
        metadata = args[1:]
        return real_type, metadata
    return annotation, []


async def resolver_arguments(fn) -> dict:
    params = get_params(fn)

    request_obj = context.request
    arguments = {}

    form_data = None
    json_data = None
    form_error = False
    json_error = False

    for name, param in params.items():
        annotation_type, metadata = extract_annotation(param)

        # Combina os metadados de Annotated com o default
        source_hint = None
        for meta in metadata:
            if isinstance(meta, (Query, Form, Body)):
                source_hint = meta
                break
        if isinstance(param.default, (Query, Form, Body)):
            source_hint = param.default

        # if is request give to her
        if name == "request" or annotation_type is Request:
            arguments[name] = request_obj

        elif isinstance(source_hint, Body):
            try:
                if source_hint.type == "JSON":
                    if json_data is None and not json_error:
                        try:
                            json_data = await request_obj.json
                        except:
                            json_error = True
                    arguments[name] = (
                        json_data.get(name, source_hint.default)
                        if json_data
                        else source_hint.default
                    )

                elif source_hint.type == "TEXT":
                    arguments[name] = await request_obj.text

            except:
                raise InvalidParameterResolution(
                    request_obj,
                    name,
                    f"body with {source_hint.type}",
                    await request_obj.text,
                )

        elif isinstance(source_hint, Form):
            if form_data is None and not form_error:
                try:
                    form_data = await request_obj.form
                except:
                    form_error = True
            if not form_error and form_data is not None:
                arguments[name] = form_data.get(name, source_hint.default)

        elif isinstance(source_hint, Query):
            arguments[name] = request_obj.args.get(name, source_hint.default)

        else:
            value = request_obj.args.get(name)

            if value is None and json_data is None and not json_error:
                try:
                    json_data = await request_obj.json
                except:
                    json_error = True

            if value is None and json_data:
                value = json_data.get(name)

            if value is None and form_data is None and not form_error:
                try:
                    form_data = await request_obj.form
                except:
                    form_error = True

            if value is None and form_data:
                value = form_data.get(name)

            if value is None:
                raise InvalidParameterResolution(
                    request_obj, name, "query, form or json", "nothing"
                )

            arguments[name] = value

        if arguments.get(name) is None:
            expected_from = (
                source_hint.__class__.__name__.lower()
                if source_hint
                else "query, form or json"
            )

            raise InvalidParameterResolution(
                request_obj,
                name,
                f"required parameter from {expected_from}",
                "None (no value provided and no default set)",
            )

    return arguments

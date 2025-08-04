from inspect import Parameter, signature
from typing import Annotated, get_args, get_origin

from feline.context import context
from feline.exceptions import InvalidParameterResolution

def get_params(fn):
    return dict(signature(fn).parameters)


def get_annotation_type(param: Parameter):
    ann = param.annotation
    if get_origin(ann) is Annotated:
        return get_args(ann)[0]
    return ann if ann != Parameter.empty else str


def cast_value(value, to_type):
    if value is None:
        return None
    try:
        if to_type == bool:
            return str(value).lower() in ("1", "true", "yes", "on")
        return to_type(value)
    except:
        return None


async def resolver_arguments(fn):
    params = get_params(fn)
    req = context.request
    args = {}

    form = None
    json = None

    for name, param in params.items():
        if name == "request" or name == "req" or name == "REQUEST":
            args[name] = req
            continue

        expected_type = get_annotation_type(param)
        default = param.default if param.default != Parameter.empty else None

        value = req.args.get(name)

        if value is None:
            if json is None:
                try:
                    json = await req.json
                except:
                    json = {}
            value = json.get(name)

        if value is None:
            if form is None:
                try:
                    form = await req.form
                except:
                    form = {}
            value = form.get(name)

        if value is None:
            if default is not None:
                args[name] = default
                continue
            raise InvalidParameterResolution(req, name, "query/form/json", "missing")

        casted = cast_value(value, expected_type)
        if casted is None:
            raise InvalidParameterResolution(req, name, expected_type.__name__, value)

        args[name] = casted

    return args

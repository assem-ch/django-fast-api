from functools import wraps
from typing import Iterable

from django.db.models import Model, QuerySet
from django.db.models.query import RawQuerySet
from django.template.response import TemplateResponse
from djangorestframework_camel_case.parser import (
    CamelCaseFormParser,
    CamelCaseJSONParser,
    CamelCaseMultiPartParser,
)
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from prodict import Prodict
from rest_framework import serializers
from rest_framework.decorators import (
    api_view,
    parser_classes,
    permission_classes,
    renderer_classes,
)
from rest_framework.response import Response


def update_dict(d, u):
    import collections.abc

    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            if isinstance(v, list) and len(v) == 1:
                d[k] = v[0]
            else:
                d[k] = v
    return d



def parse_url_objects(param, value):
    import re

    reg = re.compile(
        r"(?P<level0>[^\[^\]]+)(?:(?:\[(?P<level1>[^\[\]]+)\])(?:\[(?P<level2>[^\[\]]+)\])?)?"
    )
    match = reg.match(param)
    d = {}
    if match:
        level1, level2, level3 = match.groups()
        if not level2:
            d[level1] = value
        elif level2 and not level3:
            d[level1] = {level2: value}
        else:
            d[level1] = {level2: {level3: value}}
    print(d)
    return d


def omittable_parentheses(maybe_decorator=None, /, allow_partial=False):
    """A decorator for decorators that allows them to be used without parentheses"""

    def decorator(func):
        @wraps(decorator)
        def wrapper(*args, **kwargs):
            if len(args) == 1 and callable(args[0]):
                if allow_partial:
                    return func(**kwargs)(args[0])
                elif not kwargs:
                    return func()(args[0])
            return func(*args, **kwargs)

        return wrapper

    if maybe_decorator is None:
        return decorator
    else:
        return decorator(maybe_decorator)


def get_serializer(model, fields="__all__"):
    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            pass

        Meta.model = model
        Meta.fields = fields

    return GenericSerializer



def build_params(request_serializer, response_serializer, query_params):
    if not query_params:
        query_params = []
    params = {}
    manual_params = []
    for query_param in query_params:
        manual_params.append(
            OpenApiParameter(
                name=query_param,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                default="",
            ),
        )

    params["request"] = request_serializer or dict

    params["parameters"] = manual_params
    params["responses"] = {"200": response_serializer or dict}
    return params


class APIRouter:
    def __init__(self, prefix=None, tags=tuple()):
        self.prefix = prefix or ""
        self.urls = []
        self.tags = tags or (prefix and [prefix.strip("/")])

    @omittable_parentheses(allow_partial=True)
    def api(
        self,
        path=None,
        query_params_for_docs_only=None,
        permissions=tuple(),
        methods=("post",),
        renderers=(CamelCaseJSONRenderer,),
        template=None,
        parsers=(CamelCaseJSONParser, CamelCaseFormParser, CamelCaseMultiPartParser),
        tags=None,
    ):
        def decorator(func):
            req_serializer = getattr(
                func, "__annotations__", {}
            ).get("req")
            res_serializer = getattr(
                func, "__annotations__", {}
            ).get("return")

            @wraps(func)
            @extend_schema(
                methods=methods,
                tags=tags or self.tags,
                **build_params(
                    req_serializer,
                    res_serializer,
                    query_params=query_params_for_docs_only,
                ),
            )
            @api_view(methods)
            @renderer_classes(renderers)
            @permission_classes(permissions)
            @parser_classes(parsers)
            def decorated(request, **kwargs):

                args = {}
                request_data = request.data
                request_get = {}
                for param in request.GET:
                    update_dict(
                        request_get,
                        parse_url_objects(param, request.GET.getlist(param)),
                    )
                request_files = request.FILES
                data = {**request_get, **request_data, **request_files, **kwargs}
                print(data)
                decorated_args = set(
                    func.__code__.co_varnames[: func.__code__.co_argcount]
                )

                if func.__code__.co_argcount:
                    if "req" in decorated_args:
                        if req_serializer and "file" not in req_serializer().fields:
                            serializer_data = req_serializer(data=data)
                            serializer_data.is_valid(raise_exception=True)
                            data = serializer_data.data



                        request.args = Prodict(data)
                        args['req'] = request

                raw_data = func(**args)

                if res_serializer:
                    response_data = res_serializer(raw_data).data
                elif isinstance(raw_data, QuerySet):
                    response_data = get_serializer(raw_data.model)(
                        raw_data, many=True
                    ).data
                elif isinstance(raw_data, RawQuerySet):
                    response_data = get_serializer(
                        raw_data.model, fields=raw_data.columns
                    )(raw_data, many=True).data
                elif isinstance(raw_data, Model):
                    response_data = get_serializer(type(raw_data))(raw_data).data
                else:
                    response_data = raw_data

                if template:
                    return TemplateResponse(request, template, response_data)
                return Response(response_data)

            if path:
                from django import urls

                if isinstance(path, str):
                    paths = [path]
                elif isinstance(path, Iterable):
                    paths = path
                else:
                    paths = []
                for p in paths:
                    self.urls.append(urls.path(f"{self.prefix}{p}", decorated))

            return decorated

        return decorator

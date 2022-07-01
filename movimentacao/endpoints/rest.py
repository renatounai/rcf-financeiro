from http import HTTPStatus
from typing import List

from django.db import models
from django.shortcuts import get_object_or_404
from ninja import Schema, Router

from utils.api_utils import dict_to_model


def get_one(router: Router, model, out_schema):
    @router.get("/{pk}", response={HTTPStatus.OK: out_schema})
    def get_internal(_, pk):
        return get_object_or_404(model, id=pk)


def delete(router: Router, model):
    @router.delete("/{pk}", response={HTTPStatus.OK: None})
    def delete_internal(_, pk):
        get_object_or_404(model, id=pk).delete()


def put(router: Router, model, schema_in, schema_out):
    @router.put("/{pk}", response={HTTPStatus.OK: schema_out})
    def put_internal(_, pk, body: schema_in):
        m = get_object_or_404(model, id=pk)
        dict_to_model(body.dict(), m)
        m.save()
        return m


def get_all(router: Router, model, out_schema):
    @router.get("/", response={HTTPStatus.OK: List[out_schema]})
    def get_all_internal(_):
        return model.objects.all()


def post(router: Router, model, schema_in, schema_out):
    @router.post("/", response={HTTPStatus.CREATED: schema_out})
    def post_internal(_, body: schema_in):
        m = model(**body.dict())
        m.save()
        return m


def create_crud(router: Router, model: models.Model, schema_in: Schema, schema_out: Schema):
    get_one(router, model, schema_out)
    get_all(router, model, schema_out)
    post(router, model, schema_in, schema_out)
    put(router, model, schema_in, schema_out)
    delete(router, model)

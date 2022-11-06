from bson.objectid import ObjectId
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.generics import get_object_or_404


class CreateModelMixin:

    def __init__(self, *args, **kwargs):
        """ Custome Create Model Mixins Views Instance """
        super(CreateModelMixin, self).__init__(*args, **kwargs)
        self.create_responser = {"code": 0, "error": False, 'detail': 'request create object success', 'data': {}}

    def create(self, request, *args, **kwargs):
        """ create Method Will Save Data """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.create_responser['data'] = serializer.data
        return Response(self.create_responser)

    def perform_create(self, serializer):
        """ perform_create Method Will Save Request Data To DB"""
        serializer.save()

    def get_success_headers(self, data):
        """ get_success_headers Will Location to new address"""
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:

    def __init__(self, *args, **kwargs):
        """ Custome List Model Mixins Views Instance """
        super(ListModelMixin, self).__init__(*args, **kwargs)
        self.list_responser = {"code": 0, "error": False, 'detail': 'request list object success', 'data': {}}

    def list(self, request, *args, **kwargs):
        """ list Method Will List Data """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        self.list_responser['data'] = serializer.data
        return Response(self.list_responser)


class UpdateModelMixin:

    def __init__(self, *args, **kwargs):
        """ Custome Update Model Mixins Views Instance """
        super(UpdateModelMixin, self).__init__(*args, **kwargs)
        self.update_responser = {"code": 0, "error": False, 'detail': 'update object success', 'data': {}}

    def update(self, request, *args, **kwargs):
        """ update Method Will List Data """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        self.update_responser['data'] = serializer.data
        return Response(self.update_responser)

    def perform_update(self, serializer):
        """ perform_update Method Will Save Request Data To DB"""
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def __init__(self, *args, **kwargs):
        super(RetrieveModelMixin, self).__init__(*args, **kwargs)
        self.retrive_responser = {"code": 0, "error": False, 'detail': 'retrive object success', 'data': {}}

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.retrive_responser['data'] = serializer.data
        return Response(self.retrive_responser)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def __init__(self, *args, **kwargs):
        super(DestroyModelMixin, self).__init__(*args, **kwargs)
        self.delete_responser = {"code": 0, "error": False, 'detail': 'delete object success', 'data': {}}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(self.delete_responser)

    def perform_destroy(self, instance):
        instance.delete()
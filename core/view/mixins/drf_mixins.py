# -*- coding:utf-8 -*-
#
# Copyright © 2020,  BadSky
# Author Badskyer
# Email  badskyer@fireunix.net
# All rights reserved.
#
# Redistribution and use in source and binary params, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of TrustCentric nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


# import line_profiler
from rest_framework.response import Response
from rest_framework.settings import api_settings

# profile = line_profiler.LineProfiler()


class CreateModelMixin:

    def __init__(self, *args, **kwargs):
        """ Custome Create Model Mixins Views Instance """
        super(CreateModelMixin, self).__init__(*args, **kwargs)
        self.create_responser = {"code": 0, "error": False, 'detail': 'request create object success', 'data': {}}

    def create(self, request, *args, **kwargs):
        """ create Method Will Save Data """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.before_create(request, serializer)
        self.perform_create(serializer)
        self.after_create(request, serializer)
        self.create_responser['data'] = serializer.data
        return Response(self.create_responser)

    def before_create(self, request, serializer):
        pass

    def after_create(self, request, serializer):
        pass

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

    def get_paged_queryset(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        return page


    def get_list_data(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return queryset,page, serializer.data
        serializer = self.get_serializer(queryset, many=True)
        return queryset, page, serializer.data

    def list(self, request, *args, **kwargs):
        """ list Method Will List Data """
        queryset,page, data = self.get_list_data(request, *args, **kwargs)
        if page is not None:
            return self.get_paginated_response(data)
        self.list_responser['data'] = data
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
        self.before_update(request, serializer, instance)
        self.perform_update(serializer)
        self.after_update(request, serializer, instance)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        self.update_responser['data'] = serializer.data
        return Response(self.update_responser)

    def before_update(self, request, serializer, instance):
        pass

    def after_update(self, request, serializer, instance):
        pass

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
        self.before_destroy(request, instance)
        self.perform_destroy(instance)
        self.after_destroy(request, instance)
        return Response(self.delete_responser)

    def before_destroy(self, request, instance):
        pass

    def after_destroy(self, request, instance):
        pass

    def perform_destroy(self, instance):
        instance.delete()


class SmartDestroyModelMixn:
    """
    Destroy a model instance.
    """

    def __init__(self, *args, **kwargs):
        super(SmartDestroyModelMixn, self).__init__(*args, **kwargs)
        self.delete_responser = {"code": 0, "error": False, 'detail': 'delete object success', 'data': {}}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_delete_perm(instance)
        self.perform_destroy(instance)
        return Response(self.delete_responser)

    def perform_destroy(self, instance):
        model = instance.__class__
        model.objects.smart_delete(instance)


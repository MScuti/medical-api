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

""" Dynamic resource and common resource setting model, Dynamic resource attr
now display is limited, mode detail: https://li.feishu.cn/wiki/wikcnbCcRankKUlvxuh0GN89E0f#
"""

import copy
from django.db import models
from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet
from django.core.exceptions import ObjectDoesNotExist

from apps.common.models import Resources
from core.view.const import MODEL_FIELD_MAP
from core.exceptions import ResourceNotExists, ResourceUnknownError, DymaticFiledTypeMetaError
from core.view.mixins.drf_dymatic_mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, \
    RetrieveModelMixin, DestroyModelMixin


class VirtrualSerializer(serializers.ModelSerializer):
    """ Basic virtrual serializer template, do not use this directly,
    it is not thread safe, just use deepcopy !
    """

    class Meta:
        fields = "__all__"


class CreateVirtrualResource:
    """ Create Virtrual `Model` and Virtraul `ModelSerializer` to
    support `rest framework`, Virtrual `Model` now  support  data
    type limited, other problem is warnning show when call this
    class more than one time, but no effect for system.
    :arg
        model: Django Model instance, default is None if not create.
        serializer_cls: ModelSerializer instance, default is None if not create.
        RESOURCE_ID_NAME: customize resource filed name for request.
    """
    model = None
    serializer_cls = None
    RESOURCE_ID_NAME = 'resource_id'

    def get_resource(self):
        """ Get resource object by `RESOURCE_ID_NAME`, if resource is not
        exists in database, `ResourceNotExists` will raise.
        :exception              ResourceNotExists, ResourceUnknownError
        :rtype:                 Resources instance
        :return:                resource instance if resouce is regsitered
        """
        try:
            resource_id = self.kwargs.get(self.RESOURCE_ID_NAME)
            return Resources.objects.get(pk=resource_id)
        except ObjectDoesNotExist:
            raise ResourceNotExists("resource not found by id:{}".format(resource_id))
        except Exception:
            raise ResourceUnknownError()

    def parser_field(self, field_meta):
        """ Get field options from Mode Maped Fields, now support
        fields only include `int`, `str`, `text`, `float`, `datetime`.
        above options is limited!
        :param field_meta:         field dispaly type meta
        :return:                   field maped field and defualt options
        """
        if not field_meta:
            raise DymaticFiledTypeMetaError
        return field_meta['field'], field_meta['options']

    def update_field_options(self, attr, options):
        """ Update Django `field` initiallize options, now support options
        is limited, only basic options is support.
        :param attr:         resource attr object
        :param options:      field default options
        :return:             updated options
        :rtype:              dict
        """
        if attr.allow_empty and 'null' in options.keys():
            options['null'] = True
        if attr.allow_empty and 'blank' in options.keys():
            options['blank'] = False
        return options

    def get_model_fields(self, resource):
        """ Get model fields and map field to Django `Field` object  with
        basic options.
        :param resource:      resource instance
        :return:              list of field dict with name and `Field` object
        :rtype                list
        """
        model_fields = []
        attrs = resource.resourceattrs_set.filter(is_valid=1)
        for attr in attrs:
            field_name = attr.filed_name
            field_display_type = attr.attr_type.display_type
            filed_meta = MODEL_FIELD_MAP.get(field_display_type, None)
            field, options = self.parser_field(filed_meta)
            options = self.update_field_options(attr, options)
            model_fields.append(dict(name=field_name, obj=field(**options)))
        return model_fields

    def get_model(self):
        """ Create model dymatic, there use metaclass to create model, avoid
        raise exceptoins.
        :arg
            bind_attrs:             Field attrs will bind to Django Model create by `type`
            resource:               Custome resource instance.
            model_fileds:           Resource attr map to model field.
        :return:                    Resource model instance.
        :rtype:                     cls
        """
        bind_attrs = {}
        resource = self.get_resource()
        model_fileds = self.get_model_fields(resource)

        class Meta:
            """ Django Model Class """
            managed = False
            app_label = 'common'
            db_table = resource.db_table

        bind_attrs['Meta'] = Meta
        bind_attrs['__module__'] = ''
        for field in model_fileds:
            bind_attrs[field['name']] = field['obj']
        self.model = type('VirtrualModel', (models.Model,), bind_attrs)
        self.get_serializer_cls()
        return self.model

    def get_serializer_cls(self):
        """ Create drf serializer dymatic, the serializer type is `ModelSerializer`,
        since type is `ModelSerializer`, need create Django Model first.
        :return:                    Resource serilazer class.
        :rtype:                     cls
        """
        if self.serializer_cls:
            return self.serializer_cls
        if not self.model:
            self.get_model()
        serializer = copy.deepcopy(VirtrualSerializer)
        setattr(serializer.Meta, 'model', self.model)
        self.serializer_cls = serializer
        return serializer


class CustomResourceViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin,
                            RetrieveModelMixin, DestroyModelMixin, GenericViewSet, CreateVirtrualResource):

    def get_queryset(self):
        model = self.model if self.model else self.get_model()
        return model.objects.all()

    def get_serializer_class(self):
        return self.serializer_cls if self.serializer_cls else self.get_serializer_cls()

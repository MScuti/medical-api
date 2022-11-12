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

""" user rest api """
from django.contrib.auth import authenticate


import uuid
from . import errors
from . import serializer
from apps.user import models
from core.view import DRFBaseView
from rest_framework.response import Response



class UserViewSet(DRFBaseView):
    """ User ViewSet
    Author:        balinchao(badskyer@fireunix.net)
    Date:          2022-11-05  15:00
    User ViewSet, support request method blow:
    create(POST):   '/api/${version}/user/'               create new user.
    update(PATCH):  '/api/${version}/user/${pk}/'         update user.
    retrieve(GET):  '/api/${version}/user/${pk}/'         get user detail.
    list(GET):      '/api/${version}/user/'               get user list.
    delete(DELETE): '/api/${version}/user/${pk}/'         delete user.
    """
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_list = serializer.user_serializers
    queryset = models.User.objects.filter()


class LoginViewSet(DRFBaseView):

    def create(self, request, *args, **kwargs):
        data = request.data
        serializers = serializer.LoginSerialzer(data=data)
        serializers.is_valid(raise_exception=True)
        u_name = request.data.get('username')
        u_password = request.data.get('password')
        user = authenticate(username=u_name, password=u_password)
        if user is not None:
            # 获取唯一标识码
            token = uuid.uuid4()
            user.token = token
            user.save()
            self.create_responser['data'] = {"token": token}
            return Response(self.create_responser)
        else:
            raise errors.LoginError("用户名或密码输入错误!")


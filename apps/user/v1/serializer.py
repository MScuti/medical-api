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

""" User serialzier, more detail: https://lmwdvqokez.feishu.cn/wiki/wikcnTDaVNgkh0KuCvHqaC72Vxd """

from rest_framework import serializers
from apps.user import models


class LoginSerialzer(serializers.Serializer):
    """用户登录"""

    username = serializers.CharField(allow_null=False, max_length=32)
    password = serializers.CharField(allow_null=False, max_length=32)



# User serializers, include: create, update, list, detail
class UserCreateSerializer(serializers.ModelSerializer):
    """ User Create Serializer """

    class Meta:
        model = models.User
        exclude = ('add_time', 'update_time')


class UserUpdateSerializer(serializers.ModelSerializer):
    """ User Update Serializer """

    class Meta:
        model = models.User
        exclude = ('add_time', 'update_time')


class UserDetailSerializer(serializers.ModelSerializer):
    """ User Detail Serializer """

    class Meta:
        model = models.User
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    """ User List Serializer """

    class Meta:
        model = models.User
        fields = '__all__'


user_serializers = {
    "create": UserCreateSerializer,
    'list': UserListSerializer,
    'retrieve': UserDetailSerializer,
    'partial_update': UserUpdateSerializer
}

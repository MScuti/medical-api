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

import jwt
import json
import logging
import base64
from jose import jws, jwe
from core import requests
from django.conf import settings
from django.core.cache import cache
from apps.users.models import Staff
from apps.oauth.models import APIAuth
from jwcrypto import jwe, jwk


logger = logging.getLogger('user.authentication')


class User:
    user_id = None
    user_name = ''
    avatar = ''
    is_active = False
    is_anonymous = True
    is_authenticated = False
    is_it_department = False
    is_allow_department = False

class Authentication:

    def __init__(self, get_response):
        self.get_response = get_response
    def get_decrypt_signature(self):
        secret_decode = json.loads(base64.b64decode(settings.IDAAS_SECRET + '=' * (-len(settings.IDAAS_SECRET) % 4)))
        return secret_decode['k']

    def get_decrypt_key(self, user_token, signature):
        meta = user_token.split('.')[0]
        decode_meta = json.loads(base64.b64decode(meta + '=' * (-len(meta) % 4)))['enc']
        keyjson = {"kty": "oct", "alg": decode_meta, "k": signature}
        keyjsonstr = json.dumps(keyjson)
        key = jwk.JWK.from_json(keyjsonstr)
        return key

    def parse_jwt_token(self, token):
        result = jwt.decode(token, options={"verify_signature": False})
        return result

    def parse_user_info(self, user_token):
        signature = self.get_decrypt_signature()
        key = self.get_decrypt_key(user_token, signature)
        jwetoken = jwe.JWE()
        jwetoken.deserialize(user_token, key)
        return json.loads(jwetoken.payload)



    def read_cache_user(self, token):
        """ Read user from cache, if user information is cached, user will
        returned, else None will returned.
        :param token(str):         user authencation token.
        :return(object|None):      user instance or None.
        """
        user = cache.get(token)
        logger.info("try get user object from cache by token:{}, user is:{}".format(token,user))
        return user

    def get_user_avator(self, staff_id):
        """ Get user avatar by staff id, only be called when user is company
        user, service user will never be called.
        :param staff_id(int):     user primary key.
        :return(str):             user avator url or emtry str.
        """
        staff_query = Staff.objects.filter(id=staff_id)
        avatar_address =  staff_query.first().avatar if staff_query.exists() else ''
        logger.info("get user avatar address by staff primary key:{}, result:{}".format(staff_id, avatar_address))
        return avatar_address

    def get_company_user(self, token):
        """ Get `LiXiang` company staff informaton by `token`
        :param token(str):  user authencation token.
        :return(object):    user instance.
        """
        auth_user = User()
        decode_token = self.parse_jwt_token(token)
        user_info = self.parse_user_info(decode_token['sub'])
        org_name = user_info['leg']
        user_name = user_info['nickname']
        avator = user_info['picture']
        staff = Staff.objects.filter(email=org_name + '@lixiang.com').first()
        auth_user.avator = avator
        auth_user.user_name = user_name
        auth_user.user_id = staff.pk
        auth_user.type = "user"
        auth_user.is_active = True
        auth_user.is_anonymous = False
        auth_user.is_authenticated = True
        auth_user.is_allow_department = True
        cache.set(token, auth_user, settings.CHACHE_TIMEOUT)
        return auth_user
        # try:
        #     response = requests.get(settings.JWT_TOKEN + token)
        #     user = response.json()
        #     auth_user.type = "user"
        #     auth_user.user_name = user['name']
        #     auth_user.user_id = user['staff_id']
        #     auth_user.is_active = True
        #     auth_user.is_anonymous = False
        #     auth_user.is_authenticated = True
        #     auth_user.is_allow_department = True
        #     auth_user.avator = self.get_user_avator(user['staff_id'])
        #     cache.set(token, auth_user, settings.CHACHE_TIMEOUT)
        #     logger.info("get user with token:{} from user center success, user id is:{}".format(token, auth_user.user_id))
        # except:
        #     logger.exception("try to get company user by token:{} from user center with exception.".format(token), exc_info=True)
        # return auth_user

    def get_service_user(self, token):
        """ Get `API Client` service account infomation by `Token`.
        :param token(str):    service authencation token.
        :return(object):      service instance.
        """
        auth_user = User()
        service = APIAuth.objects.filter(token=token).first()
        if not service:
            logger.info("try to get service user by token:{} failed...".format(token))
            return service
        auth_user.avator = ''
        auth_user.type = "service"
        auth_user.is_active = True
        auth_user.is_anonymous = False
        auth_user.user_id = service.id
        auth_user.is_authenticated = True
        auth_user.is_allow_department = True
        auth_user.user_name = service.service_name
        cache.set(token, auth_user, settings.CHACHE_TIMEOUT)
        logger.info("get service user with token:{} from user center success, service id is:{}".format(token, auth_user.user_id))
        return auth_user

    def get_user_by_token(self, token):
        """ Get user by token, user can be company user or
        `API Client` user.
        :param token(str):      user authencation token.
        :return(object):        user instance.
        """
        user = self.read_cache_user(token)
        if user:
            logger.info("get cached user success...")
            return user
        user = self.get_service_user(token)
        if user:
            logger.info("get service user success...")
            return user
        return self.get_company_user(token)

    def __call__(self, request):
        r""" Main Entry for log metrics middleware.
        :param request: `Request` object used for get metrics in `Django` view.
        :rtype: 'Reponse'
        :return: response the view return by view
        """
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            request.user = User()
            response = self.get_response(request)
            return response
        request.user = self.get_user_by_token(token)
        response = self.get_response(request)
        return response

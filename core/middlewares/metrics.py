# -*- coding:utf-8 -*-
#
# Copyright © 2020,  BadSky
# Author BadSkyer
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

import time
import json
import logging
from user_agents import parse

from django.urls import resolve
from django.conf import settings
from django.db import connections
from django.http.request import QueryDict

from apps.users.models import Staff
from apps.oauth.models import APIAuth
from apps.security.models import UserBrowser, RequestLogs


logger = logging.getLogger('metircs')

class MongoMetircs:

    def __init__(self, get_response):
        self.get_response = get_response

    def get_queries(self):
        """ get request sql queries.
        :return:                     list of request queries.
        :rtype:                      list.
        """
        return [{key: connections[key].queries} for key, _ in connections.databases.items()]

    def get_body(self, request):
        """ get request body josn if request body is not empty
        :param request(Request):    request object
        :return:                    request body ditc if request body is valid else {}
        :rtype:                     dict
        """
        try:
            return json.loads(request.body)
        except Exception:
            return {}

    def get_staff(self,request):
        """ get request user
        :param request(Request):    request object
        :return:                    staff pk if user is valid else 0
        :rtype:                     int
        """
        if request.user.is_anonymous:
            return None
        if request.user.type == 'service':
            return None
        return Staff.objects.filter(pk=request.user.user_id).first().pk

    def get_oauth(self,request):
        """ get request user
        :param request(Request):    request object
        :return:                    staff pk if user is valid else 0
        :rtype:                     int
        """
        if request.user.is_anonymous:
            return None
        if request.user.type == 'user':
            return None
        return APIAuth.objects.filter(pk=request.user.user_id).first().pk

    def get_username(self,request):
        """ get request user
        :param request(Request):    request object
        :return:                    staff pk if user is valid else 0
        :rtype:                     int
        """
        if request.user.is_anonymous:
            return ''
        return request.user.user_name

    def get_staff_type(self,request):
        """ get request user
        :param request(Request):    request object
        :return:                    staff pk if user is valid else 0
        :rtype:                     int
        """
        if request.user.is_anonymous:
            return ''
        if request.user.type == 'service':
            return 'API客户端'
        if request.user.type == 'user':
            return '员工'
        return ''

    def get_action(self, request):
        """ get view action by request method
        :param request(Request):    request object
        :return:                    action name if action defiend else `unknown`
        :rtype:                     str
        """
        method = request.method.lower()
        myfunc, myargs, mykwargs = resolve(request.path)
        cls = getattr(myfunc, "cls", None)
        actions_map = getattr(myfunc, 'actions', None)
        if not actions_map:
            return 'unknown'
        action_method = actions_map.get(method, '')
        if not action_method:
            return 'unknown'
        actions_cls = getattr(cls, 'actions_cls', None)
        if not actions_cls:
            return 'unknown'
        return getattr(actions_cls, action_method, 'unknown')

    def get_address(self, request):
        """ get request remote ipv4 address
        :param request(Request):    request object
        :return:                    action name if action defiend else `unknown`
        :rtype:                     str
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    def get_browser(self, request):
        """ get request browser detail by request
        :param request(Request):    request object
        :return:                    `browser` instance
        :rtype:                     object
        """
        browser = {}
        if 'HTTP_USER_AGENT' in request.META.keys():
            user_agent = parse(request.META['HTTP_USER_AGENT'])
            browser['system'] = user_agent.os.family
            browser['browser'] = user_agent.browser.family
            browser['version'] = user_agent.browser.version_string
            browser['system_version'] = user_agent.os.version_string
            browser['is_pc'] = user_agent.is_pc
            browser['is_bot'] = user_agent.is_bot
            browser['is_mobile'] = user_agent.is_mobile
            browser['is_tablet'] = user_agent.is_tablet
            return browser
        browser['system'] = 'unkown'
        browser['browser'] = 'unkown'
        browser['version'] = 'unkown'
        browser['system_version'] = 'unkown'
        browser['is_pc'] = False
        browser['is_bot'] = False
        browser['is_mobile'] = False
        browser['is_tablet'] = False
        return browser

    def collect_request_metrics(self, request):
        r""" Get request metrics by `Request` object.
        :param request: `Request` object used for get metrics in `Django` view.
        :rtype: Tuple
        :return: request start time and metrics
        """
        metrics = {}
        start_time = time.time()
        metrics['scheme'] = request.scheme
        metrics['method'] = request.method
        metrics['action'] = self.get_action(request)
        metrics['address'] = self.get_address(request)
        metrics['staff_id'] = self.get_staff(request)
        metrics['username'] = self.get_username(request)
        metrics['oauth_id'] = self.get_oauth(request)
        metrics['body_data'] = self.get_body(request)
        metrics['request_path'] = request.get_full_path()
        metrics['staff_type'] = self.get_staff_type(request)
        metrics['useragent'] = request.META.get('HTTP_USER_AGENT','')
        metrics['xrequest_id'] = request.META.get('X-REQUEST-ID', '')
        metrics['plantform_env'] =settings.PLANTFORM_ENV
        metrics['plantform_name'] = settings.PLANTFORM_NAME
        metrics['get_data'] = dict(request.GET) if isinstance(request.GET, QueryDict) else request.GET
        metrics['post_data'] = dict(request.POST) if isinstance(request.POST, QueryDict) else request.POST
        return start_time, metrics

    def collect_handler_metrics(self, start_time, metrics, request, response):
        r""" Get request metrics by `Request`, `Reponse` object.
        :param start_time: `start_time` user start request.
        :param metrics: metrics that had collected, used for merge.
        :param request: `Request` object used for get metrics in `Django` view.
        :param response: `Response` object used for get metrics in `Django` view.
        :rtype: dict
        :return: the metric of dict
        """
        browser_info = self.get_browser(request)
        metrics['queries'] = self.get_queries()
        metrics['duration'] =int(float(format(time.time()-start_time, '.3f')) *1000)
        return metrics, browser_info

    def __call__(self, request):
        r""" Main Entry for log metrics middleware.
        :param request: `Request` object used for get metrics in `Django` view.
        :rtype: 'Reponse'
        :return: response the view return by view
        """
        start_time, metrics = self.collect_request_metrics(request)
        response = self.get_response(request)
        metrics['error'] = getattr(response, 'exception', '')
        metrics['exception'] = getattr(response, 'exception_detail', '')
        metrics, browser_info = self.collect_handler_metrics(start_time, metrics, request, response)
        metrics_record_data = {"metircs":metrics,'browser':browser_info}
        logger.info(json.dumps(metrics_record_data).encode("utf-8"))
        return response

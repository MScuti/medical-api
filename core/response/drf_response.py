# -*- coding:utf-8 -*-
#
# Copyright © 2020,  BadSky
# Author Badskyer
# Email  badskyer@fireunix.net
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
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

""" Manager for PangolinUser; PangolinGroup; PangolinProductGroup,
aim to provide more convenients to operate models that releated user.
"""

import logging
import traceback
from copy import deepcopy
# from apps.monitor.models import ErrorLogs
from rest_framework.response import Response
from django.utils.translation import gettext as _
from rest_framework.views import exception_handler

logger = logging.getLogger("error.common")


exception_response = {
    'code': 40000,
    'error': True,
    'data': dict(),
    'detail': _("sorry, there is some error happend in our services, we are solving!")
}

api_error = {
    'code': 40001,
    'error': True,
    'data': dict(),
    'detail': _("some nexpected happend,unservice temporarily unavailable, try again later!")
}

parse_error = {
    'code': 40002,
    'error': True,
    'data': dict(),
    'detail': _("you request data we can not parse, please check our docs and try again!")
}

auth_failed = {
    'code': 40003,
    'error': True,
    'data': dict(),
    'detail': _("you request login or obtain token paire, but no active or valid user found!")
}

not_auth = {
    'code': 40004,
    'error': True,
    'data': dict(),
    'detail': _("you request resource without auth info, please check auth info and try again!")
}

permission_denied = {
    'code': 40005,
    'error': True,
    'data': dict(),
    'detail': _("you request resource but not permission denied, if you think this unnormal, please contact admin!")
}

not_found = {
    'code': 40006,
    'error': True,
    'data': dict(),
    'detail': _("you request resource not found, please check you request and try again!")
}

method_not_allow = {
    'code': 40007,
    'error': True,
    'data': dict(),
    'detail': _("you request method we not allowed, please check our docs and try again!")
}

not_acceptable = {
    'code': 40008,
    'error': True,
    'data': dict(),
    'detail': _("you request with specific headers we not acceptable, please check our docs and try again!")
}

unsupport_media = {
    'code': 40009,
    'error': True,
    'data': dict(),
    'detail': _("you request with unssport media we not acceptable, please check our docs and try again!")
}

throttled = {
    'code': 40010,
    'error': True,
    'data': dict(),
    'detail': _("you had requested too many requests, what means reached our limitation, please try again later!")
}

validate_error = {
    'code': 40011,
    'error': True,
    'data': dict(),
    'detail': _("request data is invalid, please try again!")
}

token_invalid = {
    'code': 40012,
    'error': True,
    'data': dict(),
    'detail': _("request without a valid token, you can obtain a new token with refresh_token!")
}

create_more_error = {
    'code': 40013,
    'error': True,
    'data': dict(),
    'detail': _("request create new object, but server not allow create more objects than limit!")
}

dymatic_resource_error = {
    'code': 40014,
    'error': True,
    'data': dict(),
    'detail': _("request a custome resource but custome resource is not exists!")
}

request_notexists_error = {
    'code': 40016,
    'error': True,
    'data': dict(),
    'detail': _("request a rest api, but not support in backend!")
}

operationa_error = {
    'code': 40017,
    'error': True,
    'data': dict(),
    'detail': _("request success, but database backend error, we are solving!")
}

auth_code_error = {
    'code': 40018,
    'error': True,
    'data': dict(),
    'detail': _("reuqets a jwt token, but auth code is empty!")
}

auth_user_error = {
    'code': 40019,
    'error': True,
    'data': dict(),
    'detail': _("reuqets jwt token by code, auth code may invalid!")
}

user_not_auth_error = {
    'code': 40020,
    'error': True,
    'data': dict(),
    'detail': _("request resource action, but user is not auth!")
}

machine_not_found = {
    'code': 40021,
    'error': True,
    'data': dict(),
    'detail': _("virtual machine is not found in record")
}

machine_power_action_unkown = {
    'code': 40022,
    'error': True,
    'data': dict(),
    'detail': _("virtual machine expect a power action, but acion is unkown")
}

machine_power_action_not_allow = {
    'code': 40023,
    'error': True,
    'data': dict(),
    'detail': _("vritaul can not execute power action in this status")
}

permission_not_allow = {
    'code': 40024,
    'error': True,
    'data': dict(),
    'detail': _("you request api but not allow because no permission")
}

empty_page = {
    'code': 40025,
    'error': True,
    'data': dict(),
    'detail': _("you request api with page params, but no data found.")
}

task_can_not_retry = {
    'code': 40026,
    'error': True,
    'data': dict(),
    'detail': _("task can not retry only failed task support retry.")
}



vmware_machine_not_found = {
    'code': 40028,
    'error': True,
    'data': dict(),
    'detail': _("can not found specific machine.")
}

vmware_template_not_found = {
    'code': 40029,
    'error': True,
    'data': dict(),
    'detail': _("create vm with specific template is not found.")
}

vmware_department_not_found = {
    'code': 40030,
    'error': True,
    'data': dict(),
    'detail': _("create vm with specific virtual department is not found.")
}

vmware_no_free_address = {
    'code': 40031,
    'error': True,
    'data': dict(),
    'detail': _("reate new subnets is conflict with anothor subnets.")
}



permission_denied = {
    'code': 40037,
    'error': True,
    'data': dict(),
    'detail': _("create new machine must specific esxi or cluster, ethier esxi or cluster is not specific.")
}



vmware_no_environment = {
    'code': 40048,
    'error': True,
    'data': dict(),
    'detail': _("create new subnets is conflict with anothor subnets.")
}

vmware_no_gateway = {
    'code': 40049,
    'error': True,
    'data': dict(),
    'detail': _("create new subnets is conflict with anothor subnets.")
}

vmware_no_options = {
    'code': 40050,
    'error': True,
    'data': dict(),
    'detail': _("create new subnets is conflict with anothor subnets.")
}

vmware_no_valid_subnet = {
    'code': 40051,
    'error': True,
    'data': dict(),
    'detail': _("create vmware machine but no valid subnet found")
}


vmware_create_invalid_compute = {
    'code': 40052,
    'error': True,
    'data': dict(),
    'detail': _("create vmware machine must choose an cluster or esxi server.")
}


vmware_create_unkown_error = {
    'code': 40053,
    'error': True,
    'data': dict(),
    'detail': _("create vmware machie with unkown error, please concat admin.")
}

vmware_create_ip_missing = {
    'code': 40054,
    'error': True,
    'data': dict(),
    'detail': _("create vmware with specific ip address, but address not found.")
}


vmware_create_ip_is_used = {
    'code': 40055,
    'error': True,
    'data': dict(),
    'detail': _("create vmware with specific ip address, but address is used.")
}


vmware_create_ip_not_own = {
    'code': 40056,
    'error': True,
    'data': dict(),
    'detail': _("create vmware machine with specific ip address, but ip is not in department.")
}

vmware_create_ip_already_decalared = {
    'code': 40057,
    'error': True,
    'data': dict(),
    'detail': _("create vmware machine with specific ip address, but ip is in multi subnets..")
}

vmware_esxi_not_in_datacenter = {
    'code': 40058,
    'error': True,
    'data': dict(),
    'detail': _("create vmware machine with specific esxi and datacnter, but esxi is not in datacenter.")
}


vmware_cluster_not_in_datacenter = {
    'code': 40059,
    'error': True,
    'data': dict(),
    'detail': _("create vmware machine with specific cluster and datacnter, but cluster is not in datacenter.")
}

vmware_network_not_in_datacenter = {
    'code': 40060,
    'error': True,
    'data': dict(),
    'detail': _("create vmware machine with specific network and datacnter, but network is not in datacenter.")
}

vmware_create_task_not_found = {
    'code': 40061,
    'error': True,
    'data': dict(),
    'detail': _("create vmware machine task type not found in allow task type, please concat admin.")
}

vmware_subnet_not_config = {
    'code': 40062,
    'error': True,
    'data': dict(),
    'detail': _("create vmware machine with subnet is not configed, please concat admin.")
}


rack_delete_not_empty = {
    'code': 40070,
    'error': True,
    'data': dict(),
    'detail': _("try to delete a rack without empty device.")
}


class ErrorResponse(dict):

    def __init__(self, defualt, *args, **kwargs):
        self.default = defualt
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        if key not in self.keys():
            return self.default
        val = super(ErrorResponse, self).__getitem__(key)
        return val

    def __setitem__(self, key, val):
        super(ErrorResponse, self).__setitem__(key, val)


message = ErrorResponse(exception_response)
message['APIException'] = api_error
message['ParseError'] = parse_error
message['AuthenticationFailed'] = auth_failed
message['NotAuthenticated'] = not_auth
message['PermissionDenied'] = permission_denied
message['PermssionDenied'] = permission_denied
message['NotFound'] = not_found
message['Http404'] = not_found
message['MethodNotAllowed'] = method_not_allow
message['NotAcceptable'] = not_acceptable
message['UnsupportedMediaType'] = unsupport_media
message['Throttled'] = throttled
message['InvalidToken'] = token_invalid
message['ValidationError'] = validate_error
message['ObjectExistError'] = create_more_error
message['ResourceNotExists'] = dymatic_resource_error
message['RequestNotAllow'] = request_notexists_error
message['OperationalError'] = operationa_error
message['AuthCodeError'] = auth_code_error
message['UserAuthError'] = auth_user_error
message['UserNotAuthError'] = user_not_auth_error
message['PowerActionUnkown'] = machine_power_action_unkown
message['PowerActionNotAllow'] = machine_power_action_not_allow
message['PermNotAllow'] = permission_not_allow
message['EmptyPage'] = empty_page
message['TaskCanNotRetry'] = task_can_not_retry
message['NewSubnetConflict'] = task_can_not_retry

message['MachineNotFound'] = vmware_machine_not_found
message['TemplateNotFound'] = vmware_template_not_found
message['DepartmentNotFound'] = vmware_department_not_found
message['NoFreeIPAddress'] = vmware_no_free_address
message['NoEnvironmentError'] = vmware_no_environment
message['NoValidGateway'] = vmware_no_gateway
message['NoValidOption'] = vmware_no_options
message['NoValidSubnet'] = vmware_no_valid_subnet
message['NoClusterOrEsxiSpecific'] = vmware_create_invalid_compute
message['MachineCreateUnkownError'] = vmware_create_invalid_compute
message['SpecificIPNotFound'] = vmware_create_ip_missing
message['SpecificIPIsUsed'] = vmware_create_ip_is_used
message['DepartmentNoOwnAddress'] = vmware_create_ip_not_own
message['SameAddressIsDecalared'] = vmware_create_ip_already_decalared
message['ESXINotInDatacenter'] = vmware_esxi_not_in_datacenter
message['ClusterNotInDatacenter'] = vmware_cluster_not_in_datacenter
message['NetworkNotInDatacenter'] = vmware_network_not_in_datacenter
message['CreateVmwareTaskTypeNotFound'] = vmware_network_not_in_datacenter
message['VmwareSubnetsGatewayNotConfig'] = vmware_subnet_not_config
message['DeleteRackNotEmpty'] = rack_delete_not_empty





def handler_exception(exception, context):
    r""" `defualt_excetion_handler` method will custome response error information when exception happend in views.
    :attr exc: `exc` is `Exception` instance catched in the view .
    :attr context: `context` is the request context instance.
    :return: HttpResponse object
    """
    logger.error("uncatched exeception catched when request view, exception detail: {}".format(traceback.format_exc()))
    exception_name = exception.__class__.__name__
    if exception_name in message.keys():
        if exception_name == "ValidationError":
            message[exception_name]['data'] = exception.detail
        if exception_name == 'PermssionDenied':
            message[exception_name]['data'] = exception.denied_error.code
            message[exception_name]['detail'] = exception.denied_error.detail
        response = Response(data=message[exception_name])
        response.exception_detail = traceback.format_exc()
        return response
    response = Response(data=message['unkown'])
    response.exception_detail = traceback.format_exc()
    return response
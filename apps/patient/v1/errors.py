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

""" Nats models, more detail: https://li.feishu.cn/wiki/wikcnTYngAmddmhKX7ri7Nmi8JU """

patient_errors = {
    'name': {
        'error_messages': {
            "invalid": "您输入的患者姓名无效",
            "blank": "您必须输入患者姓名",
            "max_length": "您输入的患者姓名长度不能超过32",
            "required": "您必须输入患者姓名",
            "null": "您必须输入患者姓名",
            "max_length": "您输入的患者姓名长度不能超过32"
        }
    },
    'phone': {
        'error_messages': {
            "invalid": "您输入患者的手机号无效",
            "required": "您必须输入患者手机号",
            "blank": "您必须输入患者手机号",
            "null": "您必须输入患者手机号",
            "unique": "您必须输入患者手机号",
            "max_length": "您输入的患者手机号长度不能超过16"
        }},
    'address': {
        'error_messages': {
            "invalid": "您输入的用户住址信息无效",
            "required": "您必须指定用户住址",
            "blank": "您必须指定用户住址",
            "null": "您必须指定用户住址",
            "max_length": "您输入的用户住址长度不能超过128"
        }
    },
    'id_card': {
        'error_messages': {
            "invalid": "您输入患者的身份证信息无效",
            "required": "您必须指定患者身份证信息",
            "blank": "您必须指定患者身份证信息",
            "null": "您必须指定患者身份证信息",
            "max_length": "您输入的患者身份证长度不能超过128"
        }
    },
    'age': {
        'error_messages': {
            "invalid": "您输入用户年龄无效",
            "required": "您必须指定用户年龄",
            "blank": "您必须指定用户年龄",
            "null": "您必须指定用户年龄",
        }},
    'height': {
        'error_messages': {
            "invalid": "您输入用户身高无效",
            "required": "您必须指定用户身高",
            "blank": "您必须指定用户身高",
            "null": "您必须指定用户身高",
        }},
    'weight': {
        'error_messages': {
            "invalid": "您输入用户体重无效",
            "required": "您必须指定用户体重",
            "blank": "您必须指定用户体重",
            "null": "您必须指定用户体重",
        }},
    'gender': {
        'error_messages': {
            "invalid": "您输入用户性别无效",
            "required": "您必须指定用户性别",
            "blank": "您必须指定用户性别",
            "null": "您必须指定用户性别",
        }},
}

guardian_errors = {
    'name': {
        'error_messages': {
            "invalid": "您输入的监护人姓名无效",
            "blank": "您必须输入监护人信息",
            "max_length": "您输入的监护人姓名长度不能超过32",
            "required": "您必须输入监护人姓名",
            "null": "您必须输入监护人姓名",
            "max_length": "您输入的监护人姓名长度不能超过32"
        }
    },
    'phone': {
        'error_messages': {
            "invalid": "您输入监护人的手机号无效",
            "required": "您必须输入监护人手机号",
            "blank": "您必须输入监护人手机号",
            "null": "您必须输入监护人手机号",
            "unique": "您必须输入监护人手机号",
            "max_length": "您输入的监护人手机号长度不能超过16"
        }},
    'relation':{
        'error_messages': {
            "invalid": "您输入监护人和患者关系无效",
            "required": "您必须输入监护人和患者关系",
            "blank": "您必须输入监护人和患者关系",
            "null": "您必须输入监护人和患者关系",
            "max_length": "您输入的监护人和患者关系长度不能超过32"
        },
    }
}

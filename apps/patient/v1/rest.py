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

""" patient rest api """

from . import serializer
from apps.patient import models
from core.view import DRFBaseView



class PatientViewSet(DRFBaseView):
    """ Patient ViewSet
    Author:        balinchao(badskyer@fireunix.net)
    Date:          2022-11-05  15:00
    Patient ViewSet, support request method blow:
    create(POST):   '/api/${version}/patient/'               create new patient.
    update(PATCH):  '/api/${version}/patient/${pk}/'         update patient.
    retrieve(GET):  '/api/${version}/patient/${pk}/'         get patient detail.
    list(GET):      '/api/${version}/patient/'               get patient list.
    delete(DELETE): '/api/${version}/patient/${pk}/'         delete patient.
    """
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_list = serializer.patient_serializers
    queryset = models.Patients.objects.filter()



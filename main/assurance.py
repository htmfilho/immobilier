##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2018 Verpoorten Leïla
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.contrib.auth.decorators import login_required
from main import models as mdl
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@login_required
def create(request):
    new_assurance = mdl.assurance.Assurance()
    new_assurance.nom = request.GET.get('nom', None)
    new_assurance.description = request.GET.get('description', None)
    new_assurance.save()
    serializer = AssuranceSerializer(mdl.assurance.find_all(), many=True)
    return JSONResponse(serializer.data)


class AssuranceSerializer(serializers.ModelSerializer):

    class Meta:
        model = mdl.assurance.Assurance
        fields = '__all__'

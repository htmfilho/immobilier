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
from datetime import datetime


DATE_SHORT_FORMAT = "%d/%m/%Y"


def get_key(id):
    if id is None or id == "" or id == "-" or id == "None":
        return None
    return int(id)


def get_previous(request):
    previous = request.POST.get('previous', None)
    if previous is None:
        return request.META.get('HTTP_REFERER', '/')
    return previous


def get_date(value):
    if value:
        try:
            return datetime.strptime(value, '%d/%m/%Y')
        except ValueError:
            return None
    return None

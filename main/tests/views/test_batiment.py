##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2017 Verpoorten Leïla
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
from django.test import TestCase, RequestFactory
from unittest import mock
from main.tests.factories.batiment import BatimentFactory
from django.core.urlresolvers import reverse
#
#
# class BatimentTest(TestCase):
#
#     @mock.patch('django.contrib.auth.decorators')
#     @mock.patch('main.batiment.search_par_proprietaire')
#     def test_search_par_proprietaire_non_defini(self, mock_render, mock_decorators):
#         mock_decorators.login_required = lambda x: x
#         un_batiment = BatimentFactory()
#         request_factory = RequestFactory()
#         request = request_factory.get(reverse('batiment', args=[un_batiment.id]))
#         request.user = mock.Mock()
#
#         from main.batiment import search_par_proprietaire
#         search_par_proprietaire(request)
#
#         self.assertTrue(mock_render.called)
#         request, template, context = mock_render.call_args[0]
#
#         self.assertEqual(template, 'batiment/listeBatiments.html')
#         self.assertEqual(len(context['academic_years']), 1)
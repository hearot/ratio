# Ratio: Quisque faber fortunae suae.
# Copyright (C) 2019 Hearot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url('', include('school.urls', namespace='school')),
    url('', include('competition.urls', namespace='competition')),
    prefix_default_language=False
)


def handler404(request, *__, **___):
    return render(request, 'layouts/default/404.html', {'error_message': _("404: Page not found!")})

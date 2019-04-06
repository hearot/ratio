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

from django.contrib import admin

from .models import Competition, Contestant, Question

admin.site.register(Competition)
admin.site.register(Contestant)
admin.site.register(Question)

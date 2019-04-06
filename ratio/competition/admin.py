from django.contrib import admin

from .models import Answer, Competition, Contestant, Question

admin.site.register(Answer)
admin.site.register(Competition)
admin.site.register(Contestant)
admin.site.register(Question)

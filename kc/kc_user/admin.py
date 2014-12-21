from django.contrib import admin
from kc_user.models import KcGroup, KcUser


admin.site.register(KcGroup)
admin.site.register(KcUser)
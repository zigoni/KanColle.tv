from django.contrib import admin
from kc_user.models import KcGroup, KcUser


class KcUserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'username']


admin.site.register(KcGroup)
admin.site.register(KcUser, KcUserAdmin)
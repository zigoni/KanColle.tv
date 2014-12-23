from django.contrib import admin
from kc_donjin.models import KcUploadedComicFile


class KcUploadedComicFileAdmin(admin.ModelAdmin):
    search_fields = ['file_name', 'uploader']


admin.site.register(KcUploadedComicFile, KcUploadedComicFileAdmin)
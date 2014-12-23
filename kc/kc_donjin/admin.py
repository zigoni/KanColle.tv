from django.contrib import admin
from kc_donjin.models import KcUploadedComicFile, KcComic


class KcUploadedComicFileAdmin(admin.ModelAdmin):
    search_fields = ['file_name', 'uploader']


class KcComicAdmin(admin.ModelAdmin):
    search_fields = ['title', 'publisher', 'translator', 'description']


admin.site.register(KcUploadedComicFile, KcUploadedComicFileAdmin)
admin.site.register(KcComic, KcComicAdmin)
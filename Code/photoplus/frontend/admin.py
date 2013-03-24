from django.contrib import admin
from frontend.models import *

class AlbumAdmin(admin.ModelAdmin):
    pass
admin.site.register(Album, AlbumAdmin)
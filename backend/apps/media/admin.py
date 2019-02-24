from django.contrib import admin
from .models import MediaCreatorRole, License, Media, MediaCreator, MediaType

admin.site.register(MediaType)
admin.site.register(MediaCreator)
admin.site.register(MediaCreatorRole)
admin.site.register(License)
admin.site.register(Media)

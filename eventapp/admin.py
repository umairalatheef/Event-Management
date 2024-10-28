from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'image')
    search_fields = ('event_name',)

admin.site.register(Event, EventAdmin)

   

# Register your models here.

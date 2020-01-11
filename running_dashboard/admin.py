from django.contrib import admin
from django.contrib.gis import admin
from running_dashboard.models import Run, Neighborhood

# Register your models here.

# admin.site.register(Run, admin.OSMGeoAdmin)


class RunAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'time_sec', 'start_time')  # full -> list_display = ('id', 'time_sec', 'start_time', 'route', 'neighborhood')
    fields = [('start_time', 'time_sec'),'route']
    ordering = ['id']

class NeighborhoodAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'name')


admin.site.register(Run, RunAdmin)
admin.site.register(Neighborhood, NeighborhoodAdmin)


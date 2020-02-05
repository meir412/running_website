from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.gis import admin as gis_admin
from running_dashboard.models import Run, Neighborhood

# Register your models here.


class SessionAdmin(admin.ModelAdmin):

    def _session_data(self, obj):
        return obj.get_decoded()

    fields = ['session_key', '_session_data', 'expire_date']
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']


class RunAdmin(gis_admin.OSMGeoAdmin):
    list_display = ('id', 'runner', 'time_sec', 'start_time', 'length')  # full -> list_display = ('id', 'time_sec', 'start_time', 'route', 'neighborhood')
    fields = ['runner', ('start_time', 'time_sec'), 'length', 'route']
    readonly_fields = ['length']
    ordering = ['id']


class NeighborhoodAdmin(gis_admin.OSMGeoAdmin):
    list_display = ('id', 'name')


admin.site.register(Session, SessionAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(Neighborhood, NeighborhoodAdmin)


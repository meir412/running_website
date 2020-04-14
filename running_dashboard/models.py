import math
from datetime import datetime

from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import linestring
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class Run(gis_models.Model):

    id = models.AutoField(primary_key=True)
    time_sec = models.PositiveIntegerField()
    start_time = models.DateTimeField(default=now)
    route = gis_models.LineStringField()
    runner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # neighborhood = models.ManyToManyField('Neighborhood', null=True)
    # length = linestring.LineString.length()    pass

    @property
    def length(self):
        if self.route:
            return round((self.route.transform(3857, clone=True).length) / (1.183), 2)

    @property
    def readable_date(self):
        "Runs date in <Sunday the 1st of January 1970> format"

        day_suffix = 'th'

        if self.start_time.day in [1,11,21]:
            day_suffix = 'st'

        if self.start_time.day in [2,12,22]:
            day_suffix = 'nd'

        return self.start_time.strftime(f"%A the %-d{day_suffix} of %B	%Y")
    
    @property
    def duration(self):
        "Run duration in hours:minutes:seconds format, with zero padding, as String"

        hours = str(math.floor(self.time_sec / 3600)).zfill(2)
        extra_minutes = str(math.floor(self.time_sec / 60) - int(hours)*60).zfill(2)
        extra_seconds = str(self.time_sec % 60).zfill(2)
        return f"{hours}:{extra_minutes}:{extra_seconds}"

    @property
    def average_pace(self):

        # minutes = math.floor(self.time_sec / 60)
        # extra_seconds = self.time_sec % 60
        # length_km = (self.length)/1000
        # min_per_km = minutes / length_km
        # sec_per_km = extra_seconds / length_km

        # return f"{min_per_km}:{sec_per_km} / per Kilometer"

        meter_per_second = self.length / self.time_sec
        min_per_km = 16.666666667 / meter_per_second
        trunc_min_per_km = math.floor(min_per_km)
        extra_sec_per_km = math.floor((min_per_km % 1) * 60)


        return f"{trunc_min_per_km}:{extra_sec_per_km}"
        
    class Meta:
        permissions = (('can_observe_all_runs', 'Can observe all runs'),)


class Neighborhood(models.Model):

    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=80)
    area = gis_models.PolygonField(null=True)

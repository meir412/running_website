# from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import linestring
from django.utils.timezone import now

# Create your models here.


class Run(models.Model):

    id = models.AutoField(primary_key=True)
    time_sec = models.PositiveIntegerField()
    start_time = models.DateTimeField(default=now)
    route = models.LineStringField()
    # neighborhood = models.ManyToManyField('Neighborhood', null=True)
    # length = linestring.LineString.length()    pass

    # def calc_length(self):
    #     print(id)


class Neighborhood(models.Model):

    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=80)
    area = models.PolygonField(null=True)

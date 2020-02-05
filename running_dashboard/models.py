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

    class Meta:
        permissions = (('can_observe_all_runs', 'Can observe all runs'),)


class Neighborhood(models.Model):

    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=80)
    area = gis_models.PolygonField(null=True)

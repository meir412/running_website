
from django.shortcuts import render
from django.core.serializers import serialize
from django.views import generic
from running_dashboard.models import Run


def index(request):
    # query = Run.objects.filter(id__gt=1)
    query = Run.objects.all()
    run_geojson = serialize('geojson', query, geometry_field='route', srid=3857, fields=('id','time_sec',))
    route_1 = Run.objects.get(id=1).route
    route_1_3857 = route_1.transform(3857, clone=True)
    length = route_1_3857.length
    num_runs = Run.objects.only('id').all().count()
    lengths = {}
    total_length = 0
    for i in range(num_runs):
        lengths[i+1] = (Run.objects.get(id=i+1).route.transform(3857, clone=True).length)/(1.183)
        total_length += lengths[i+1]

    total_length_km = round(total_length / 1000, 2)
    context = {'num_runs': num_runs, 'total_length': total_length_km,'runs': run_geojson}
    return render(request, 'index.html', context=context)


class RunListView(generic.ListView):

    model = Run
    queryset = Run.objects.order_by('id')


class RunDetailView(generic.DetailView):

    model = Run

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(RunDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        # Create any data and add it to the context
        query = [Run.objects.get(id=pk)]
        run_geojson = serialize('geojson', query, geometry_field='route', srid=3857, fields=('id', 'time_sec',))
        context['route'] = run_geojson
        return context

from django.shortcuts import redirect
from django.shortcuts import render
from django.core.serializers import serialize
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from running_dashboard.models import Run

@login_required
def index(request):

    if request.user.is_superuser:
        query = Run.objects.all()
    else:
        query = Run.objects.filter(runner=request.user)

    run_geojson = serialize('geojson', query, geometry_field='route', srid=3857, fields=('id','time_sec',))
    num_runs = query.count()
    total_length = sum([run.length for run in query])

    total_length_km = round(total_length / 1000, 2)
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {'num_runs': num_runs, 'total_length': total_length_km, 'runs': run_geojson, 'num_visits': num_visits}
    return render(request, 'index.html', context=context)


class RunListView(LoginRequiredMixin, generic.ListView):

    model = Run
    # queryset = Run.objects.order_by('id')
    # query = Run.objects.filter(runner=request.user)

    def get_queryset(self):

        if self.request.user.is_superuser:
            return Run.objects.order_by('id')
        else:
            return Run.objects.filter(runner=self.request.user).order_by('id')


class RunDetailView(LoginRequiredMixin, generic.DetailView):

    model = Run

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        query = Run.objects.get(id=pk)
        if query.runner is not self.request.user and not self.request.user.is_superuser:
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(RunDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        # Create any data and add it to the context
        query = [Run.objects.get(id=pk)]
        run_geojson = serialize('geojson', query, geometry_field='route', srid=3857, fields=('id', 'time_sec',))
        context['route'] = run_geojson
        return context
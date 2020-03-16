import datetime

from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy

from running_dashboard.forms import ChangeRunDurationForm
from running_dashboard.forms import AddRunForm
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


def change_run_duration(request, pk):
    run_instance = get_object_or_404(Run, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ChangeRunDurationForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            run_instance.time_sec = form.cleaned_data['time_sec']
            run_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('run-detail', args=[run_instance.id]))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_run_time = 1800
        form = ChangeRunDurationForm(initial={'date': proposed_run_time})

    context = {
        'form': form,
        'run_instance': run_instance,
    }

    return render(request, 'running_dashboard/change_run_time.html', context)


def addNewRun(request):

    if request.method == 'POST':

        form = AddRunForm(request.POST, request.FILES)
        print('hi')

        if form.is_valid():
            pass
            # run = Run(time_sec=, start_time=, route=, runner=)
            # run.save()

    else:

        form = AddRunForm()

    context = {
        'form': form,
    }

    return render(request, 'running_dashboard/add_run.html', context)


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


class RunCreate(CreateView):
    model = Run
    fields = '__all__'


class RunUpdate(UpdateView):
    model = Run
    fields = ['time_sec', 'start_time']
    success_url = reverse_lazy('index')
    # exclude = ['time_sec']


class RunDelete(DeleteView):
    model = Run
    success_url = reverse_lazy('index')
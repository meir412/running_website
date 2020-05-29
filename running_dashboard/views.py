import datetime

from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from running_dashboard.forms import ChangeRunDurationForm
from running_dashboard.forms import AddRunForm
from running_dashboard.forms import SignUpForm
from running_dashboard.models import Run
from running_dashboard.tokens import account_activation_token
from running_dashboard.util import attributesFromGpx

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

@login_required
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

@login_required
def addNewRun(request):
    """
    This view allows a user to add a new run and associate it with their account.
    The view renders a form with input for the gpx file.
    If the form doesn't pass validations it is rendered again with errors.
    If the form passes all validations, the run is added to the db and the user is redirected
    to the home page.
    """

    if request.method == 'POST':

        form = AddRunForm(request.POST, request.FILES)

        if form.is_valid():
            gpx_file = form.cleaned_data['gpx_file']
            start_time = gpx_file['start_time']
            time_sec = gpx_file['time_sec']
            route = gpx_file['wkt']
            runner = request.user
            run = Run(time_sec=time_sec, start_time=start_time, route=route, runner=runner)
            run.save()

            return HttpResponseRedirect(reverse('run-detail', args=[run.id]))

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

        pk = self.kwargs.get(self.pk_url_kwarg)
        query = Run.objects.get(id=pk)
        if query.runner.id != self.request.user.id and not self.request.user.is_superuser:
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


class RunUpdate(UpdateView):
    model = Run
    fields = ['time_sec', 'start_time', 'route']
    success_url = reverse_lazy('index')
    # exclude = ['time_sec']


class RunDelete(DeleteView):
    model = Run
    success_url = reverse_lazy('index')


def signUp(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your running website account.'
            message = render_to_string('registration/signup_activation_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=password)
            # login(request, user)
            return render(request, 'awaiting_activation.html')

        return render(request, 'sign_up.html', {'form': form})

    else:
        form = SignUpForm()
        return render(request, 'sign_up.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('index')

    else:
        return render(request, 'registration/invalid_activation_link.html')

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm



from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Resolution
from .forms import CommentForm

# Create your views here.
def home(request):
   return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = "Invalid sign up - try again"
  form = UserCreationForm()
  context = { 'form': form, 'error_message': error_message }
  return render(request, 'registration/signup.html', context)

class ResolutionIndex(LoginRequiredMixin, ListView):
  model = Resolution
  fields = '__all__'

class ResolutionDetail(LoginRequiredMixin, DetailView):
  model = Resolution
  def get_context_data(self, **kwargs):
    context = super(ResolutionDetail, self).get_context_data(**kwargs)
    context['comment_form'] = CommentForm()
    return context


class ResolutionCreate(LoginRequiredMixin, CreateView):
   model = Resolution
   fields = ['goal', 'reason', 'time_period', 'notes']
   # We are trying to pass the user id into the form instance that was returned to us by the form html. For some reason, self.request has user in it. Super calls CreateView so we can use the default functions of the original CreateView model. form_valid checks if the form is valid. 
   def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)

class ResolutionUpdate(LoginRequiredMixin, UpdateView):
  model = Resolution
  fields = ['goal', 'reason', 'time_period', 'notes']

class ResolutionDelete(LoginRequiredMixin, DeleteView):
  model = Resolution
  success_url = '/resolutions/'

def add_comment(request, resolution_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.resolution_id = resolution_id
    new_comment.user = request.user
    new_comment.save()
  return redirect('detail', pk=resolution_id)
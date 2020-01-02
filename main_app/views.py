from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Resolution, Comment, Entry, Photo
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
      return redirect('index')
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


@login_required
def user_resolutions(request, user_id):
   resolutions = Resolution.objects.filter(user=request.user)
   # city_form = CityForm()
   return render(request, 'resolutions/user_resolutions.html', { 
      'resolutions': resolutions
      })

@login_required
def add_comment(request, resolution_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.resolution_id = resolution_id
    new_comment.user = request.user
    new_comment.save()
  return redirect('detail', pk=resolution_id)

@login_required
def delete_comment(request, comment_id):
   comment = Comment.objects.get(id=comment_id)
   comment.delete()
   return redirect('detail', comment.resolution_id)

class EntryList(LoginRequiredMixin, ListView):
   model = Entry
   fields = '__all__'
   def get_context_data(self, **kwargs):
      context = super(EntryList, self).get_context_data(**kwargs)
      context['entry_list'] = Entry.objects.filter(resolution_id=self.kwargs.get('resolution_id'))
      context['resolution'] = Resolution.objects.get(id=self.kwargs.get('resolution_id'))
      return context

class EntryCreate(LoginRequiredMixin, CreateView):
   model = Entry
   fields = ['mood', 'week', 'notes', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
   def form_valid(self, form):
      form.instance.user = self.request.user
      form.instance.resolution = Resolution.objects.get(id=self.kwargs.get('resolution_id'))
      return super().form_valid(form)

class EntryUpdate(LoginRequiredMixin, UpdateView):
   model = Entry
   fields = ['mood', 'week', 'notes', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

@login_required
def delete_entry(request, entry_id):
   entry = Entry.objects.get(id=entry_id)
   entry.delete()
   return redirect('entry_index', entry.resolution_id)

@login_required
def add_photo(request, user_id):
  S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
  BUCKET = 'goaltracker'
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f'{S3_BASE_URL}{BUCKET}/{key}'
      photo = Photo(url=url, user_id=user_id)
      photo.save()
    except:
      print('An error occured uploading file to s3')
  return redirect('user_resolutions', user_id=user_id)
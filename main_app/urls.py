from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path('resolutions/', views.ResolutionsIndex.as_view(), name='index'),
   path('accounts/signup/', views.signup, name='signup'),
]
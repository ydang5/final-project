from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from api import views

urlpatterns = [
    #Homepage
    path('api/version', views.GetVersion.as_view(),name='get_version'),

]

urlpatterns = format_suffix_patterns(urlpatterns)

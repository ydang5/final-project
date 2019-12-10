from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from api import views

urlpatterns = [
    #homepage
    path('api/version', views.GetVersion.as_view(),name='get_version'),
    #gateway
    path('api/login', obtain_auth_token, name='api_token_auth'),
    path('api/logout',views.UserLogoutAPI.as_view()),
    #file-upload
    path('api/student-file-uploads', views.LLIStudentMasterSheetUploadAPIView.as_view()),
    #data_organizer
    path('api/immi-check',views.ImmiStatusValidCheckAPI.as_view()),
    path('api/payment-check',views.PaymentValidCheckAPI.as_view()),
    path('api/insurance-check',views.InsuranceValidCheckAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='dashboard'),
    path('report/', report, name='report'),
    path('login/', login_view, name='login'),
    path('loginauth/', login_auth, name='loginauth'),
    path('logoutauth/', logout_auth, name='logoutauth'),
]

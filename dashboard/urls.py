from django.urls import path
from django.conf.urls import handler404, handler500
from .views import *


urlpatterns = [
    path('', index, name='dashboard'),
    path('report/', report, name='report'),
    path('login/', login_view, name='login'),
    path('loginauth/', login_auth, name='loginauth'),
    path('logoutauth/', logout_auth, name='logoutauth'),
]

handler404 = 'dashboard.views.page_404'
handler500 = 'dashboard.views.page_500' 
from django.urls import path
from .views import *

urlpatterns = [
    path('sendemail/', send_html_email, name='kirim_html'),
]

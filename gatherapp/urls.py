from django.urls import path
from .views import *

urlpatterns = [
    path('entry/', entry, name='entrydata'),
    # path('fromcsv/', from_csv, name='fromcsv'),
]

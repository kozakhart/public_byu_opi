from django.urls import path
from . import views

urlpatterns = [
    path('', views.opi_form, name='opi_form'),
    path('receipt', views.receipt, name='receipt'),
    path('data', views.index_data, name='index_data'),
    path('thirdyear', views.create_slats, name='create_slats'),
    path('thirdyear/receipt', views.slats_receipt, name='slats_receipt'),
]

from django.urls import path
from .views import CustomerDetailView


urlpatterns = [
    path(route='<slug:slug>/', view= CustomerDetailView.as_view(), name='detail'),
]
from django.urls import path
from .views import CustomerDetailView, SignupPageView


urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),
    path(route='<slug:slug>/', view=CustomerDetailView.as_view(), name='profile'),

]
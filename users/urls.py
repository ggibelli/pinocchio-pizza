from django.urls import path
from .views import CustomerDetailView

from .views import SignupPageView

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),
    path(route='users/<slug:slug>/', view=CustomerDetailView.as_view(), name='profile'),

]
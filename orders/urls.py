from django.urls import path
from .views import OrderListView, OrderDetailView, OrderDeleteView, OrderUpdateView, MultipleModelView, ItemCreateView


urlpatterns = [
    path(route='orders/menu/', view=MultipleModelView.as_view(), name='menu'),
    path(route='orders/orders/', view=OrderListView.as_view(), name='order-list'),
    path(route='orders/<int:pk>/', view=OrderDetailView.as_view(), name='order-detail'),
    path(route='orders/<int:pk>/edit', view=OrderUpdateView.as_view(), name='order-edit'),
    path(route='orders/<int:pk>/delete', view=OrderDeleteView.as_view(), name='order-delete'),
    path(route='orders/item/', view=ItemCreateView.as_view(), name='additem')
]
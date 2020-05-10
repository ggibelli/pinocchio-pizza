from django.urls import path
from .views import charge, post_payment, ConfirmOrderView, OrderListView, OrderDetailView, OrderEditView, OrderDeleteView, CartUpdateView, MultipleModelView, ItemCreateView


urlpatterns = [
    path(route='orders/menu/', view=MultipleModelView.as_view(), name='menu'),
    path(route='orders/orders/', view=OrderListView.as_view(), name='order-list'),
    path(route='orders/<int:pk>/', view=OrderDetailView.as_view(), name='order-detail'),
    path(route='orders/<int:pk>/edit', view=OrderEditView.as_view(), name='order-edit'),
    path(route='orders/<int:pk>/cart', view=CartUpdateView.as_view(), name='cart'),
    path(route='orders/<int:pk>/delete', view=OrderDeleteView.as_view(), name='order-delete'),
    path(route='orders/item/<slug:category>', view=ItemCreateView.as_view(), name='additem'),
    path(route='orders/<int:pk>/confirm', view=ConfirmOrderView.as_view(), name='confirm-cart'),
    path('charge/', charge, name='charge'),
    path('post-payment/<int:cart_id>', post_payment, name='post_payment'),
]
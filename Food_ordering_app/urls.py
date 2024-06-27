from django.urls import path
from Food_ordering_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('add/<int:pizza_id>/', views.add_item, name='add_item'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),

]

    
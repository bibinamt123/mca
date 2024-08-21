from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('order/', views.order_product, name='order_product'),
    path('feedback/', views.feedback, name='feedback'),
    path('view_orders/', views.view_orders, name='view_orders'),
]

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('order/', views.order_product, name='order_product'),
    path('feedback/', views.feedback, name='feedback'),
    path('total-orders/',views.total_orders_view, name='total_orders'),
    path('order/<int:order_id>/pay/', views.initiate_payment, name='initiate_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
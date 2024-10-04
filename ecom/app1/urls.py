from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('reg/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_quantity/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/', views.view_cart, name='view_cart'),
    path('proceed-to-payment/', views.proceed_to_payment, name='proceed_to_payment'),
    path('feedback/', views.feedback, name='feedback'),
    path('user-feedbacks/', views.user_feedbacks, name='user_feedbacks'),  # New view for user feedbacks
    path('feedback/success/', views.feedback_success, name='feedback_success'),
    path('total-orders/', views.total_orders_view, name='total_orders'),
    path('order/<int:order_id>/pay/', views.proceed_to_payment, name='initiate_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
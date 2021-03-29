from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('adminlogin', views.admin_login, name='adminlogin'),
    path('delete/<int:id>/',views.delete_data,name='delete'),
    path('<int:id>', views.update_data, name='update'),
    path('userlogin', views.user_login, name='userlogin'),
    path('add-to-cart/<int:id>/',views.add_to_cart , name="addtocart"),
    path('mycart',views.OrderSummaryView,name="mycart")
]
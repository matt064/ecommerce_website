from django.urls import path
from django.contrib.auth import views as v


from . import views

app_name = 'core'

urlpatterns = [
    path('', views.frontpage, name="main"),
    path('shop/', views.shop, name="shop"),

    path('signup/', views.sign_up, name="signup"),
    path('login/', v.LoginView.as_view(template_name='core/login.html'), name="login"),
    path('logout/', v.LogoutView.as_view(), name="logout"),

    path('myaccount/', views.my_account, name="my_account"),
    path('myaccount/edit/', views.edit_my_account, name="edit_my_account"),
]
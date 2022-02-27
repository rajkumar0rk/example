from django.urls import include, path

from . import views

urlpatterns = [
    
    path('login/', views.login,name="login"),
    path('register/', views.register,name="register"),
    path('logout/', views.logout,name="logout"),
    path('dashboard/', views.dashboard,name="dashboard"),
    path('', views.dashboard),
    path('forgetpassword/', views.forgetpassword,name="forgetpassword"),
    path('activate/<uidb64>/<token>/', views.activate,name="activate"),
    path('reset_password_validation/<uidb64>/<token>/', views.reset_password_validation,name="reset_password_validation"),
    path('reset_password/', views.reset_password,name="reset_password"),
   
]

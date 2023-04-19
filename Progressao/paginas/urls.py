from django.urls import path,include 
from paginas import views
from .views import signup_view, login_view,logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout_view'),
    path('home/', views.home, name='home'),
    path('home/', include('paginas.urls')),
    
    
]

    # path('form/', views.sucesso_view, name='form_view'),


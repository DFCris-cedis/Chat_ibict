# from paginas.views import MyPasswordResetConfirmView
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView
from paginas import views

# from paginas.views import CustomPasswordResetConfirmView
# from .views import SignUpNameView, SignUpEmailView, SignUpPasswordView


urlpatterns = [
    path('', views.home, name='home_root'),
    path('', include('paginas.urls', namespace='home')),
    path('signup/email/', views.signup_email, name='signup_email'),
    path('signup/name/', views.signup_name, name='signup_name'),
    path('signup/password/', views.signup_password, name='signup_password'),
    path('logout/', views.logout_view, name='logout_view'),
    path('home/', include('paginas.urls')),
    path('manual_de_uso/', TemplateView.as_view(template_name="manual_de_uso.html"), name='manual_de_uso'),
    path('duvidas_frequentes/', TemplateView.as_view(template_name="duvidas_frequentes.html"), name='duvidas_frequentes'),
    path('sucesso_cadastro/', TemplateView.as_view(template_name="sucesso_cadastro.html"), name='sucesso_cadastro'),
    path('login/email/', views.email_login, name='login'),
    path('login/senha/', views.senha_login, name='senha_login'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]

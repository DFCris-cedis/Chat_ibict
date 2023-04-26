from django.urls import path, include
from django.contrib.auth import views as auth_views
from paginas.views import CustomPasswordResetView
from paginas import views
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

urlpatterns = [
    path('', include('paginas.urls', namespace='home')),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout_view'),
    path('home/', include('paginas.urls')),
    path('reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/complete/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]

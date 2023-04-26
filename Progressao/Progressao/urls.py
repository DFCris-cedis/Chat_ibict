
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from paginas.views import CustomPasswordResetView
from paginas import views
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout_view'),
    path('reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password/done/', CustomPasswordResetView.as_view(),
         name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/complete/', CustomPasswordResetView.as_view(),
         name='password_reset_complete'),




    #     path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
    #         template_name="password_reset_sent.html"), name="password_reset_done"),
    #     path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #         template_name="password_reset_form.html"), name="password_reset_confirm"),
    #     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
    #         template_name="password_reset_complete.html"), name="password_reset_complete"),
]

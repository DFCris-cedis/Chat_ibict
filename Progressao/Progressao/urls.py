
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from paginas import views
# from django.contrib.auth.views import PasswordResetConfirmView
# from django.urls import reverse_lazy
# from django.core.mail import send_mail
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.contrib.auth.tokens import default_token_generator



urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout_view'),
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
     path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),

]

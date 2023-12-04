from paginas.views import MyPasswordResetConfirmView
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib import admin
from paginas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    path('accounts/login/', views.custom_login, name='login'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout_view'),
    path('accounts/reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_form/', auth_views.PasswordResetForm.as_view(), name='password_reset_form'),
    path('accounts/reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset_password_confirm/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

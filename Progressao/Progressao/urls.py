
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from paginas import views
from paginas.views import CustomPasswordResetConfirmView



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
    path('accounts/reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

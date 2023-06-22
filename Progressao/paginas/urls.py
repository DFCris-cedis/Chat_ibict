from paginas.views import MyPasswordResetConfirmView
from django.contrib.auth import views as auth_views
from django.urls import path, include
from paginas import views

urlpatterns = [
    path('', include('paginas.urls', namespace='home')),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout_view'),
    path('home/', include('paginas.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_complete'),

]

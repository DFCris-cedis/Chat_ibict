from django.shortcuts import redirect

class StaffOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exceptions = [
            
            '/accounts/login/',
            '/accounts/signup/',
            '/accounts/password_reset/',
            '/accounts/password_reset/done/',
            '/accounts/reset/<uidb64>/<token>/',
            '/accounts/password_reset_confirm/',
            '/accounts/password_reset_form/',
            '/reset/done/',
            '/reset/<uidb64>/<token>/'
        ]  # adicionar a URL de cadastro aqui

        if not request.user.is_authenticated:
            if request.path not in exceptions and '/reset/<uidb64>/<token>' not in request.path:
                return redirect('login')


        response = self.get_response(request)
        return response


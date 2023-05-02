from django.shortcuts import redirect

class StaffOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exceptions = [
            '/accounts/login/',
            '/accounts/signup/',
            '/accounts/reset_password/',
            '/accounts/reset_password/done/',
            '/accounts/reset/done/'
        ]  # adicionar a URL de cadastro aqui

        if not request.user.is_authenticated or not request.user.is_staff:
            if request.path not in exceptions and '/accounts/reset_password_confirm/' not in request.path:
                return redirect('login')

        response = self.get_response(request)
        return response


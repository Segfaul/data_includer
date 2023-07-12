from django.middleware.csrf import CsrfViewMiddleware
from django.shortcuts import render


class CustomCsrfMiddleware(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return render(request, template_name='dataset/exceptions/error_page.html', status=403, context={
            'title': 'Ошибка доступа: 403',
            'error_message': 'Некорректный CSRF токен',
        })
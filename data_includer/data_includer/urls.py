from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import settings

schema_view = get_schema_view(  # new
    openapi.Info(
        title="Data Includer API",
        default_version='v1',
        description="Data Includer - is an api service for working with csv datasets. "
                    "Our users have the ability to add/edit/read csv files. "
                    "Also thanks to our api token system it is possible to use basic services from remote systems.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    patterns=[path('api/', include('api.urls')), ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include('api.urls')),
    path('', include('table.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'table.views.tr_handler403'
handler404 = 'table.views.tr_handler404'
handler405 = 'table.views.tr_handler405'
handler500 = 'table.views.tr_handler500'

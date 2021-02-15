from django.contrib import admin
from django.urls import path,include
from public.views import Logout
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header="Tuzowe Admin."
admin.site.site_title="Tuzowe Admin Page."
admin.site.index_title="Welcome to Tuzowe admin page."


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('public.urls')),
    path('user-dashboard/', include('client.urls')),
    path('admin-dashboard/', include('superuser.urls')),
    path('logout/', Logout,name='Logout'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns=urlpatterns+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

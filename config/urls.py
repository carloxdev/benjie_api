# Django's Libraries
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

# from django.conf.urls import handler404
# from django.conf.urls import handler500

# Third-party Libraries
# from Utils.views import Stx404view
# from Utils.views import Stx500view

# handler404 = Stx404view
# handler500 = Stx500view

admin.site.site_header = settings.APP_NAME

ADMIN_URLS = [
    path('admin/', admin.site.urls),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
]

urlpatterns = ADMIN_URLS

if settings.DEBUG:
    urlpatterns = static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    ) + \
        urlpatterns

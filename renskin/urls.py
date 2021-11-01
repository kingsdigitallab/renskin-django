# from ddhldap.signal_handlers import register_signal_handlers as \
#     ddhldap_register_signal_handlers

from django.conf import settings
from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from cms.views import SearchView
#from wagtail.search.urls import frontend as wagtailsearch_frontend_urls

admin.autodiscover()
# ddhldap_register_signal_handlers()

urlpatterns = [
    path(r'grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
]

# -----------------------------------------------------------------------------
# Django Debug Toolbar URLS
# -----------------------------------------------------------------------------
try:
    if settings.DEBUG:
        import debug_toolbar
        urlpatterns += [
            path(r'__debug__/',
                include(debug_toolbar.urls)),
        ]

except ImportError:
    pass


# -----------------------------------------------------------------------------
# Wagtail CMS
# -----------------------------------------------------------------------------

urlpatterns += [
    path(r'wagtail/', include(wagtailadmin_urls)),
    path(r'documents/', include(wagtaildocs_urls)),
    url(r"^search/", SearchView.as_view()),
    path(r'', include(wagtail_urls)),
]

# -----------------------------------------------------------------------------
# Static file DEBUGGING
# -----------------------------------------------------------------------------
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import os.path

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(settings.MEDIA_ROOT,
                                                     'images'))

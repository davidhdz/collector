from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from banknotes.views import (
    album_all_detail_view,
    album_all_view,
    album_country_view,
    album_detail_view,
    banknote_detail_view,
    banknote_statistics_views,
    create_album,
    create_banknote,
    edit_album,
    edit_banknote,
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("collector.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("<str:username>/", banknote_statistics_views, name="dashboard"),
    path(
        "<str:username>/banknote/<slug:pk>/<slug:slug>/",
        banknote_detail_view.as_view(template_name="banknote/banknote_detail.html"),
        name="banknote_detail_view",
    ),
    path(
        "<str:username>/banknote/edit/<slug:pk>/<slug:slug>/",
        edit_banknote,
        name="banknote_edit",
    ),
    path("<str:username>/banknote/create/", create_banknote, name="banknote_create"),
    path(
        "<str:username>/album/edit/<slug:pk>/<slug:slug>/",
        edit_album,
        name="album_edit",
    ),
    path("<str:username>/album/create/", create_album, name="album_create"),
    path(
        "<str:username>/album/<slug:pk>/<slug:slug>/",
        album_detail_view.as_view(template_name="banknote/album.html"),
        name="album_detail_view",
    ),
    path(
        "<str:username>/album/all-banknotes/",
        album_all_detail_view,
        name="album_all_detail_view",
    ),
    path("<str:username>/album/index/", album_all_view, name="album_all_view"),
    path(
        "<str:username>/country/<url_country>/",
        album_country_view,
        name="album_country_view",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

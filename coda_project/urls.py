from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from coda_project import settings

# =========== ERROR HANDLING SECTION ================
handler400 = "main.views.handler400"  # Corrected typo here
handler403 = "main.views.handler403"  # Corrected typo here
handler404 = "main.views.handler404"  # Corrected typo here
handler500 = "main.views.handler500"  # Corrected typo here

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),
    
    # Static and Media file handling
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    
    # Authentication URLs
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="accounts/registration/DC48K/logins.html"),
        name="account-logout",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="accounts/registration/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done",
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/registration/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/registration/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    
    # Including the app URLs
    path("", include("main.urls", namespace="main")),
    path("accounts/", include("accounts.urls")),
    path("finance/", include("finance.urls"), name="finance"),
]

# Serve static and media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

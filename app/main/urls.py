from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from main.view.index import index
from main.view.login import HosLoginView
from main.view.logout import HosLogoutView

from main.view.password_reset_done import HosPasswordResetDoneView
from main.view.password_reset import HosPasswordResetView
from main.view.password_reset_complete import HosPasswordResetCompleteView
from main.view.password_reset_confirm import HosPasswordResetConfirmView
from main.view.password_change import HosPasswordChangeView
from main.view.profile_delete import DeleteUserView
from main.view.profile_change import ChangeUserInfoView
from main.view.register_activate import user_activate
from main.view.register_done import RegisterDoneView
from main.view.register import RegisterUserView
from main.view.other import other_page
from main.view.fav_playlist import fav_playlist
from main.view.get_playlist import get_playlist
from main.view.get_mytrack import get_mytrack
from main.view.set_mytrack import set_mytrack

app_name = "main"
urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    # По умолчанию Django выполняет перенаправление по пути 'accounts/login'
    # при попытке гостя получить доступ к закрытой он него странице
    path("accounts/login/", HosLoginView.as_view(), name="login"),
    path("accounts/logout/", HosLogoutView.as_view(), name="logout"),
    path(
        "accounts/password/reset/done/",
        HosPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/password/reset/",
        HosPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "accounts/password/confirm/complete/",
        HosPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "accounts/password/confirm/<uidb64>/<token>/",
        HosPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password/change/",
        HosPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "accounts/profile/delete/",
        DeleteUserView.as_view(),
        name="profile_delete",
    ),
    path(
        "accounts/profile/change/",
        ChangeUserInfoView.as_view(),
        name="profile_change",
    ),
    path(
        "accounts/register/activate/<str:sign>/",
        user_activate,
        name="register_activate",
    ),
    path(
        "accounts/register/done/",
        RegisterDoneView.as_view(),
        name="register_done",
    ),
    path("accounts/register/", RegisterUserView.as_view(), name="register"),
    path(
        "<str:pgm_num>/<int:track_pos>/<str:id>/set/",
        set_mytrack,
        name="set_mytrack",
    ),
    path(
        "<str:pgm_num>/<int:track_pos>/get/", get_mytrack, name="get_mytrack"
    ),
    path("<int:playlist_pk>/fav/", fav_playlist, name="fav"),
    path("<int:playlist_pk>/playlist/", get_playlist, name="get_playlist"),
    path("<str:page>/", other_page, name="other"),
    path("", index, name="index"),
]

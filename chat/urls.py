from django.urls import path
from .views import index, SignupView, LoginView, logout_view, RoomCreateView, room_detail

urlpatterns = [
    path("", index, name="index"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("rooms/new/", RoomCreateView.as_view(), name="room_create"),
    path("rooms/<str:room_name>/", room_detail, name="room_detail"),
]
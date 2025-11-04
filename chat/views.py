from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpRequest
from .models import Room, Message

def index(request: HttpRequest):
    q = request.GET.get("q", "").strip()
    if q:
        rooms = Room.objects.filter(name__icontains=q)
    else:
        rooms = Room.objects.all()
    stats = {"total_rooms": rooms.count(), "total_users": User.objects.count()}
    return render(request, "index.html", {"rooms": rooms, "q": q, "stats": stats})

class SignupView(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        if not username or not password:
            return render(request, "signup.html", {"error": "Both fields are required."})
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists."})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("index")

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "login.html", {"error": "Invalid credentials."})
        login(request, user)
        return redirect("index")

def logout_view(request):
    logout(request)
    return redirect("index")

class RoomCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "room_create.html")

    def post(self, request):
        name = request.POST.get("name", "").strip()
        if not name:
            return render(request, "room_create.html", {"error": "Room name is required."})
        if Room.objects.filter(name=name).exists():
            return render(request, "room_create.html", {"error": "Room name already exists."})
        room = Room.objects.create(name=name, created_by=request.user)
        return redirect("room_detail", room_name=room.name)

@login_required
def room_detail(request, room_name: str):
    room = get_object_or_404(Room, name=room_name)
    messages = Message.objects.filter(room=room).select_related("user")
    return render(request, "room.html", {"room": room, "messages": messages})

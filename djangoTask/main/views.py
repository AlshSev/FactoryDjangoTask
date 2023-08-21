from django.shortcuts import render, redirect
from .forms import RegistrationForm, MessageForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Message
import requests
import json
from django.conf import settings

host = getattr(settings, "HOST", None)

@login_required(login_url="/login")
def home(request):
    messages = Message.objects.filter(author=request.user)

    if request.method == "POST":
        message_id = request.POST.get("message-id")
        message = Message.objects.filter(id=message_id).first()
        if message and message.author == request.user:
            message.delete()

    return render(request, 'main/home.html', {"messages" : messages})

@login_required(login_url="/login")
def create_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            # Yes, it is stupid, I know
            requests.post(f"http://{host}:8000/api/send", 
                          json.dumps({"message": message.body}), 
                          headers={"token": request.user.profile.token})
            message.author = request.user
            message.save()
            return redirect("/home")
    else:
        form = MessageForm()

    return render(request, 'main/create_message.html', {"form": form})

@login_required(login_url="/login")
def quickstart(request):
    return render(request, 'main/quickstart.html')

def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/quickstart')
    else:
        form = RegistrationForm

    return render(request, 'registration/sign_up.html', {"form": form})
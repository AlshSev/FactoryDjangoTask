#from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.conf import settings
import json
from main.models import User

bot_token = getattr(settings, "BOT_TOKEN", None)
tele_url = f"https://api.telegram.org/bot{bot_token}/"

@api_view(["POST"])
def send_message(request, *args, **kwargs):
    if "token" not in request.headers:
        return Response({"status": "FAILED", "detail": "No token provided"})
    token = request.headers["token"]
    user = User.objects.filter(profile__token=token).first()
    if user is None:
        return Response({"status": "FAILED", "detail": "Unknown token"})
    if user.profile.telegram_id == "":
        return Response({"status": "FAILED", "detail": "Telegram is not connected to this token"})
    data = {}
    try:
        data = json.loads(request.body.decode())
    except:
        pass
    if "message" not in data:
        return Response({"status": "FAILED", "detail": "No message provided"})
    tg_body = {
        "chat_id": user.profile.telegram_id,
        "text": f"{user.username}, I got a message from you:\n{data['message']}"
    }
    r = requests.post(tele_url + "sendMessage", tg_body)
    jr = r.json()
    if jr["ok"]:
        message_id = jr["result"]["message_id"]
        chat_id = jr["result"]["chat"]["id"]
        return Response({"status": "OK", "result": str(message_id) + ' ' + str(chat_id)})
    return Response({"status": "FAILED", "full_response": r.text})

@api_view(["POST"])
def receive_update(request, *args, **kwargs):
    data = {}
    try:
        data = json.loads(request.body.decode())
    except:
        pass
    if "message" in data:
        try:
            token = data["message"]["text"]
            chat_id = data["message"]["chat"]["id"]
        except:
            return Response()
        user = User.objects.filter(profile__token=token).first()
        user.profile.telegram_id = chat_id
        user.save()
        return Response({"detail": 
                            {"token": token, "id": chat_id, "user_token": user.profile.token, 
                             "user_tele_id": user.profile.telegram_id}
                        })
    return Response()

from django.shortcuts import redirect
from django.http import JsonResponse
import requests
from django.utils.timezone import now
from .models import CustomUser

CLIENT_ID = "ТВОЙ_CLIENT_ID"
CLIENT_SECRET = "ТВОЙ_CLIENT_SECRET"
REDIRECT_URI = "http://127.0.0.1:8000/api/google/callback/"

def google_login(request):
    url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=openid email profile"
    return redirect(url)

def google_callback(request):
    code = request.GET.get('code')

    token_response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
    ).json()

    access_token = token_response.get("access_token")

    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    email = user_info.get("email")

    user, _ = CustomUser.objects.get_or_create(email=email)

    user.first_name = user_info.get("given_name")
    user.last_name = user_info.get("family_name")
    user.is_active = True
    user.last_login = now()
    user.registration_source = "google"

    user.save()

    return JsonResponse({"message": "Google login success"})
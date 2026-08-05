import json
from django.contrib.auth import authenticate, logout
from django.http import JsonResponse
from app_user.models import User


def user_view(request):
    """profile page(is settings)"""
    user = request.user
    return JsonResponse({
        "image_profile": user.image_profile,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone
    })

def change_profile(request):
    pass


def register(request):
    """signup page"""
    if request.method == "POST":
        data = json.loads(request.body)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get("email")
        password = data.get("password")

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "message": "This account already exists. Please login."
            }, status=400)

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        return JsonResponse({
            "message": "Registration successful",
            "full_name": user.get_full_name,
            "email": user.email
        }, status=201)

    return JsonResponse({
        "message": "Only POST method is allowed"
    }, status=405)

def login_view(request):
    """login page"""
    if request.method == "POST":
        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")

        user = authenticate(
            request,
            email=email,
            password=password
        )
        if user is not None:
            return JsonResponse({
                "message": "Login Successful",
                "user_id": user.id,
                "email": user.email
            })
        else:
            return JsonResponse({
                "message": "Invalid phone or password",
            }, status=401)

    return JsonResponse({
        "message": "Only POST method is allowed"
    }, status=405)

def logout_view(request):
    """logout"""
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({
            "message": "Logout Successful",
        }, status=200)

    return JsonResponse({
        "message": "user is not logged in",
    }, status=401)

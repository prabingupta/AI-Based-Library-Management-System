from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")
    return redirect("accounts:login")


def error_404(request, exception):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)


def error_403(request, exception):
    return render(request, "errors/403.html", status=403)


@login_required
@require_POST
def chatbot_api(request):
    try:
        body = json.loads(request.body)
        user_message = body.get("message", "").strip()
        chat_history = body.get("history", [])

        if not user_message:
            return JsonResponse({"error": "Message is required."}, status=400)

        if len(user_message) > 500:
            return JsonResponse({"error": "Message too long."}, status=400)

        from core.services.chatbot import chat_with_gemini

        response = chat_with_gemini(user_message, chat_history)
        return JsonResponse({"response": response})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request."}, status=400)
    except Exception:
        return JsonResponse({"error": "Something went wrong."}, status=500)

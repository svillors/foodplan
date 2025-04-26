from django.shortcuts import render
from subscriptions.models import Subscription


def index(request):
    active_subscription = None
    if request.user.is_authenticated:
        active_subscription = Subscription.objects.filter(user=request.user, is_active=True).first()
    return render(request, "index.html", {"active_subscription": active_subscription})

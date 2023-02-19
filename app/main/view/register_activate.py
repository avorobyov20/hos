from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.signing import BadSignature
from main.utilities import signer
from main.models import AdvUser


def user_activate(request, sign):
    """32.4.2 Веб-страницы активации пользователя"""

    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, "main/bad_signature.html")
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = "main/user_is_activated.html"
    else:
        template = "main/activation_done.html"
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

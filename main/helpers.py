import base64
import json

from django.contrib.auth.views import login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.encoding import force_bytes

from .forms import *


def base_context(request):
    context = {
        'signup_form': SignUpForm(request.POST)
    }
    return context


def activate(request, url):
    data = json.loads(base64.b64decode(force_bytes(url)))
    user_id = data['user_id']
    user_confirmation = data['key']
    user = User.objects.get(pk=int(user_id))
    user.confirm_email(user_confirmation)
    if user.is_confirmed:
        user.is_active = True
        user.save()
        if user is not None:
            login(request, user)
        return redirect(reverse('main'))
    else:
        return HttpResponse('Link is invalid')

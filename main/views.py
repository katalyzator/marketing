# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def index_view(request):
    context = {}
    template = 'index.html'

    return render(request, template, context)

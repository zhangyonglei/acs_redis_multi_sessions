# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import Random
from django.http import HttpResponse

def test(request):
    request.session['username'] = Random().randint(1, 100000)

    return HttpResponse("OK")

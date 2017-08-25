# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from importlib import import_module

from django.test import TestCase

class SessionTestCase(TestCase):
    def test_something(self):
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        print '-OK'


class SimpleTest(TestCase):
   def test_stuff(self):

      # ugly and long create of session if session doesn't exist
      from django.conf import settings
      engine = import_module(settings.SESSION_ENGINE)
      store = engine.SessionStore()
      store.save()  # we need to make load() work, or the cookie is worthless
      self.cookies = {}
      self.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
      print store.session_key

      #   ugly and long set of session
      session = self.client.session
      session['foo'] = 33
      session.save()
      print self.client.session



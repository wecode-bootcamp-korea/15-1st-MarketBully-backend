#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from .views import SignupView, SigninView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/signin', SigninView.as_view()),
]

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from .views import SignupView, SigninView, FindAccountView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/signin', SigninView.as_view()),
    path('/findaccount', FindAccountView.as_view())
]

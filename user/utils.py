#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, jwt, requests

from django.http             import jsonresponse
from django.core.exceptions  import ObjectDoesNotExist

from my_settings             import SECRET_KEY, ALGORITHM
from .models                 import User

    
def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs): 

        access_token = request.headers.get("Authorization", None)  

        try:
            token_payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user = User.objects.get(account = token_payload["account"]) 
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"EXPIRED_TOKEN"}, status=401) 

        except jwt.DecodeError: 
            return JsonResponse({"message":"INVALID_TOKEN"}, status=401) 

        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=401) 
        
        return JsonResponse({"message":"NEED_LOGIN"}, status=401)

    return wrapper

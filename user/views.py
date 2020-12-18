import json, bcrypt
import re

from django.views import View
from django.http import JsonResponse
from .models import User, Gender, Grade, TermsAndCondition, Address
from my_settings import SECRET_KEY

# Create your views here.
class SignupView(View): 
    def validate_account(self, account):  
        REGEX_ACCOUNT = '^[a-z0-9]{6,}$'

        if not re.match(REGEX_ACCOUNT, account):
            return False
        return True


    def validate_password(self, password):
        REGEX_PASSWORD = '^[A-Za-z0-9@#$%^&+=]{10,}$'

        if not re.match(REGEX_PASSWORD, password):
            return False
        return True

    def validate_email(self, email): 
        REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if not re.match(REGEX_EMAIL, email):
            return False
        return True
    

    def validate_phone_number(self, phone_number):
        REGEX_PHONE_NUMBER = '^\d{3}?[-]\d{4}?[-]\d{4}$'
        
        if not re.match(REGEX_PHONE_NUMBER, phone_number):
            return False
        return True
    

    def post(self, request):
        data = json.loads(request.body)

        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        birth_date  = data.get('birth_date')
        recommender = data.get('recommender')
        event_name  = data.get('event_name')

        try:

            if not self.validate_account(data['account']):
                return JsonResponse({"message":"INVALID_ID"}, status=400)

            if User.objects.filter(account=data['account']).exists():
                return JsonResponse({"message":"USER_EXIST"}, status=409)

            if not self.validate_password(data['password']):
                return JsonResponse({"message": "INVALID_PW"}, status=400)

            if not self.validate_email(data['email']):
                return JsonResponse({"message":"INVALID_EMAIL"}, status=400)

            if not self.validate_phone_number(data['phone_number']):
                return JsonResponse({"message":"INVALID_PHONE_NUMBER"}, status=400)

            else:
                User.objects.create(
                    account             = data['account'],
                    password            = hashed_pw,
                    name                = data['name'],
                    email               = data['email'],
                    phone_number        = data['phone_number'],
                    gender              = Gender(id=3),
                    birth_date          = birth_date,
                    recommender         = recommender,
                    event_name          = event_name,
                    grade               = Grade(id=1),
                    terms_and_condition = TermsAndCondition(id=1),
                    mileage             = 0
                    )
                return JsonResponse({"message":"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

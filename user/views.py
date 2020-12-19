import json, bcrypt
import re

from django.views import View
from django.http import JsonResponse
from .models import User, Gender, Grade, TermsAndCondition, Address
from my_settings import SECRET_KEY

# Create your views here.
class SignupView(View): 
    def validate_account(self, account): # 6자 이상의 영문 또는 영문과 숫자를 조합 
        REGEX_ACCOUNT_1 = '^[a-z]{6,}$'                      # 영문 6자 이상
        REGEX_ACCOUNT_2 = '^(?=.*[0-9])(?=.*[a-z]).{6,}$'    # 영문+숫자 6자 이상

        if not re.match(REGEX_ACCOUNT_1, account) and not re.match(REGEX_ACCOUNT_2, account):
            return False
        return True

    def validate_password(self, password): # 10자 이상, 영문/숫자/특수문자만 허용하며 2개 이상 조합
        REGEX_PASSWORD_1 = '^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$'                       # 영문+숫자 10자 이상
        REGEX_PASSWORD_2 = '^(?=.*[!@#$%^&*()_+])(?=.*[a-zA-Z]).{10,}$'              # 영문+특수문자 10자 이상
        REGEX_PASSWORD_3 = '^(?=.*[0-9])(?=.*[!@#$%^&*()_+]).{10,}$'                 # 숫자+특수문자 10자 이상
        REGEX_PASSWORD_4 = '^(?=.*[0-9])(?=.*[!@#$%^&*()_+])(?=.*[a-zA-Z]).{10,}$'   # 영문+숫자+특수문자 10자 이상

        if not re.match(REGEX_PASSWORD_1, password) and not re.match(REGEX_PASSWORD_2, password) \
            and not re.match(REGEX_PASSWORD_3, password) and not re.match(REGEX_PASSWORD_4, password):
            return False
        return True

    def validate_email(self, email): # @, . 포함 
        REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if not re.match(REGEX_EMAIL, email):
            return False
        return True
    

    def validate_phone_number(self, phone_number):
        REGEX_PHONE_NUMBER = '^\d{3}?[-]\d{3,4}?[-]\d{4}$'
        
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


            if User.objects.filter(account=data['account']).exists():
                return JsonResponse({"message":"USER_EXIST"}, status=409)

            if not self.validate_account(data['account']):
                return JsonResponse({"message":"INVALID_ID"}, status=400)

            if not self.validate_password(data['password']):
                return JsonResponse({"message": "INVALID_PW"}, status=400)

            if not self.validate_email(data['email']):
                return JsonResponse({"message":"INVALID_EMAIL"}, status=400)

            if not self.validate_phone_number(data['phone_number']):
                return JsonResponse({"message":"INVALID_PHONE_NUMBER"}, status=400)

            user_model = User(
                account             = data['account'],
                password            = hashed_pw,
                name                = data['name'],
                email               = data['email'],
                phone_number        = data['phone_number'],
                gender_id           = data['gender_id'],
                birth_date          = birth_date,
                recommender         = recommender,
                event_name          = event_name,
                grade_id            = data['grade_id'],
                terms_and_condition = TermsAndCondition(id=1),
                mileage             = 0
                )
            
            user_model.save()

            Address(
                name=data['name'],
                user=User.objects.get(id=user_model.id),
                is_active=False
                ).save()
            
            return JsonResponse({"message":"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        


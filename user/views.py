import json, bcrypt, jwt
import re

from django.views   import View
from django.http    import JsonResponse
from django.db      import transaction

from .models        import User, Gender, Grade, TermsAndCondition, Address
from my_settings    import SECRET_KEY, ALGORITHM

# Create your views here.
class SignupView(View): 
    def validate_account(self, account): # 6자 이상의 영문 또는 영문과 숫자를 조합 
        REGEX_ACCOUNT_1 = '^[a-z]{6,}$'                      # 영문 6자 이상
        REGEX_ACCOUNT_2 = '^(?=.*[0-9])(?=.*[a-z]).{6,}$'    # 영문+숫자 6자 이상
        
        return re.match(REGEX_ACCOUNT_1, account) or re.match(REGEX_ACCOUNT_2, account)

    def validate_password(self, password): # 10자 이상, 영문/숫자/특수문자만 허용하며 2개 이상 조합
        REGEX_PASSWORD_1 = '^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$'                       # 영문+숫자 10자 이상
        REGEX_PASSWORD_2 = '^(?=.*[!@#$%^&*()_+])(?=.*[a-zA-Z]).{10,}$'              # 영문+특수문자 10자 이상
        REGEX_PASSWORD_3 = '^(?=.*[0-9])(?=.*[!@#$%^&*()_+]).{10,}$'                 # 숫자+특수문자 10자 이상
        REGEX_PASSWORD_4 = '^(?=.*[0-9])(?=.*[!@#$%^&*()_+])(?=.*[a-zA-Z]).{10,}$'   # 영문+숫자+특수문자 10자 이상

        return re.match(REGEX_PASSWORD_1, password) or re.match(REGEX_PASSWORD_2, password) \
            or re.match(REGEX_PASSWORD_3, password) or re.match(REGEX_PASSWORD_4, password)

    def validate_email(self, email): # @, . 포함 
        REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        return re.match(REGEX_EMAIL, email)
    

    def validate_phone_number(self, phone_number):
        REGEX_PHONE_NUMBER = '^\d{3}?[-]\d{3,4}?[-]\d{4}$'
        
        return re.match(REGEX_PHONE_NUMBER, phone_number)
    

    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(account=data['account']).exists():
                return JsonResponse({"message":"USER_EXIST"}, status=409)

            if not self.validate_account(data['account']):
                return JsonResponse({"message":"INVALID_ACCOUNT"}, status=400)

            if not self.validate_password(data['password']):
                return JsonResponse({"message": "INVALID_PW"}, status=400)

            if not self.validate_email(data['email']):
                return JsonResponse({"message":"INVALID_EMAIL"}, status=400)

            if not self.validate_phone_number(data['phone_number']):
                return JsonResponse({"message":"INVALID_PHONE_NUMBER"}, status=400)

            hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            birth_date  = data.get('birth_date')
            recommender = data.get('recommender')
            event_name  = data.get('event_name')

            with transaction.atomic():  # user_model.save(), address.save() 중 하나만 실패해도 모든 commit rollback 
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
                    name      = data['address.name'],
                    user_id   = user_model.id,
                    is_active = True
                    ).save()
                
                return JsonResponse({"message":"SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)


class CheckAccountView(View):
    def post(self, request):
        data = json.loads(request.body)

        REGEX_ACCOUNT_1 = '^[a-z]{6,}$'                      
        REGEX_ACCOUNT_2 = '^(?=.*[0-9])(?=.*[a-z]).{6,}$' 

        try:
            if user_model.account == '':
                return JsonResponse({"message":"ACCOUNT_NOT_ENTERED"}, status=400)
            
            if User.objects.filter(account=data["account"]).exists():
                return JsonResponse({"message":"ACCOUNT_EXIST"}, status=409)
            
            return re.match(REGEX_ACCOUNT_1, account) or re.match(REGEX_ACCOUNT_2, account)

            return JsonResponse({"message":"SUCCESS"}, status=200)
    
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)


class CheckEmailView(View):
    def post(self, request):
        data = json.loads(request.body)

        REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        try:
            if user_model.email == '':
                return JsonResponse({"message":"EMAIL_NOT_ENTERED"}, status=400)

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message":"EMAIL_EXIST"}, status=409)

            return re.match(REGEX_EMAIL, email)

            return JsonResponse({"message":"SUCCESS"}, status=200)
    
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)


class SigninView(View):
        
    def post(self, request):
        data = json.loads(request.body)
        
        try: 
            
            if not User.objects.filter(account=data["account"]).exists():
                return JsonResponse({"message":"UNKNOWN_USER"}, status=404)

            if User.objects.filter(account=data["account"]).exists():

                user = User.objects.get(account=data["account"]) 
                hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
   
                    access_token = jwt.encode({'id':user.account}, SECRET_KEY, ALGORITHM).decode('utf-8')

                    return JsonResponse({"ACCESS_TOKEN":access_token}, status=201)

                return JsonResponse({"message": "INVALID_PW"}, status = 401)

            return JsonResponse({"message":"INVALID_ACCOUNT"}, status=401)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)


#class FindAccountView(view):
#
#    def post(self, request):
#        data = json.loads(request.body)
#
#        try:
#
#            if not User.objects.filter(name=data["name"], email=data["email"]).exists():
#                return JsonResponse({"message": ""})
#
#            if User.objects.filter(name=data["name"], email=data["email"]).exists():
#                account = User.objects.get(account=data["account"])

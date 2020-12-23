import json

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from .models    import Question
from user.utils import signin_decorator


class QuestionView(View):
    @signin_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            Question.objects.create(
                author_id  = request.user.id,
                product_id = data['product_id'],
                title      = data['title'],
                contents   = data['contents'],
                is_private = data['private'] if data.get('private') else False,
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + str(e.args[0])}, status=400)
        except ValidationError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + str(e.args[0])}, status=400)

    def get(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
            question_post = {
                'id'         : question.id,
                'product_id' : question.product_id,
                'title'      : question.title,
                'contents'   : question.contents,
                'private'    : question.is_private,
                'create_at'  : question.created_at,
            }

            return JsonResponse({"MESSAGE": "SUCCESS", "question_post": question_post}, status=201)

        except Question.DoesNotExist as e:
           return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)

    @signin_decorator
    def patch(self, request, question_id):
        try:
            data = json.loads(request.body)

            question = Question.objects.get(id=question_id, author_id=request.user.id)
            if data.get('title'):
                question.title = data.get('title')
            if data.get('contents'):
                question.contents = data.get('contents')
            if data.get('private'):
                question.is_private = data.get('private')
            question.save()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)
        except Question.DoesNotExist:
            return JsonResponse({"MESSAGE": "QUESTION_DOES_NOT_EXIST"}, status=400)

    @signin_decorator
    def delete(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id, author_id=request.user.id)
            question.delete()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=204)

        except Question.DoesNotExist:
            return JsonResponse({"MESSAGE": "QUESTION_DOES_NOT_EXIST"}, status=400)


class QuestionListView(View):
    def get(self, request, product_id):
        try:
            offset = int(request.GET.get('offset'), 0)
            limit  = int(request.GET.get('limit'), 10)
            limit += offset

            questions = Question.objects.order_by('-create_at').filter(product_id=product_id)

            question_list = [{
                'id'        : question.id,
                'product_id': question.product_id,
                'title'     : question.title,
                'contents'  : question.contents,
                'private'   : question.is_private,
                'create_at' : question.created_at,

            }for question in questions[offset:limit]]

            return JsonResponse({'MESSAGE': 'SUCCESS', "question_list": question_list}, status=200)

        except Exception as e:
            return JsonResponse({'message' : 'ERROR => ' + e.args[0]}, status = 400)
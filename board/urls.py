from django.urls    import path
from .views  import QuestionView, QuestionListView

urlpatterns = [
    path('/question', QuestionView.as_view()),
    path('/question/<int:question_id>', QuestionView.as_view()),
    path('/question/product/<int:product_id>', QuestionListView.as_view()),
]
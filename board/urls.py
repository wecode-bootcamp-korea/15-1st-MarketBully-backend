from django.urls    import path

from .views  import QuestionView, QuestionListView
from .views  import ReviewView, ReviewListView


urlpatterns = [
    path('/question', QuestionView.as_view()),
    path('/question/<int:question_id>', QuestionView.as_view()),
    path('/question/product/<int:product_id>', QuestionListView.as_view()),

    path('/review', ReviewView.as_view()),
    path('/review/<int:review_id>', ReviewView.as_view()),
    path('/review/product/<int:product_id>', ReviewListView.as_view()),
]
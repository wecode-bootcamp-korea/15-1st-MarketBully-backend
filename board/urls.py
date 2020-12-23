from django.urls    import path
from .views  import ReviewView, ReviewListView

urlpatterns = [
    path('/review', ReviewView.as_view()),
    path('/review/<int:review_id>', ReviewView.as_view()),
    path('/review/product/<int:product_id>', ReviewListView.as_view()),
]
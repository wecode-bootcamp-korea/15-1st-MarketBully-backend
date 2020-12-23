from django.urls    import path
from product.views  import (
    ProductDetailView,
    ProductListView,
    MdChoiceView,
    CategoryView,
    )

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/md-choice', MdChoiceView.as_view()),
    path('/category', CategoryView.as_view()),
]

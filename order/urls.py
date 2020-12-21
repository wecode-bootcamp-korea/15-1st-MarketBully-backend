from django.urls import path


from .views import CartView, OftenBuyingView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/often_buying', OftenBuyingView.as_view()),
]
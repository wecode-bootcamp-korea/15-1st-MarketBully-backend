import json
from datetime import datetime

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from order.models import Cart, Order
from user.models  import Address


class CartView(View):
    # @login_required
    @transaction.atomic
    def post(self, request):  # 장바구니에 상품 담기
        try:
            data = json.loads(request.body)
            user_id = "3"  # 데코레이터 나오기 전까지 사용자 임의지정

            # 사용자 장바구니 가져오기, 있으면 가져오고 없으면 생성하여 가져옴
            if not Order.objects.filter(user_id=user_id, status_id=1).exists():
                new_order = Order.objects.create(
                    user_id           = user_id,
                    order_number      = user_id + "-" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f'),
                    status_id         = 1,
                    address_id        = Address.objects.get(user_id=user_id, is_active=1).id,
                    payment_method_id = 1
                )
                new_order_id = new_order.id
            else:
                new_order_id = Order.objects.get(user_id=user_id, status_id=1).id

            # 사용자의 장바구니에 이미 해당 상품이 있는 경우 전달된 quantity 만큼 그 수량을 올림
            if Cart.objects.filter(order_id=new_order_id, product_id=data['product_id']).exists():
                product_in_cart = Cart.objects.get(order_id=new_order_id, product_id=data['product_id'])
                product_in_cart.quantity += int(data['quantity'])
                product_in_cart.save()
                return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
            else:
                Cart.objects.create(
                    order_id   = new_order_id,
                    product_id = data['product_id'],
                    quantity   = data['quantity'],
                )
                return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)


    # @login_required
    def get(self, request):  # 장바구니 상품 조회
        try:
            user_id = 3  # 데코레이터 나오기 전까지 임의로 사용자 지정
            order_cart_id = Order.objects.get(user_id=user_id, status=1).id   # status=1 -> 장바구니
            cart = Cart.objects.filter(order_id=order_cart_id).prefetch_related("product__discount", "product__packing_type")

            items_in_cart = [{
                "id"               : item.id,
                "product_id"       : item.product.id,
                "name"             : item.product.name,
                "quantity"         : item.quantity,
                "price"            : item.product.price,
                "discount_rate"    : float(item.product.discount.percentage),
                "is_soldout"       : item.product.is_soldout,
                "cart_packing_type": item.product.packing_type.cart_packing_type,
                "image_url"        : item.product.image_url,
                "selected"         : False,
            }for item in cart]

            return JsonResponse({"MESSAGE": "SUCCESS", "items_in_cart": items_in_cart}, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({"MESSAGE": "SUCCESS", "items_in_cart":[]}, status=200)


    # @login_required
    def delete(self, request):
        try:
            data = json.loads(request.body)
            item = Cart.objects.get(id=data['cart_item_id'])
            item.delete()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=204)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)
        except Cart.DoesNotExist:
            return JsonResponse({"MESSAGE": "ITEM_DOES_NOT_EXIST"}, status=400)


    # @login_required
    def patch(self, request):
        try:
            data      = json.loads(request.body)
            delta     = data['delta']
            cart_item = Cart.objects.get(id=data['cart_item_id'])

            if delta == "minus":
                if cart_item.quantity == 1:
                    return JsonResponse({'MESSAGE': 'ITEM QUANTITY IS 1'}, status=400)
                cart_item.quantity -= 1
            elif delta == "plus":
                cart_item.quantity += 1
            else:
                return JsonResponse({"MESSAGE": "KEY_ERROR => 'delta' SHOULD BE 'minus' OR 'plus'"}, status=400)
            cart_item.save()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)

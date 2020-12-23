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
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = "1"

            new_order, flag = Order.objects.get_or_create(
                user_id    = user_id,
                status_id  = 1,
                address_id = Address.objects.get(user_id=user_id, is_active=1).id,
                payment_method_id = 1,
            )
            if not flag:
                new_order.order_number = user_id + "-" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                new_order.save()

            new_order_id = new_order.id

            if Cart.objects.filter(order_id=new_order_id, product_id=data['product_id']).exists():
                product_in_cart = Cart.objects.get(order_id=new_order_id, product_id=data['product_id'])
                product_in_cart.quantity += int(data['quantity'])
                product_in_cart.save()
                return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

            Cart.objects.create(
                order_id   = new_order_id,
                product_id = data['product_id'],
                quantity   = data['quantity'],
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)


    # @login_required
    def get(self, request):
        try:
            user_id = "1"
            cart = Cart.objects.filter(order__user_id=user_id, order__status=1).prefetch_related("product__discount", "product__packing_type")

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
                "selected"         : item.is_selected,
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

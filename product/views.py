import json

from django.views       import View
from django.http        import JsonResponse

from my_settings        import SECRET_KEY
from .models            import (
                                Category,
                                Subcategory,
                                Product,
                                Discount,
                                Origin,
                                PackingType
                               )

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.select_related('discount', 'delivery_type', 'origin', 'packing_type').prefetch_related('productdescription_set', 'detailedimage_set').get(id=product_id)

            product_detail = {
                'id'                    : product.id,
                'name'                  : product.name,
                'subtitle'              : product.subtitle,
                'price'                 : product.price,
                'discount_name'         : product.discount.name,
                'discount_percentage'   : product.discount.percentage,
                'is_soldout'            : product.is_soldout,
                'image_url'             : product.image_url,
                'sales_unit'            : product.sales_unit,
                'weight'                : product.weight,
                'delivery_type'         : product.delivery_type.name,
                'origin'                : product.origin.name,
                'packing_type'          : product.packing_type.packing_type,
                'allergy'               : product.allergy,
                'expiration_date'       : product.expiration_date,
                'notice'                : product.notice,
                'content'               : product.productdescription_set.get().content,
                'product_image_url'     : product.detailedimage_set.get().product_image_url,
                'description_image_url' : product.detailedimage_set.get().description_image_url
                }


        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_NOT_FOUND'}, status = 404)
        return JsonResponse({'message': 'SUCCESS', 'product_detail': product_detail}, status = 200)

import json

from django.http        import JsonResponse
from django.views       import View

from .models            import Category, Subcategory, Product

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

class ProductListView(View):
    def get(self, request):
        try:
            offset         = int(request.GET.get('offset', 0))
            limit          = int(request.GET.get('limit', 100))
            subcategory_id = request.GET.get('subcategory', None)
            categories     = Category.objects.prefetch_related('subcategory_set')
            products       = Product.objects.select_related('discount', 'subcategory').filter(subcategory=subcategory_id) if subcategory_id else Product.objects.all()

            product_list = [{
                'id'                  : product.id,
                'name'                : product.name,
                'subtitle'            : product.subtitle,
                'price'               : product.price,
                'discount_percentage' : product.discount.percentage,
                'is_soldout'          : product.is_soldout,
                'image_url'           : product.image_url,
                } for product in products[offset:limit]]

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status = 400)

        return JsonResponse({'message': 'SUCCESS', 'product_list': product_list}, status = 200)

class CategoryView(View):
    def get(self,request):
        categories = Category.objects.prefetch_related('subcategory_set')

        categories = [{
            'id'          : category.id,
            'name'        : category.name,
            'subcategories' : [{
                'id'      : subcategory.id,
                'name'    : subcategory.name
                } for subcategory in category.subcategory_set.all()]
            } for category in categories]

        return JsonResponse({'message': 'SUCCESS', 'categories': categories}, status = 200)

class MdChoiceView(View):
    def get(self, request):
        try:
            products = Product.objects.select_related('discount', 'subcategory')

            product_list = [{
                'id'                  : product.id,
                'name'                : product.name,
                'subtitle'            : product.subtitle,
                'price'               : product.price,
                'discount_percentage' : product.discount.percentage,
                'is_soldout'          : product.is_soldout,
                'image_url'           : product.image_url,
                'subcategory_id'      : product.subcategory.id,
                'subcategory_name'    : product.subcategory.name
                } for product in products]

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status = 400)

        return JsonResponse({'message': 'SUCCESS', 'product_list': product_list}, status = 200)

import json

def cart_counter(request):
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        products_list = json.loads(product_ids)
        products_list_ids = [k['id'] for k in products_list]
        products_count_in_cart = len(products_list_ids)
    else:
        products_count_in_cart = 0
    return {
        'products_count_in_cart': products_count_in_cart
        }
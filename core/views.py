import json
from django.db.models import Q
from django.shortcuts import redirect, render
from .forms import FeedbackForm, MakeOrderForm
from .models import Customer, Order, Product
# Create your views here.

def home_page_view(request):
    products = Product.objects.filter(quantity__gt=0)
    return render(request, 'home.html', {'products': products})


def about_page_view(request):
    return render(request, 'about.html')


def feedback_page_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid:
            form.save()
            return render(request, 'feedback_sent.html')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})


# return all products that match search pattern
def search_products_view(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            result_product = Product.objects.filter((Q(name__icontains=query) |
            Q(categ_id__name__icontains=query))
            & Q(quantity__gt=0))
            return render(request, 'search.html', {'products': result_product})
        else:
            products = Product.objects.filter(quantity__gt=0)
            return render(request, 'home.html', {'products': products})


# TODO : Send products details to cart page and calc total price
def cart_page_view(request):
    # 1 - Fetching products whose ids in cookies
    products = None
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_ids = json.loads(product_ids)
            quantities_list = [qty['ordered_qty'] for qty in product_ids]
            products_id_in_cart = [k['id'] for k in product_ids]
            length = len(products_id_in_cart)
            #products = Product.objects.filter(id__in=products_id_in_cart)
            # 2 - Calculate Total
            total = 0
            prices = []
            products = []
            for p in products_id_in_cart:
                product = Product.objects.get(id=p)
                products.append(product)
                prices.append(product.price)
            for p in range(length):
                total += (prices[p] * quantities_list[p])
            zipped_list = zip(products, quantities_list)
        else:
            products = None
            total = 0
            zipped_list = None
    else:
        products = None
        total = 0
        zipped_list = None

    return render(request, 'view_cart_items.html', {'total': total, 'zipped_list': zipped_list})


# TODO : add item to cart and set ordered quantities
def add_to_cart_view(request, pk):
    if request.method == 'POST':
        # take ordered qty and product id to create cookie
        ordered_quantity = int(request.POST.get('ordered_qty'))
        # Update Counter
        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            product_ids = json.loads(product_ids)
            products_list_ids = [k['id'] for k in product_ids]
        # if pk of product exist in counter don't incremment counter
            if pk in products_list_ids:
                products_count_in_cart = len(set(products_list_ids))
        # else : (new product in cart) increment counter
            else:
                products_count_in_cart = len(set(products_list_ids)) + 1
        else:
            products_count_in_cart = 1
        # Back to home page
        products = Product.objects.filter(quantity__gt=0)
        response = render(request, 'home.html',
            {'products': products, "products_count_in_cart": products_count_in_cart})
        # Update Cookie by adding product id and qty
        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            products_list = json.loads(product_ids)
            products_ids_list = [i['id'] for i in products_list ]
            if pk not in products_ids_list:
                products_list.append({'id': pk, 'ordered_qty': ordered_quantity})
                response.set_cookie('product_ids',
                json.dumps(products_list))
        else:
            response.set_cookie('product_ids',
            json.dumps([{'id': pk, 'ordered_qty': ordered_quantity}]))
        return response
    else:
        product = Product.objects.get(id=pk)
        return render(request, 'add_item_to_cart.html', {'product': product})


# TODO : delete item from cart, update the counter and update (set) cookies
def delete_cart_item_view(request, pk):
    # 1 - Remove product id from cookie
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_list_in_cart = json.loads(product_ids)
        products_ids_list = [i['id'] for i in product_list_in_cart]
        products_ids_list.remove(pk)
    response = redirect('cart')
    # 3 - Update the cookie after reomving id
    if products_ids_list:
        # delete item from cookie
        products_list = [i for i in product_list_in_cart if i['id'] != pk]
        # transform dict to json and set cookie
        response.set_cookie('product_ids',json.dumps(products_list))
    else:
        response.delete_cookie('product_ids')
    return response

# TODO : view form order to get all order data from user
def make_order_view(request, total):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MakeOrderForm(request.POST)
            if form.is_valid:
                address = request.POST.get('shipping-address')
                #phone = request.POST.get('mobile')
                try:
                    customer = Customer.objects.get(user_id=request.user.id)
                except:
                    # ch = Customer.objects.filter(phone=phone)
                    # if ch:
                    #     print("NUMBER ALREADY TAKEN FOR ANOTHER CUSTOMER")
                    # else:
                    #     print("NEW NUMBER")
                    customer = Customer.objects.create(user_id=request.user.id, address=address)
                # 1 - Create order record
                email = request.user.email
                product_ids = request.COOKIES['product_ids']
                product_ids = json.loads(product_ids)
                products_id_in_cart = [k['id'] for k in product_ids]
                quantities_list = [qty['ordered_qty'] for qty in product_ids]
                products = Product.objects.filter(id__in=products_id_in_cart)
                order = Order.objects.create(customer=customer, status='Pending',
                    mobile=request.user.phone, email=email, address=address, total=total)
                order.products.add(*products)
                #2 - Update remaining quantity of products
                ids_qty = zip(products_id_in_cart, quantities_list)
                for id,qty in ids_qty:
                    product = Product.objects.get(id=id)
                    remaining = product.quantity
                    remaining = remaining - qty
                    Product.objects.filter(id=id).update(quantity=remaining)
                response = redirect('home')
                response.delete_cookie('product_ids')
                return response
        else:
            form = MakeOrderForm()
            return render(request, 'make_order.html', {'form': form, 'total': total})
    else:
        return redirect('login')


# TODO : view customer orders
def view_customer_order(request):
    customer = Customer.objects.get(user_id=request.user.id)
    customer_orders = Order.objects.filter(customer=customer)
    return render(request, 'view_customer_orders.html', {'orders': customer_orders})

# TODO : Delete cookie and logout
def logout_and_delete_cookie_view(request):
    response = redirect('logout')
    response.delete_cookie('product_ids')
    return response
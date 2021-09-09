from django import forms
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.template import context
from .forms import FeedbackForm, MakeOrderForm
from .models import Order, Product
from django.db.models import Q
from django.urls import reverse
import json
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
            products_id_in_cart = [k['id'] for k in product_ids]
            products = Product.objects.filter(id__in=products_id_in_cart)

            # 2 - Calculate Total
            total = 0
            for product in products:
                total = total + product.price
        else:
            products = None
            total = 0
    else:
        products = None
        total = 0

    return render(request, 'view_cart_items.html', {'products_list': products, 'total': total})

def add_to_cart_view(request, pk):
    products = Product.objects.filter(quantity__gt=0)
    # 1 - Update Cart Counter
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
    response = render(request, 'home.html', {'products': products, "products_count_in_cart": products_count_in_cart})
    
    # 2 - Add Product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        products_list = json.loads(product_ids)
        products_list_ids = [k['id'] for k in products_list]
        if pk not in products_list_ids:
            products_list.append({"id": pk, "ordered_qty": 1})
            response.set_cookie('product_ids', json.dumps(products_list))

    else:
        response.set_cookie('product_ids', json.dumps([{'id': pk, 'ordered_qty': 1}]))
        
    return response

# TODO : delete item from cart, update the counter and update (set) cookies
def delete_cart_item_view(request, pk):
    # 1 - Remove product id from cookie
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_list_in_cart = json.loads(product_ids)
        products_ids_list = [i['id'] for i in product_list_in_cart]
        # to fix error : item x not in list ( occur if we refresh after delete item)
        if pk not in products_ids_list:
            #cart page view
            return redirect('cart')
        else:
            products_ids_list.remove(pk)
            products = Product.objects.filter(id__in=products_ids_list)

            # Calculate total price
            total = 0
            for product in products:
                total = total + product.price

            # 2 - Update cart counter
            products_count_in_cart = len(products_ids_list)
    else:
        products = {}

    response = render(request, 'view_cart_items.html', {'products_list': products, 'products_count_in_cart': products_count_in_cart, 'total': total})
    
    # 3 - Update the cookie after reomving id
    if products != {}:
        # delete item from cookie
        products_list = [i for i in product_list_in_cart if i['id'] != pk]
        # transform dict to json and set cookie
        response.set_cookie('product_ids',json.dumps(products_list))
    else:
        response.delete_cookie('product_ids')
    return response

def recalculate_total_price_view(request):
    # 1 - fetch all cart products from cookies
    #if 'product_ids' in request.COOKIES:
    #    product_ids = request.COOKIES['product_ids']
    #    product_ids = json.loads(product_ids)
    #    products_ids_list = [i['id'] for i in product_ids]
    #    items_count = len(products_ids_list)
    # cart_products = Product.objects.filter(id__in=products_ids_list)
    # total_price = 0
    # for product in cart_products:
    #     qty = request.GET.get('ordered_quantity')
    #     print("QTY ", qty)
    #     total_price = total_price + product.price
    # print("Total ", total_price) 
    # # 2 - calcuate total = product.price * quantity

    return cart_page_view(request)

# TODO : view form order to get all order data from user
def make_order_view(request, total):
    if request.method == 'POST':
        form = MakeOrderForm(request.POST)
        if form.is_valid:
            form.save()
            return(request, 'home.html')
    else:
        form = MakeOrderForm()
    return render(request, 'make_order.html', {'form': form, 'total': total})
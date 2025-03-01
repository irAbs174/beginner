from user_accounts.models import user_accounts as UserModel
from .serializers import CartSerializer, SupportSerializer
from django.contrib.auth.decorators import login_required
from index.extensions.http_service import get_client_ip
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from product.models import InventoryItem, Discount
from django.http import HttpRequest, JsonResponse
from .models import Cart, Support, SupportRequest
from django.shortcuts import render, redirect
from rest_framework import generics, filters
from root.local_settings import fadax_API
from product.forms import DiscountForm
from django.contrib import messages
from .models import Fadax_payment
import requests
import json


class CartViewSet(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    ordering_fields = ['user', 'product_id', 'product_title', 'product_title', 'product_collection', 'quantity', 'price', 'image', 'color', 'color_quantity',]
    search_fields = ['user', 'product_title']
    
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    

class SupportViewSet(generics.ListCreateAPIView):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer
    ordering_fields = ['room', 'support_user','message','support_status','timestamp', 'time']
    search_fields = ['support_user']
    
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

@csrf_exempt
def load_cart_data(request):
    context = []
    if request.user.is_authenticated:
        for i in Cart.objects.all().filter(user = request.user.phoneNumber):
            if Cart.objects.filter(user=request.user.phoneNumber):
                if (Cart.objects.filter(user=request.user.phoneNumber)[0].price == 0):
                    context = {}
                else:
                    item = {
                        'id': i.product_id,
                        'title': i.product_title,
                        'image': i.image,
                        'number': i.quantity,
                        'price': i.price,
                        'sub_total': i.quantity * i.price,
                        'color_quantity': i.color_quantity,
                        'offer_code_value': i.offer_code_value,
                        'total_price': i.total_price,
                    }
                    context.append(item)
            else:
                context = {}
        return JsonResponse({'status': context, 'success': True})

    else:
        return JsonResponse({'status': 'لطفا ابتدا در سایت ثبت نام کنید', 'success':  False})
    
    
@csrf_exempt
def support_index(request):
    return render(request, 'support/index.html')

@csrf_exempt
def support_add(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                support_user = request.user.phoneNumber
                support_status = request.POST.get('support_status')
                support_room = request.POST.get('support_room')
                if (Support.objects.filter(room = support_room ,support_user=request.user.phoneNumber)):
                    return JsonResponse({'status':"شما در حال حاظر یک پشتیبانی فعال دارید", 'success': False})
                else:
                    Support.objects.create(
                        room = support_room,
                        support_user = support_user,
                        support_status = support_status,
                        message = 'خوش آمدید. لطفا پیام خود را وارد کنید',
                    )
                    SupportRequest.objects.create(
                        user = support_user,
                        support_request = support_room,
                    )
                    return JsonResponse({'status':"پشتیبانی با موفقیت ایجاد شد. اکنون به صفحه پشتیبانی منتقل میشوید", 'success': True})
            except:
                return JsonResponse({'status':"با عرض پوزش در حال حاظر امکان پشتیبانی آنلاین وجود ندارد کمی بعد مجددا تلاش کنید", 'success': False})
        else:
            return JsonResponse({'status':"برای دریافت پشتیبانی ابتدا ثبت نام کنید یا وارد حساب کاربری خود شوید", 'success': False})
    else:
        return JsonResponse({'status':"درخواست معتبر نیست", 'success': False})

@login_required
def support_room(request, room):
    return render(request, 'support/room.html')

@login_required
def cart_view(request):

    phone = request.user.phoneNumber
    list_cart = Cart.objects.filter(user=phone)
    cart_count = list_cart.count()
    # SEND CART DATA TO PAGE(http response)
    discount = DiscountForm()
    context = {
        'discount': discount,
        'cart_list': cart_count,
    }
    return render(request, 'products/cart/cart.html',context)

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated :
            if Cart.objects.filter(user=request.user.phoneNumber):
                if (Cart.objects.filter(user=request.user.phoneNumber)[0].price == 0):
                    Cart.objects.filter(user=request.user.phoneNumber).delete()
            pq = InventoryItem.objects.all().public().live().search(request.POST.get('id'))
            product_id = pq[0].id
            product_title = pq[0].title,
            product_collection = pq[0].collection.values()[0]['title'],
            product_quantity = int(request.POST.get('number'))
            product_color_text = pq[0].PRODUCT_COLORS.values().filter(id=int(request.POST.get('selected_color_text')))[0]['color_title']
            product_color_quantity = pq[0].PRODUCT_COLORS.values().filter(id=int(request.POST.get('selected_color_text')))[0]['pquantity']
            product_image = pq[0].image.get_rendition('fill-250x280').url,
            if pq[0].PRODUCT_OFFER.values()[0]['value']:
                add_cart_date = pq[0].PRODUCT_OFFER.values()[0]['value']
            else:
                add_cart_date = pq[0].price
            try:
                product = InventoryItem.objects.get(pk=product_id)
                if product.is_available and product.is_active:
                    if(Cart.objects.filter(user=request.user.phoneNumber, product_title=product_title, color=product_color_text)):
                        return JsonResponse({'status':"کالا با رنگ بندی انتخاب شده هم اکنون در سبد خرید شما موجود است", 'success': False})
                    else:
                        quantity_requested = product_quantity
                        if quantity_requested <= product.quantity and quantity_requested <= product_color_quantity :
                            if add_cart_date > 0:
                                Cart.objects.create(
                                    user = request.user.phoneNumber,
                                    product_id = product_id,
                                    product_title = pq[0].title,
                                    product_collection = pq[0].collection.values()[0]['title'],
                                    quantity = product_quantity,
                                    price = add_cart_date,
                                    image = pq[0].image.get_rendition('fill-250x280').url,
                                    color = pq[0].PRODUCT_COLORS.values().filter(id=int(request.POST.get('selected_color_text')))[0]['color_title'],
                                    color_quantity = pq[0].PRODUCT_COLORS.values().filter(id=int(request.POST.get('selected_color_text')))[0]['pquantity'],
                                )
                                Cart.update_total(request.user.phoneNumber)
                                return JsonResponse({'status':f"محصول {product.product_title} با موفقیت به سبد خرید اضافه شد.", 'success': True})
                            else:
                                Cart.objects.create(
                                    user = request.user.phoneNumber,
                                    product_id = product_id,
                                    product_title = pq[0].title,
                                    product_collection = pq[0].collection.values()[0]['title'],
                                    quantity = product_quantity,
                                    price = product.price,
                                    image = pq[0].image.get_rendition('fill-250x280').url,
                                    color = pq[0].PRODUCT_COLORS.values().filter(id=int(request.POST.get('selected_color_text')))[0]['color_title'],
                                    color_quantity = pq[0].PRODUCT_COLORS.values().filter(id=int(request.POST.get('selected_color_text')))[0]['pquantity'],
                                )
                                Cart.update_total(request.user.phoneNumber)
                                return JsonResponse({'status':f"محصول {product.product_title} با موفقیت به سبد خرید اضافه شد.", 'success': True})
                        else:
                            return JsonResponse({'status':"تعداد سفارش درخواستی بیشتر از موجودی محصول است.", 'success': False})
                else:
                    return JsonResponse({'status':"موجودی محصول به پایان رسیده است", 'success': False})

            except InventoryItem.DoesNotExist:
                return JsonResponse({'status':"محصول مورد نظر پیدا نشد.", 'success': False})
        else:
            return JsonResponse({'status':"برای افزودن کالا به سبد خرید ابتدا باید ثبت نام کنید یا وارد حساب خود شوید", 'success': False})

    return render(request, 'products/cart/cart.html',{'discount': discount})

@login_required
@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        product_title = request.POST.get('product_title')
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            product = InventoryItem.objects.filter(product_title=product_title)
            try:
                user_cart = Cart.objects.get(user=request.user.phoneNumber, product_title=product_title)
                if user_cart.color_quantity >= quantity:
                    user_cart.quantity = quantity
                    user_cart.save()
                    Cart.update_total(request.user.phoneNumber)
                    return JsonResponse({'status': "تعداد درخواستی با موفقیت به روز شد", 'success': True})
                else:
                    return JsonResponse({'status': "تعداد درخواستی بالاتر از موجودی محصول است.", 'success': False})
            except Cart.DoesNotExist:
                return JsonResponse({'status': "محصول مورد پیدا نشد.", 'success': False})
        else:
            try:
                Cart.objects.filter(user=request.user.phoneNumber, product_title=product_title).delete()
                Cart.update_total(request.user.phoneNumber)
                return JsonResponse({'status':"محصول از سبد خرید حذف شد.", 'success': True})
            except Cart.DoesNotExist:
                return JsonResponse({'status': "محصول مورد پیدا نشد.", 'success': False})
    else:
        return render(request, 'products/cart/cart.html',{'discount': discount})

@login_required
@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        product_title = request.POST.get('product_title')
        if product_title:
            try:
                Cart.objects.filter(user=request.user.phoneNumber, product_title=product_title).delete()
                Cart.update_total(request.user.phoneNumber)
                return JsonResponse({'status':"محصول از سبد خرید حذف شد.", 'success': True})
            except:
                return JsonResponse({'status':"محصول از سبد خرید حذف شد.", 'success': True})
        else:
            return JsonResponse({'status':"محصول مورد پیدا نشد.", 'success': False})
    return render(request, 'products/cart/cart.html',{'discount': discount})

@login_required
@csrf_exempt
def apply_discount(request):
    if request.method == 'POST':
        product_title = request.POST.get('product_title')
        if product_title:
            price = int(request.POST.get('product_price'))
            category_id = int(request.POST.get('product_collection'))
            form = DiscountForm(request.POST)
            if form.is_valid():
                discount = Discount.objects.get(code=form.cleaned_data['code'])
                try:
                    if discount.product == product_id or discount.collection == category_id:
                        code = form.cleaned_data['code']
                        discounted_price = InventoryItem.apply_discount(discount_code=code, price=price)
                        Cart.objects.filter(user=request.user.phoneNumber, product_title=product_title).update(price=int(discounted_price))
                        return JsonResponse({'status':"کد تخفیف با موفقیت اعمال شد.", 'success': True})
                    else:
                        return JsonResponse({'status':"کد تخفیف معتبر نیست", 'success': False})
                except:
                    return JsonResponse({'status':"محصول مورد پیدا نشد.", 'success': False})
        else:
            return JsonResponse({'status':"محصول مورد پیدا نشد.", 'success': False})
    else:
        return render(request, 'products/cart/cart.html',{'discount': discount})

@login_required
def clear_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            Cart.objects.filter(user=request.user.phoneNumber).delete()
            Cart.update_total(request.user.phoneNumber)
            return JsonResponse({'status':"سبد خرید خالی شد.", 'success': True})
        else:
            return JsonResponse({'status':"سبد خرید هم اکنون خالی است.", 'success': False})
    else:
        return render(request, 'products/cart/cart.html',{'discount': discount})

@login_required
def checkout(request):
    if request.method == 'POST':
        if(Cart.objects.filter(user = request.user.phoneNumber)):
            return JsonResponse({'status':'200', 'success':True})
        else:
            return JsonResponse({'status':'محصولی برای خرید انتخاب نکرده اید', 'success':False})
    else:
        return JsonResponse({'status':'درخواست نامعتبر', 'success':False})

@login_required
def checkout_view(request):
    if Cart.objects.filter(user = request.user.phoneNumber):
        # fadax payment possible check:
        phone = request.user.phoneNumber
        '''list_cart = Cart.objects.filter(user=phone)
        for i in list_cart:
            total_price = i.total_price
        url = f"https://gateway.fadax.ir/supplier/v1/eligible?amount={total_price}&mobile=0{int(phone)}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {fadax_API}",
            "Content-Type": "application/json"
            }

        response_recived = requests.get(url, headers=headers)
        response = response_recived.json()
        '''
        Fadax_payment.objects.create(
            customer = request.user.phoneNumber,
        )
        UserModel.objects.filter(phoneNumber=phone).update(
            fadax_payment_possible = True
        )
        return render(request, 'products/checkout/checkout.html')
    else:
        return render(request, 'products/cart/cart.html')
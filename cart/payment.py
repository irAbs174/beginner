from root.local_settings import fadax_API, fadax_API_PATH, SMS_API_KEY
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from user_accounts.models import Customer
from django.http import JsonResponse
from django.shortcuts import render
from product.models import Orders
from .models import Fadax_payment
from .models import Cart
from kavenegar import *
import requests 
import random

@csrf_exempt
@login_required
def fadax_pay(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            customer = request.user.phoneNumber
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            email = request.POST.get('email')
            ostan = request.POST.get('State')
            city = request.POST.get('City')
            code_melli = request.POST.get('nationalcode')
            zip_zode = request.POST.get('postalcode')
            static_phone = request.POST.get('tel2')
            address = request.POST.get('address')
            pelak = request.POST.get('address2')
            send_method = request.POST.get('SEND_METHOD')
            payment_method = request.POST.get('PAYMENT_METHOD')
            cart = Cart.objects.filter(user = customer)
            if first_name:
                if last_name:
                    if ostan:
                        if city:
                            if code_melli:
                                if zip_zode:
                                    if address:
                                        if len(zip_zode) > 10 or len(zip_zode) < 10 :
                                            return JsonResponse({'status':'کد پستی وارد شده معتبر نیست','success':False})
                                        else:
                                            if len(code_melli) > 10 or len(code_melli) < 10 :
                                                return JsonResponse({'status':'کد ملی وارد شده معتبر نیست','success':False})
                                            else:
                                                if len(cart) > 0:
                                                    if send_method:
                                                        print(payment_method)
                                                        if payment_method == '2':
                                                            ######################################
                                                            response_post_request = request.POST.get('task')
                                                            print(response_post_request)
                                                            task = response_post_request
                                                            if task:
                                                                if Customer.objects.filter(customer = request.user.phoneNumber).exists():
                                                                    Customer.objects.filter(customer = request.user.phoneNumber).update(
                                                                        first_name = first_name,
                                                                        last_name = last_name,
                                                                        code_melli = code_melli,
                                                                        address = address,
                                                                        static_phone = static_phone,
                                                                        email = email,
                                                                        pelak = pelak,
                                                                        ostan = ostan,
                                                                        city = city,
                                                                        zip_zode = zip_zode,
                                                                    )
                                                                else:
                                                                    Customer.objects.create(
                                                                        customer = request.user.phoneNumber,
                                                                        first_name = first_name,
                                                                        last_name = last_name,
                                                                        code_melli = code_melli,
                                                                        address = address,
                                                                        static_phone = static_phone,
                                                                        email = email,
                                                                        pelak = pelak,
                                                                        ostan = ostan,
                                                                        city = city,
                                                                        zip_zode = zip_zode,
                                                                    )
                                                                send_price = 0
                                                                s_method = 2
                                                                shenase = random.randint(100000, 999999)
                                                                if (send_method == '1'):
                                                                    s_method = 0
                                                                    send_price = 0
                                                                elif (send_method == '2'):
                                                                    s_method = 1
                                                                    send_price = 50000
                                                                elif (send_method == '3'):
                                                                    s_method = 2
                                                                    send_price = 0
                                                                for item in cart:
                                                                    Orders.objects.create(
                                                                        shenase = shenase,
                                                                        customer = customer,
                                                                        product = item.product_title,
                                                                        number = item.quantity,
                                                                        color = item.color,
                                                                        price = item.price,
                                                                        status = 4,
                                                                        send_method = s_method,
                                                                        send_price = send_price,
                                                                    )

                                                                phone = request.user.phoneNumber
                                                                cart = Cart.objects.filter(user = phone)
                                                                for data in cart:
                                                                    amount = data.total_price
                                                                if task == 'recive_payment_token':
                                                                    cart_item = []
                                                                    phone = request.user.phoneNumber
                                                                    url = f"https://{fadax_API_PATH}/supplier/v1/payment-token"
                                                                    headers = {
                                                                        "accept": "application/json",
                                                                        "Authorization": f"Bearer {fadax_API}",
                                                                        "Content-Type": "application/json"
                                                                        }
                                                                    for item in cart:
                                                                        amount = item.total_price * 10
                                                                        item_list = {
                                                                            'title': item.product_title,
                                                                            'fee': item.price * 10,
                                                                            'count': item.quantity,
                                                                            'subtotal': (item.price * item.quantity) * 10,
                                                                        }
                                                                        cart_item.append(item_list)
                                                                        data = {
                                                                            "cartItems": cart_item,
                                                                            "mobile": phone,
                                                                            "cartTotal": amount,
                                                                            "discountAmount": Cart.objects.filter(user = phone)[0].offer_code_value,
                                                                            "shippingCost": send_price * 10,
                                                                            "taxAmount": round(amount * 0.1),
                                                                            "totalAmount": amount + (send_price * 10),
                                                                            "returnURL": "https://kikpick.com/cart/callback_fadax",
                                                                            "paymentMethodTypeDto": "INSTALLMENT"}


                                                                    print(data)
                                                                    response = requests.post(url, headers=headers, json=data)
                                                                    json = response.json()
                                                                    if json['success']:
                                                                        print(json)
                                                                        response = json['response']
                                                                        if response['status'] == 1001:
                                                                            print("1000000011111111")
                                                                            payment_Token = response['paymentToken']
                                                                            transactionId = response['transactionId']
                                                                            paymentPageURL = response['paymentPageURL']
                                                                            Fadax_payment.objects.filter(customer = phone).update(
                                                                                paymentToken = payment_Token,
                                                                            )
                                                                            return JsonResponse({
                                                                                'status': paymentPageURL,
                                                                                'success': True
                                                                            })
                                                                        elif response['status'] == 1002:
                                                                            print("1002 => 1002")
                                                                            return JsonResponse({'status': '13متاسفانه ارتباط با درگاه فدکس ناموفق بود. لطفا کمی بعد دوباره تلاش کنید', 'success': False})
                                                                        else:
                                                                            print("NOT 1002")
                                                                            return JsonResponse({'status': 'درخواست ارسال شده معتبر نیست12', 'success': False})
                                                                    else:
                                                                        print("not success !")
                                                                        print(json)
                                                                        return JsonResponse({'status': '11درخواست ارسال شده معتبر نیست', 'success': False})
                                                                elif task == 'send_verify_payment':
                                                                    paymentToken = request.POST.get('paymentToken')
                                                                    url = f"https://{fadax_API_PATH}/supplier/v1/verify’"
                                                                    headers = {
                                                                        "accept": "application/json",
                                                                        "Authorization": f"Bearer {fadax_API}",
                                                                    }
                                                                    data = {
                                                                        "paymentToken": paymentToken
                                                                    }
                                                                    response = requests.post(url, headers=headers, json=data)
                                                                    json = response.json()
                                                                    if json['success']:
                                                                        if json.response.status == 'ok':
                                                                            return JsonResponse({'status': 'سفارش با موفقیت تایید نهایی شد', 'success': True})
                                                                    else:
                                                                        return JsonResponse({'status': 'مشکلی در تایید نهایی سفارش به وجود آمده لطفا با پشتیبان سایت تماس حاصل بفرمایید', 'success': False})
                                                                elif task == 'get_payment_status':
                                                                    url = f"https://{fadax_API_PATH}/supplier/v1/status"
                                                                    headers = {
                                                                        "accept": "application/json",
                                                                        "Authorization": f"Bearer {fadax_API}",
                                                                        "Content-Type": "application/json"
                                                                        }
                                                                    for data in Fadax_payment.objects.filter(customer = request.user.phoneNumber):
                                                                        params = {
                                                                        "paymentToken": data.paymentToken,
                                                                        }
                                                                        response = requests.get(url, headers=headers, params=params)
                                                                        json = response.json()
                                                                        if json['success']:
                                                                            response = json['response'],
                                                                            if response.status == "completed":
                                                                                Fadax_payment.objects.filter(customer = request.user.phoneNumber).update(
                                                                                    status = 'completed',
                                                                                )
                                                                                return JsonResponse({'status': '10وضعیت سفارش شما تکمیل شده است و در حال انجام است', 'success': True})
                                                                        else:
                                                                            return JsonResponse({'status': '9درخواست ارسال شده معتبر نیست', 'success': False})
                                                                elif task == 'cancel_payment':
                                                                    url = f"https://{fadax_API_PATH}/supplier/v1/cancel"
                                                                    headers = {
                                                                        "accept": "application/json",
                                                                        "Authorization": f"Bearer {fadax_API}",
                                                                        "Content-Type": "application/json"
                                                                        }
                                                                    for item in Fadax_payment.objects.filter(customer = request.user.phoneNumber):
                                                                        data = {
                                                                            "paymentToken": payment_token
                                                                        }
                                                                    response = requests.post(url, headers=headers, json=data)
                                                                    json = response.json()
                                                                    if json['success']:
                                                                        response = json['response']
                                                                        if response['status'] == "canceled":
                                                                            return JsonResponse({'status': 'سفارش مورد نظر با موفقت لغو شد8', 'success': True})
                                                                        else:
                                                                            return JsonResponse({'status': '7مشکلی در لغو سفارش به وجود آمده. لطفا با پشتیبانی سایت تماس حاصل فرمایید', 'success': False})
                                                                    else:
                                                                        return JsonResponse({'status': 'درخواست ارسال شده معتبر نیست6', 'success': False})
                                                                elif task == 'revert_payment':
                                                                    url = f"https://{fadax_API_PATH}/supplier/v1/revert"
                                                                    headers = {
                                                                        "accept": "application/json",
                                                                        "Authorization": f"Bearer {fadax_API}",
                                                                        "Content-Type": "application/json"
                                                                        }
                                                                    for i in Cart.objects.filter(user = request.user.phoneNumber):
                                                                        amount = i.total_price
                                                                    for item in Fadax_payment.objects.filter(customer = request.user.phoneNumber):
                                                                        data = {
                                                                        "payment_token" : item.paymentToken,
                                                                        "lossAmount": amount,
                                                                        }
                                                                    response = requests.post(url, headers=headers, json=data)
                                                                    json = response.json()
                                                                    if json['success']:
                                                                        response = json.response
                                                                        if response['status'] == "reverted":
                                                                            return JsonResponse({'status': 'سفارش مورد نظر با موفقت مسترد شد شد', 'success': True})
                                                                        else:
                                                                            return JsonResponse({'status': '5مشکلی در لغو سفارش به وجود آمده. لطفا با پشتیبانی سایت تماس حاصل فرمایید', 'success': False})
                                                                    else:
                                                                        return JsonResponse({'status': '4درخواست ارسال شده معتبر نیست', 'success': False})
                                                            else:
                                                                return JsonResponse({'status': '3درخواست ارسال شده معتبر نیست', 'success': False})
                                                            ###################
                                                        else:
                                                            #payment method != fadax

                                                            if Customer.objects.filter(customer = request.user.phoneNumber).exists():
                                                                Customer.objects.filter(customer = request.user.phoneNumber).update(
                                                                    first_name = first_name,
                                                                    last_name = last_name,
                                                                    code_melli = code_melli,
                                                                    address = address,
                                                                    static_phone = static_phone,
                                                                    email = email,
                                                                    pelak = pelak,
                                                                    ostan = ostan,
                                                                    city = city,
                                                                    zip_zode = zip_zode,
                                                                )
                                                            else:
                                                                Customer.objects.create(
                                                                    customer = request.user.phoneNumber,
                                                                    first_name = first_name,
                                                                    last_name = last_name,
                                                                    code_melli = code_melli,
                                                                    address = address,
                                                                    static_phone = static_phone,
                                                                    email = email,
                                                                    pelak = pelak,
                                                                    ostan = ostan,
                                                                    city = city,
                                                                    zip_zode = zip_zode,
                                                                )
                                                            send_price = 0
                                                            s_method = 2
                                                            shenase = random.randint(100000, 999999)
                                                            if (send_method == '1'):
                                                                s_method = 0
                                                                send_price = 0
                                                            elif (send_method == '2'):
                                                                s_method = 1
                                                                send_price = 50000
                                                            elif (send_method == '3'):
                                                                s_method = 2
                                                                send_price = 0
                                                            for item in cart:
                                                                Orders.objects.create(
                                                                    shenase = shenase,
                                                                    customer = customer,
                                                                    product = item.product_title,
                                                                    number = item.quantity,
                                                                    color = item.color,
                                                                    price = item.price,
                                                                    status = 4,
                                                                    send_method = s_method,
                                                                    send_price = send_price,
                                                                )
                                                        #Cart.objects.filter(user = request.user.phoneNumber).delete()
                                                            return JsonResponse({'status':'https://kikpick.com/get_bank', 'success':True})
                                                    else:
                                                        return JsonResponse({'status':'لطفا نوع ارسال رو انتخاب کنید','success':False})
                                                else:
                                                    return JsonResponse({'status':'محصولی برای خرید انتخاب نشده','success':False})
                                    else:
                                        return JsonResponse({'status':'فیلد آدرس نمیتواند خالی باشد','success':False})
                                else:
                                    return JsonResponse({'status':'کد پستی را وارد کنید','success':False})
                            else:
                                return JsonResponse({'status':'کد ملی خود را وارد کنید','success':False})
                        else:
                            return JsonResponse({'status':'شهر محل سکونت را وارد نمایید','success':False})
                    else:
                        return JsonResponse({'status':'استان محل سکونت را وارد نمایید','success':False})
                else:
                    return JsonResponse({'status':'نام خانوادگی خود را وارد نمایید','success':False})
            else:
                return JsonResponse({'status':'نام خود را وارد نمایید','success':False})
        else:
            return JsonResponse({'status':'درخواست نامعتبر', 'success': False})
    else :
        return JsonResponse({'status':'برای ثبت سفارش ابتدا وارد سایت شوید', 'success': False})


@csrf_exempt
@login_required
def fadax_return_shop(request):
    if request.method == 'POST':
        success = request.POST.get('success')
        if success:
            paymentToken = paymentToken = Fadax_payment.objects.filter(customer = request.user.phoneNumber)[0].latest('paymentToken').paymentToken
            url = f"https://{fadax_API_PATH}/supplier/v1/verify’"
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {fadax_API}",
            }
            data = {
                "paymentToken": paymentToken
            }
            response = requests.post(url, headers=headers, json=data)
            json = response.json()
            if json['success']:
                if json.response.status == 'ok':
                    response = request.POST.get('response')
                    phone =  request.user.phoneNumber
                    if response.state == 'ok':
                        order = Orders.objects.filter(customer = phone)
                        for data in order:
                            order_code = order.shenase
                            customer = order.customer
                        refId = response['redId']
                        fadaxTrackingNumber = response['fadaxTrackingNumber']
                        transactionId = response['transactionId']
                        order_code = order.latest('date').shenase
                        Orders.objects.filter(customer = phone, shenase = order_code).update(status = 0)
                        Fadax_payment.objects.filter(customer = phone).update(
                            order_id = order_code,
                            refId = refId,
                            fadaxTrackingId = transactionId,
                            fadaxTrackingNumber = fadaxTrackingNumber,
                            status = 'success',
                        )
                        try:
                            api = KavenegarAPI(f'{SMS_API_KEY}')
                            params = {
                                'receptor': phone,
                                'template': 'kikpickPaymentSucces',
                                'token': order_code,
                                'type': 'sms',
                            }
                            response = api.verify_lookup(params)
                            print(response)
                        except APIException as e: 
                            print(e)
                        except HTTPException as e: 
                            print(e)
                        context = {
                            'status': 'success',
                            'message': 'با تشکر. پرداخت موفقیت آمیز بود. شناسه تراکنش : {transactionId} شماره رهگیری فدکس : {fadaxTrackingNumber}'
                        }
                        return render(request, 'payment/callback_fadax.html', context)
                    else:
                        transactionId = response['transactionId']
                        Fadax_payment.objects.create(
                            order_id = 'faild',
                            customer = request.user.phoneNumber,
                            refId = 'faild',
                            fadaxTrackingNumber = 'faild',
                            fadaxTrackingId = transactionId,
                            status = 'faild',
                        )
                        context = {
                            'status': 'failed',
                            'message': 'متاسفانه انجام تراکنش ناموفق بود. در صورت کسر از حساب پس از ۷۲ ساعت به حساب شما عودت می شود.',
                            'fadaxTrackingId': transactionId,
                        }
                        return render(request, 'payment/callback_fadax.html', context)
            else:
                transactionId = response['transactionId']
                Fadax_payment.objects.create(
                    order_id = 'faild',
                    refId = 'faild',
                    fadaxTrackingNumber = 'faild',
                    fadaxTrackingId = transactionId,
                    status = 'faild',
                )
                context = {
                    'status': 'failed',
                    'message': f'متاسفانه انجام تراکنش ناموفق بود. در صورت کسر از حساب پس از ۷۲ ساعت به حساب شما عودت می شود. شناسه تراکنش : {transactionId}',
                }
                return render(request, 'payment/callback_fadax.html', context)
        else:
            transactionId = response['transactionId']
            Fadax_payment.objects.create(
                order_id = 'faild',
                customer = request.user.phoneNumber,
                refId = 'faild',
                fadaxTrackingNumber = 'faild',
                fadaxTrackingId = transactionId,
                status = 'faild',
            )
            context = {
                'status': 'failed',
                'message': 'متاسفانه انجام تراکنش ناموفق بود. در صورت کسر از حساب پس از ۷۲ ساعت به حساب شما عودت می شود.',
                'fadaxTrackingId': transactionId,
            }
            return render(request, 'payment/callback_fadax.html', context)
    else:
        transactionId = response['transactionId']
        Fadax_payment.objects.create(
            order_id = 'faild',
            customer = request.user.phoneNumber,
            refId = 'faild',
            fadaxTrackingNumber = 'faild',
            fadaxTrackingId = transactionId,
            status = 'faild',
        )
        context = {
            'status': 'failed',
            'message': 'متاسفانه انجام تراکنش ناموفق بود. در صورت کسر از حساب پس از ۷۲ ساعت به حساب شما عودت می شود.',
            'fadaxTrackingId': transactionId,
        }
        return render(request, 'payment/callback_fadax.html', context)


@csrf_exempt
def test(request):
    if request.method == 'POST':
        response_post_request = request.POST.get('task')
        print(response_post_request)
        task = response_post_request
        if task:
            phone = request.user.phoneNumber
            cart = Cart.objects.filter(user = phone)
            for data in cart:
                amount = data.total_price
            if task == 'recive_payment_token':
                cart_item = []
                phone = request.user.phoneNumber
                url = f"https://{fadax_API_PATH}/supplier/v1/payment-token"
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {fadax_API}",
                    "Content-Type": "application/json"
                    }
                for item in cart:
                    amount = item.total_price * 10
                    item_list = {
                        'title': item.product_title,
                        'fee': item.price * 10,
                        'count': item.quantity,
                        'subtotal': (item.price * item.quantity) * 10,
                    }
                    cart_item.append(item_list)
                    data = {
                        "cartItems": cart_item,
                        "mobile": phone,
                        "cartTotal": amount,
                        "discountAmount": 0,
                        "shippingCost": 0,
                        "taxAmount": 0,
                        "totalAmount": amount,
                        "returnURL": "https://kikpick.com/cart/callback_fadax",
                        "paymentMethodTypeDto": "INSTALLMENT"}
                    
                    

                print(data)
                print('salam')
                response = requests.post(url, headers=headers, json=data)
                json = response.json()
                if json['success']:
                    print(json)
                    response = json['response']
                    if response['status'] == 1001:
                        print("1000000011111111")
                        payment_Token = response['paymentToken']
                        transactionId = response['transactionId']
                        paymentPageURL = response['paymentPageURL']
                        Fadax_payment.objects.filter(customer = phone).update(
                            paymentToken = payment_Token,
                        )
                        return JsonResponse({
                            'status': paymentPageURL,
                            'success': True
                        })
                    elif response['status'] == 1002:
                        print("1002 => 1002")
                        return JsonResponse({'status': '13متاسفانه ارتباط با درگاه فدکس ناموفق بود. لطفا کمی بعد دوباره تلاش کنید', 'success': False})
                    else:
                        print("NOT 1002")
                        return JsonResponse({'status': 'درخواست ارسال شده معتبر نیست12', 'success': False})
                else:
                    print("not success !")
                    print(json)
                    return JsonResponse({'status': '11درخواست ارسال شده معتبر نیست', 'success': False})
            elif task == 'send_verify_payment':
                paymentToken = request.POST.get('paymentToken')
                url = f"https://{fadax_API_PATH}/supplier/v1/verify’"
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {fadax_API}",
                }
                data = {
                    "paymentToken": paymentToken
                }
                response = requests.post(url, headers=headers, json=data)
                json = response.json()
                if json['success']:
                    if json.response.status == 'ok':
                        return JsonResponse({'status': 'سفارش با موفقیت تایید نهایی شد', 'success': True})
                else:
                    return JsonResponse({'status': 'مشکلی در تایید نهایی سفارش به وجود آمده لطفا با پشتیبان سایت تماس حاصل بفرمایید', 'success': False})
            elif task == 'get_payment_status':
                url = f"https://{fadax_API_PATH}/supplier/v1/status"
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {fadax_API}",
                    "Content-Type": "application/json"
                    }
                for data in Fadax_payment.objects.filter(customer = request.user.phoneNumber):
                    params = {
                    "paymentToken": data.paymentToken,
                    }
                    response = requests.get(url, headers=headers, params=params)
                    json = response.json()
                    if json['success']:
                        response = json['response'],
                        if response.status == "completed":
                            Fadax_payment.objects.filter(customer = request.user.phoneNumber).update(
                                status = 'completed',
                            )
                            return JsonResponse({'status': '10وضعیت سفارش شما تکمیل شده است و در حال انجام است', 'success': True})
                    else:
                        return JsonResponse({'status': '9درخواست ارسال شده معتبر نیست', 'success': False})
            elif task == 'cancel_payment':
                url = f"https://{fadax_API_PATH}/supplier/v1/cancel"
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {fadax_API}",
                    "Content-Type": "application/json"
                    }
                for item in Fadax_payment.objects.filter(customer = request.user.phoneNumber):
                    data = {
                        "paymentToken": payment_token
                    }
                response = requests.post(url, headers=headers, json=data)
                json = response.json()
                if json['success']:
                    response = json['response']
                    if response['status'] == "canceled":
                        return JsonResponse({'status': 'سفارش مورد نظر با موفقت لغو شد8', 'success': True})
                    else:
                        return JsonResponse({'status': '7مشکلی در لغو سفارش به وجود آمده. لطفا با پشتیبانی سایت تماس حاصل فرمایید', 'success': False})
                else:
                    return JsonResponse({'status': 'درخواست ارسال شده معتبر نیست6', 'success': False})
            elif task == 'revert_payment':
                url = f"https://{fadax_API_PATH}/supplier/v1/revert"
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {fadax_API}",
                    "Content-Type": "application/json"
                    }
                for i in Cart.objects.filter(user = request.user.phoneNumber):
                    amount = i.total_price
                for item in Fadax_payment.objects.filter(customer = request.user.phoneNumber):
                    data = {
                    "payment_token" : item.paymentToken,
                    "lossAmount": amount,
                    }
                response = requests.post(url, headers=headers, json=data)
                json = response.json()
                if json['success']:
                    response = json.response
                    if response['status'] == "reverted":
                        return JsonResponse({'status': 'سفارش مورد نظر با موفقت مسترد شد شد', 'success': True})
                    else:
                        return JsonResponse({'status': '5مشکلی در لغو سفارش به وجود آمده. لطفا با پشتیبانی سایت تماس حاصل فرمایید', 'success': False})
                else:
                    return JsonResponse({'status': '4درخواست ارسال شده معتبر نیست', 'success': False})
            else:
                return JsonResponse({'status': '3درخواست ارسال شده معتبر نیست', 'success': False})
        else:
            return JsonResponse({'status': '2درخواست ارسال شده معتبر نیست', 'success': False})
    else:
        return JsonResponse({'status': '1درخواست ارسال شده معتبر نیست', 'success': False})
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from category.models import CategoryProduct as cat
from brand.models import BrandPage as brand
from brand.models import BrandPage
from category.models import CategoryProduct
from django.http import JsonResponse
from .models import InventoryItem
import random


@csrf_exempt
def load_brand_items(request):
    context = []
    list = [
        'الکسا',
        'نیلپر',
        'فوروارد',
        'فیلا',
        'کت',
        'گپ',
    ]
    bp = BrandPage.objects.live().public().order_by('first_published_at')
    for i in list:
        bps = bp.search(i)[0]
        item = {
            'id': bps.id,
            'title': bps.title,
            'image': bps.image.get_rendition('fill-75x75').url,
        }
        context.append(item)

    return JsonResponse({'status': context, 'success': True})

@csrf_exempt
def load_category_items(request):
    cat_list = []
    for c in CategoryProduct.objects.live().public().order_by('first_published_at'):
        if c.image:
            item = {
                'id': c.id,
                'title': c.title,
                'image': c.image.get_rendition('fill-100x100').url,
                'count': 0,
            }
            count = InventoryItem.objects.filter(collection=c.id).count()
            if count:
                item['count'] = count
                cat_list.append(item)
            context = sorted(cat_list, key=lambda x: x['count'], reverse=True)
    return JsonResponse({'status': context[0:8], 'success': True})

@csrf_exempt
def load_special_products(request):
    context = []
    list = [
        '8020',
        '6006',
        '6008',
        '8017',
        '8002',
        '6633',
        '437',
        '6501',
        '7709',
    ]
    for i in list:
        item = {
            'title': InventoryItem.objects.all().public().live().search(i)[0].title,
            'slug': InventoryItem.objects.all().public().live().search(i)[0].slug,
            'price': InventoryItem.objects.all().public().live().search(i)[0].price,
            'offer': InventoryItem.objects.all().public().live().search(i)[0].PRODUCT_OFFER.values()[0]['value'] if InventoryItem.objects.all().public().live().search(i)[0].PRODUCT_OFFER.values() else 0,
            'quantity': InventoryItem.objects.all().public().live().search(i)[0].quantity,
            'brand': InventoryItem.objects.all().public().live().search(i)[0].brand.title,
            'image': InventoryItem.objects.all().public().live().search(i)[0].image.get_rendition('fill-250x280').url,
        }
        context.append(item)
    return JsonResponse({'status' : context, 'success': True})

@csrf_exempt
def get_random_products(request):
    random_number = int(request.POST.get('random_number'))
    context = []
    for i in range(random_number):
        random_int = random.randint(1, len(InventoryItem.objects.all().live()) -1)
        if InventoryItem.objects.all().live()[random_int].PRODUCT_OFFER.values():
            item = {
                'id': InventoryItem.objects.all().live()[random_int].id,
                'slug': InventoryItem.objects.all().live()[random_int].slug,
                'title': InventoryItem.objects.all().live()[random_int].title,
                'product_title': InventoryItem.objects.all().live()[random_int].product_title,
                'price': InventoryItem.objects.all().live()[random_int].price,
                'offer': InventoryItem.objects.all().live()[random_int].PRODUCT_OFFER.values()[0]['value'],
                'quantity': InventoryItem.objects.all().live()[random_int].quantity,
                'brand': InventoryItem.objects.all().live()[random_int].brand.title,
                'image': InventoryItem.objects.all().live()[random_int].image.get_rendition('fill-250x280').url,
                'is_available': InventoryItem.objects.all().live()[random_int].is_available,
                }
            context.append(item)
    return JsonResponse({'status': context, 'success': True})

@csrf_exempt
def shop_data(request):
    page_number = request.POST.get('page_number')
    load_filter = request.POST.get('load_filter')
    if load_filter == 'offer_products_list':
        context = []
        if page_number == 'indexOff':
            page_number = 1 
            per_page = 10
            next_pagintage = 'index_products'
        else:
            per_page = 16
            next_pagintage = int(page_number) + 1
        products = InventoryItem.objects.live().public().order_by('first_published_at')
        paginator = Paginator(products, per_page)
        try:
            products_list = paginator.get_page(page_number)
        except PageNotAnInteger:
            products_list = paginator.get_page(1)
        except EmptyPage:
            products_list = paginator.page(paginator.num_pages)
        if products_list.has_next() == False:
            context = 'end'
        else:
            for data in products_list:
                offer = data.PRODUCT_OFFER.values()
                if offer:
                    item = {
                    'id': data.id,
                    'slug': data.slug,
                    'title': data.title,
                    'product_title': data.product_title,
                    'price': data.price,
                    'offer': 0,
                    'quantity': data.quantity,
                    'brand': data.brand.title,
                    'color': [],
                    'image': data.image.get_rendition('fill-250x280').url,
                    'is_available': data.is_available,
                    }
                item['offer'] = offer[0]['value']
                colors = data.PRODUCT_COLORS.values()
                for color in colors:
                    color_data = {
                        'name': color['color_title'],
                        'code': color['color']
                    }
                    item['color'].append(color_data)
                context.append(item)
        return JsonResponse({
            'status': 200,
            'context': context,
            'next_pagintage': next_pagintage,
            'pagintage_key' : 'offer_products_list',
            'success': True
            })
    elif load_filter == 'brand_count_list':
        brand_list = []
        for b in brand.objects.live().public().order_by('first_published_at'):
            item = {
                'id': b.id,
                'title': b.title,
                'count': 0,
                }
            count = InventoryItem.objects.filter(brand=b.id).count()
            if count:
                item['count'] = count
                brand_list.append(item)
        context = sorted(brand_list, key=lambda x: x['count'], reverse=True)
        return JsonResponse({
            'status': 200,
            'context': context,
            'success': True,
            })
    elif load_filter == 'category_count_list':
        cat_list = []
        for c in cat.objects.live().public().order_by('first_published_at'):
            item = {
                'id': c.id,
                'title': c.title,
                'count': 0,
                }
            count = InventoryItem.objects.filter(collection=c.id).count()
            if count:
                item['count'] = count
                cat_list.append(item)
        context = sorted(cat_list, key=lambda x: x['count'], reverse=True)
        return JsonResponse({
            'status': 200,
            'context': context,
            'success': True,
            })
    elif load_filter == 'price_filter':
        min = request.POST.get('minPrice')
        max = request.POST.get('maxPrice')
        if isinstance(int(min), int) and isinstance(int(max), int):
            if max and min:
                products = InventoryItem.objects.all().model.objects.filter(price__gte=int(min), price__lte=int(max))
                if products.count() < 0 :
                    return JsonResponse({'status':'محصولی در بازه وارد شده یافت نشد', 'success': False})
                pagintage_key = 'price_filter'
            else:
                return JsonResponse({'status':'مقداری برای اعمال فیلتر وارد نشده', 'success': False})
        else:
            return JsonResponse({'status':'مقادیر وارد شده معتبر نیست. لطفا یک مقدار عددی وارد کنید','success': False})
    elif load_filter == 'old_filter':
        products = InventoryItem.objects.live().public().order_by('first_published_at')
        pagintage_key = 'old_filter'
    elif load_filter == 'expensive_filter':
        products = InventoryItem.objects.live().public().order_by('-price')
        pagintage_key = 'expensive_filter'
    elif load_filter == 'cheapest_filter':
        products = InventoryItem.objects.live().public().order_by('price')
        pagintage_key = 'cheapest_filter'
    else:
        products = InventoryItem.objects.live().public().order_by('-first_published_at')
        pagintage_key = ''
    if page_number == 'index':
        per_page = 16
        next_pagintage = 'index_products'
    else:
        per_page = 8
        next_pagintage = int(page_number) + 1
    paginator = Paginator(products, per_page)
    try:
        products_list = paginator.get_page(page_number)
    except PageNotAnInteger:
        products_list = paginator.get_page(1)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)
    if products_list.has_next() == False:
        context = 'end'
    else:
        context = []
        for data in products_list:
            item = {
                'id': data.id,
                'slug': data.slug,
                'title': data.title,
                'product_title': data.product_title,
                'price': data.price,
                'offer': 0,
                'quantity': data.quantity,
                'brand': data.brand.title,
                'color': [],
                'image': data.image.get_rendition('fill-250x280').url,
                'is_available': data.is_available,
            }
            offer = data.PRODUCT_OFFER.values()
            if offer:
                item['offer'] = offer[0]['value']
            
            colors = data.PRODUCT_COLORS.values()
            for color in colors:
                color_data = {
                    'name': color['color_title'],
                    'code': color['color']
                }
                item['color'].append(color_data)
            context.append(item)
    return JsonResponse({
        'status': 200,
        'context': context,
        'next_pagintage': next_pagintage,
        'pagintage_key' : pagintage_key,
        'success': True
    })
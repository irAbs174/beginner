from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from category.models import CategoryProduct as cat
from brand.models import BrandPage as brand
from django.http import JsonResponse
from .models import InventoryItem

@csrf_exempt
def shop_data(request):
    page_number = request.POST.get('page_number')
    load_filter = request.POST.get('load_filter')
    match load_filter:
        case 'brand_count_list':
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
        case 'category_count_list':
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
        case 'price_filter':
            min = request.POST.get('minPrice')
            max = request.POST.get('maxPrice')
            if isinstance(int(min), int) and isinstance(int(max), int):
                products = InventoryItem.objects.all().model.objects.filter(price__gte=int(min), price__lte=int(max))
            else:
                return JsonResponse({'status':'مقادیر وارد شده معتبر نیست. لطفا یک مقدار عددی وارد کنید','success': False})
        case 'old_filter':
            products = InventoryItem.objects.live().public().order_by('first_published_at')
        case 'expensive_filter':
            products = InventoryItem.objects.live().public().order_by('-price')
        case 'cheapest_filter':
            products = InventoryItem.objects.live().public().order_by('price')
        case _:
            products = InventoryItem.objects.live().public().order_by('-first_published_at')
    paginator = Paginator(products, 12)
    try:
        products_list = paginator.get_page(page_number)
    except PageNotAnInteger:
        products_list = paginator.get_page(1)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)
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
    next_pagintage = int(page_number) + 1
    return JsonResponse({
        'status': 200,
        'context': context,
        'next_pagintage': next_pagintage,
        'success': True
    })
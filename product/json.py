from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import InventoryItem

@csrf_exempt
def shop_data(request):
    page_number = request.POST.get('page_number')
    products = InventoryItem.objects.all()
    paginator = Paginator(products, 8)
    try:
        products_list = paginator.page(page_number)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)
    context = []
    for data in products:
        item = {
            'id': data.id,
            'title': data.title,
            'product_title': data.product_title,
            'price': data.price,
            'offer': 0,
            'quantity': data.quantity,
            'brand': data.brand.title,
            'color': [],
            'is_available': data.is_available,
            'image': data.image.file.url,
            'page_number': 2
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
        'status': '200',
        'context': context,
        'success': True
    })
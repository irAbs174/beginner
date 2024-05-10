from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import BlogPage as bp


@csrf_exempt
def blog_archive_data(requests):
    context = []
    for i in bp.objects.all():
        item = {
            'title': i.title,
            'slug': i.slug,
            'keywords': i.keywords,
            'description': i.description,
            'intro': i.intro,
            'image': i.image.get_rendition('max-550x400').url,
            'collection':i.collection.title,
            'date':i.jpub(),
        }
        context.append(item)
    return JsonResponse({'status':200, 'context': context , 'success': True})
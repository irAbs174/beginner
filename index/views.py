"""
2020 Black
developer : #ABS
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Custom_pages, Comments
from django.http import JsonResponse


@csrf_exempt
def submit_comment(request):
    post = request.POST.get('post')
    name = request.POST.get('name')
    body = request.POST.get('body')
    rate = request.POST.get('rate')
    if request.user.is_authenticated:
        if post:
            if name:
                if body:
                    if rate:
                        if Comments.objects.all().filter(user=request.user.phoneNumber, post=post).exists():
                            return JsonResponse({'status': 'کاربر گرامی شما برای این کالا قبلا دیدگاه ثبت نموده اید', 'success': False})
                        else:
                            Comments.objects.create(
                                title = rate,
                                user = request.user.phoneNumber,
                                name = name,
                                post = post,
                                body = body,
                            )
                            return JsonResponse({'status': 'با تشکر از شما برای ثبت دیدگاه خود', 'success': True})
                    else:
                        return JsonResponse({'status': 'لطفا نظر خود را وارد نمایید', 'success': False})
                else:
                    return JsonResponse({'status': 'لطفا نظر خود را بنویسید', 'success': False})
            else:
                return JsonResponse({'status': 'لطفا نام خود را وارد نمایید', 'success': False})
        else:
            return JsonResponse({'status': 'درخواست نامعتبر', 'success': False})
    else:
        return JsonResponse({'status': 'برای ثبت دیدگاه ابتدا وارد سایت شوید', 'success': False})

# for site custom pages
def custom_pages_view(request, Page):
    if Custom_pages.objects.filter(slug=Page).exists():
        detail = get_object_or_404(Custom_pages, slug=Page)
        content = {
            'page' : detail,
        }
        return render(request, 'custom_page/page.html', content)
    else:
        return render(request, 'utils/Error/404.html', status=404)

# for All visits
def visit_view(request):
    return render(request, 'utils/visit/visit.html')

# for mounth visits
def mounth_visit_view(request):
    return render(request, 'utils/visit/mounth_visit.html')

# for week visits
def week_visit_view(request):
    return render(request, 'utils/visit/week_visit.html')

# for daily visits
def daily_visit_view(request):
    return render(request, 'utils/visit/daily_visit.html')

# 404 Error view (Page not found)
def page_not_found_error(request, exception):
    return render(request, 'utils/Error/404.html', status=404)
    
    
# 500 Error view (Server Error)
def server_error(request):
    return render(request, 'utils/Error/500.html', status=404)
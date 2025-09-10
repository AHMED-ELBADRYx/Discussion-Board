from django.shortcuts import redirect
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_queryset(request, queryset, per_page=20):
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    
    return result

def increment_view_count(request, model, obj_id, session_key_prefix):
    session_key = f'{session_key_prefix}_{obj_id}'
    if not request.session.get(session_key, False):
        model.objects.filter(pk=obj_id).update(views=F('views') + 1)
        request.session[session_key] = True
    return True
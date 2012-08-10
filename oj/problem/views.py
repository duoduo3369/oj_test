from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import Http404
from oj.models.problem import ProblemMetaType, ItemMetaType
from oj.sa_conn import Session
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def problem_index(request):
    return render_to_response("problem/problem_index.html", context_instance=RequestContext(request))
    
from django.http import settings
from forms import ProblemMetaTypeForm

def problem_meta_type_list(request, page=1):
    session = Session()
    meta_types_all = session.query(ProblemMetaType).all()
    session.close()
    
    paginator = Paginator(meta_types_all, settings.METAS_PER_PAGE)
    
    try:
        meta_types = paginator.page(meta_types_all)
    except (EmptyPage, InvalidPage):
        meta_types = paginator.page(paginator.num_pages)
    return render_to_response('problem/problem_meta_type_list.html', {"meta_types": meta_types},
                              context_instance=RequestContext(request))
    
def problem_meta_type_detail(request, problem_meta_type_id):
    session = Session()
    meta_type = session.query(ProblemMetaType).get(problem_meta_type_id)
    
    if meta_type is None:
        raise Http404
    data = {"meta_type": meta_type,}
    session.close()
    
    return render_to_response('problem/problem_meta_type_detail.html', data,
                             context_instance=RequestContext(request))

def problem_meta_type_add(request):
    if request.method == 'POST':
        form = ProblemMetaTypeForm(request.POST)
        if form.is_valid():
            problem_meta_type = form.save()
            data = {'problem_meta_type_id': problem_meta_type.id}
            return HttpResponseRedirect(reverse('problem_meta_type_detail', kwargs=data))
    else:
        form = ProblemMetaTypeForm()
        
    data = {'form': form}
    return render_to_response("problem/problem_meta_type_add.html", data, context_instance=RequestContext(request)) 


from forms import ItemMetaTypeForm

def item_meta_type_add(request):
    if request.method == 'POST':
        form = ItemMetaTypeForm(request.POST)
        if form.is_valid():
            item_meta_type = form.save()
            data = {'item_meta_type_id': item_meta_type.id}
            return HttpResponseRedirect(reverse('item_meta_type_detail', kwargs=data))
    else:
        form = ItemMetaTypeForm()
        
    data = {'form': form}
    return render_to_response("problem/item_meta_type_add.html", data, context_instance=RequestContext(request)) 

def item_meta_type_list(request, page=1):
    session = Session()
    meta_types_all = session.query(ItemMetaType).all()
    session.close()
    
    paginator = Paginator(meta_types_all, settings.METAS_PER_PAGE)
    
    try:
        meta_types = paginator.page(meta_types_all)
    except (EmptyPage, InvalidPage):
        meta_types = paginator.page(paginator.num_pages)
        data = {"meta_types": meta_types}
    return render_to_response('problem/item_meta_type_list.html', data,
                              context_instance=RequestContext(request))
    
def item_meta_type_detail(request, item_meta_type_id):
    session = Session()
    meta_type = session.query(ItemMetaType).get(item_meta_type_id)
    
    if meta_type is None:
        raise Http404
    data = {"meta_type": meta_type,}
    session.close()
    
    return render_to_response('problem/item_meta_type_detail.html', data,
                             context_instance=RequestContext(request))
  
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import Http404
from oj.models.problem import ProblemMetaType, ItemMetaType,ItemMeta
from oj.sa_conn import Session
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from forms import ProblemMetaTypeForm,ProblemMetaForm,ItemMetaForm,ItemMetaTypeForm
from oj.constant import MARK_SEPARATOR

def problem_index(request):
    return render_to_response("problem/problem_index.html", context_instance=RequestContext(request))
    
from django.http import settings

def show_list(request,template,ItemClass, page=1):
    session = Session()
    objects_all = session.query(ItemClass).all()
    session.close()
    
    paginator = Paginator(objects_all, settings.METAS_PER_PAGE)
    
    try:
        objects = paginator.page(objects_all)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
    data = {"objects": objects}
    return render_to_response(template, data,
                              context_instance=RequestContext(request))

def problem_meta_type_detail(request, problem_meta_type_id):
    session = Session()
    meta_type = session.query(ProblemMetaType).get(problem_meta_type_id)
    
    if meta_type is None:
        raise Http404
    data = {"meta_type": meta_type,}
    item_meta_types = meta_type.get_item_meta_types()    
    data.update({'item_meta_types':item_meta_types})
    
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

    
def item_meta_type_detail(request, item_meta_type_id):
    session = Session()
    meta_type = session.query(ItemMetaType).get(item_meta_type_id)
    metas = session.query(ItemMeta).filter(ItemMeta.item_meta_type_id == item_meta_type_id)
    
    if meta_type is None:
        raise Http404
    data = {"meta_type": meta_type,
            "item_meta_type_id":item_meta_type_id,
            "metas":metas,
            }
    session.close()
    
    return render_to_response('problem/item_meta_type_detail.html', data,
                             context_instance=RequestContext(request))

from oj.models.problem import ProblemMetaMultipleChoiceFormItem

def problem_meta_add(request,problem_meta_type_id):
    session = Session()
    problem_meta_type = session.query(ProblemMetaType).get(problem_meta_type_id)
    if problem_meta_type is None:
        raise Http404
        
    item_meta_types = problem_meta_type.item_meta_types
        
    item_meta_types = item_meta_types.split(MARK_SEPARATOR)
    imts = []
    for imt in xrange(1,len(item_meta_types)):
        imts.append(int(imt))
    #item_meta_type_number = len(imts)
    data_list = []
    #[ 0:type_id  1:field_name, 2:item_meta_type_object 3:item_meta_object
    # (2,             ),
    #]
    for imt in imts:
        item_meta_type_object = session.query(ItemMetaType).get(imt)
        if item_meta_type_object is None:
            raise Http404
        item_meta_object = session.query(ItemMeta).filter(ItemMeta.item_meta_type_id == imt)
        if item_meta_object is None:
            raise Http404
 
        field_name = item_meta_type_object.title
        data = ProblemMetaMultipleChoiceFormItem(imt,field_name,item_meta_type_object,item_meta_object)
        data_list.append(data)
            
    if request.method == 'POST':
#        request_copy = request.POST.copy()
#        request_copy.update({"problem_meta_type_id":problem_meta_type_id})
#        form = ProblemMetaForm(request_copy)
        form = ProblemMetaForm(request.POST,initial={"problem_meta_type_id":problem_meta_type_id,
                                        "data_list":data_list,
                                        
                                        })
        
        if form.is_valid():
            problem_meta = form.save(problem_meta_type_id = problem_meta_type_id,data_list=data_list)
            #data = {'problem_meta_id': problem_meta.id}
            data = {"problem_meta_type_id":problem_meta_type_id}
            return HttpResponseRedirect(reverse('problem_meta_type_detail', kwargs=data))
    else:
        form = ProblemMetaForm(initial={"problem_meta_type_id":problem_meta_type_id,
                                        "data_list":data_list,
                                        
                                        })
    
    data = {'form': form,'data_list':data_list,}
    session.close()
    return render_to_response("problem/problem_meta_add.html", data, context_instance=RequestContext(request)) 



def item_meta_add(request,item_meta_type_id):
    
    if request.method == 'POST':
        form = ItemMetaForm(request.POST)
        
        if form.is_valid():
            item_meta = form.save(item_meta_type_id = item_meta_type_id)
            data = {'item_meta_type_id':item_meta_type_id,}
            return HttpResponseRedirect(reverse('item_meta_type_detail', kwargs=data))
    else:
        form = ItemMetaForm()
    
    session = Session()
    meta_type = session.query(ItemMetaType).get(item_meta_type_id)
    
    if meta_type is None:
        raise Http404    
    data = {'form': form,'meta_type':meta_type}
    session.close()
    return render_to_response("problem/item_meta_add.html", data, context_instance=RequestContext(request)) 

def item_meta_detail(request, item_meta_id):
    session = Session()
    meta = session.query(ItemMeta).get(item_meta_id)
    
    if meta is None:
        raise Http404
    data = {"meta": meta,"item_meta_id":item_meta_id}
    session.close()
    
    return render_to_response('problem/item_meta_detail.html', data,
                             context_instance=RequestContext(request))
  
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import Http404
from oj.models.problem import ProblemMetaType, ProblemMeta, Problem, ItemMetaType, ItemMeta, \
    Item
from oj.sa_conn import Session
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def problem_index(request):
    return render_to_response("problem/problem_index.html", context_instance=RequestContext(request))
    
from django.http import settings
def meta_list(request, page=1):
    session = Session()
    metas_all = session.query(ProblemMeta).all()
    session.close()
    
    paginator = Paginator(metas_all, settings.METAS_PER_PAGE)
    
    try:
         metas = paginator.page(metas_all)
    except (EmptyPage, InvalidPage):
        metas = paginator.page(paginator.num_pages)
    return render_to_response('problem/meta_list.html', {"metas": metas},
                              context_instance=RequestContext(request))


from forms import ProblemMetaTypeForm

def problem_meta_type_add(request):
    if request.method == 'POST':
        form = ProblemMetaTypeForm(request.POST)
        if form.is_valid():
            problem_meta_type = form.save()
            return HttpResponseRedirect(reverse('meta_detail', kwargs={'problem_meta_type_id': problem_meta_type.id}))
    else:
        form = ProblemMetaTypeForm()
        
    data = {'form': form}
    return render_to_response("problem/problem_meta_type_add.html", data, context_instance=RequestContext(request)) 

    
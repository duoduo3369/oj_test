from oj.problem.views import *
from django.conf.urls.defaults import patterns, url
from oj.models.problem import ProblemMetaType,ItemMetaType

urlpatterns = patterns('',
    url(r'^problem_meta_type_list/(?P<page>\d{,10})/$',
                     show_list,
                    {'template':'problem/problem_meta_type_list.html',
                     'ItemClass':ProblemMetaType},
                     name="problem_meta_type_list"),
    url(r'^problem_meta_type_detail/(?P<problem_meta_type_id>\d{,10})/$',
                     problem_meta_type_detail,
                     name="problem_meta_type_detail"),
    url(r'^problem_meta_type_add/$',
                     problem_meta_type_add,
                     name='problem_meta_type_add'),
    url(r'^item_meta_type_list/(?P<page>\d{,10})/$',
                     show_list,
                     {'template':'problem/item_meta_type_list.html',
                      'ItemClass':ItemMetaType}, 
                      name="item_meta_type_list"),
    url(r'^item_meta_type_detail/(?P<item_meta_type_id>\d{,10})/$', 
                    item_meta_type_detail, 
                    name="item_meta_type_detail"),
    url(r'^item_meta_type_add/$', 
                    item_meta_type_add, 
                    name='item_meta_type_add'),

)

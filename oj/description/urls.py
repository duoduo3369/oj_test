from django.conf.urls.defaults import patterns, url
from oj.description.models import (Item,ItemRelation,
                                         DescriptionMeta)
from oj.description.views import (show_list,item_add,item_relation_add,
                                        item_relation_combine_add,item_relation_detail,
                                        description_meta_add,description_meta_detail,
                                        description_meta_item_relation_combine_add,
                                        description_type_add,description_type_list,
                                        description_type_item_relation_combine_add,
                                        description_type_detail,description_detail_add,
                                        description_add,description_show,
                                        description_list
                                        )

urlpatterns = patterns('',
    url(r'^item_list/(?P<page>\d{,10})/$',
                     show_list,
                    {'template':'description/item_list.html',
                     'ItemClass':Item},
                     name="item_list"),
    url(r'^item_add/$', item_add,name="item_add"),
    
    url(r'^item_relation_list/(?P<page>\d{,10})/$',
                     show_list,
                    {'template':'description/item_relation_list.html',
                     'ItemClass':ItemRelation},
                     name="item_relation_list"),
    url(r'^item_relation_add/$', item_relation_add,name="item_relation_add"),
    url(r'^item_relation_combine_add/(?P<item_relation_id>\d{,10})/$', item_relation_combine_add,name="item_relation_combine_add"),
    url(r'^item_relation_detail/(?P<item_relation_id>\d{,10})/$', item_relation_detail,name="item_relation_detail"),

    url(r'^description_meta_list/(?P<page>\d{,10})/$',
                     show_list,
                    {'template':'description/description_meta_list.html',
                     'ItemClass':DescriptionMeta},
                     name="description_meta_list"),
    url(r'^description_meta_add/$', description_meta_add,name="description_meta_add"),
    url(r'^description_meta_item_relation_combine_add/(?P<description_meta_id>\d{,10})/$', 
        description_meta_item_relation_combine_add,name="description_meta_item_relation_combine_add"),
    url(r'^description_meta_detail/(?P<description_meta_id>\d{,10})/$', description_meta_detail,name="description_meta_detail"),

    url(r'^description_type_add/(?P<description_meta_id>\d{,10})/$', description_type_add,name="description_type_add"),
    url(r'^description_type_item_relation_combine_add/(?P<description_type_id>\d{,10})/$', 
        description_type_item_relation_combine_add,name="description_type_item_relation_combine_add"),
    url(r'^description_type_list/(?P<description_meta_id>\d{,10})/(?P<page>\d{,10})/$', description_type_list,name="description_type_list"),
    url(r'^description_type_detail/(?P<description_type_id>\d{,10})/$', description_type_detail,name="description_type_detail"),

    url(r'^description_detail_add/(?P<description_type_id>\d{,10})/(?P<description_id>\d{,10})/$', description_detail_add,name="description_detail_add"),
    url(r'^description_add/$', description_add,name="description_add"),
    url(r'^description_show/(?P<description_id>\d{,10})/$', description_show,name="description_show"),
    url(r'^description_list/(?P<description_type_id>\d{,10})/(?P<page>\d{,10})/$',description_list,name="description_list"),
)
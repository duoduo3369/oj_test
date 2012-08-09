from oj.problem.views import problem_meta_type_add
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('', 
    url(r'^problem_meta_type_add/$', problem_meta_type_add, name='problem_meta_type_add'),  

)

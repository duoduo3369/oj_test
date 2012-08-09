from oj.problem.views import *
from django.conf.urls.defaults import patterns, url
from oj.problem.forms import *

urlpatterns = patterns('', 
    url(r'^problem_meta_type_add/$', problem_meta_type_add, name='problem_meta_type_add'),  

)

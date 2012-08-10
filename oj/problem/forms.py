from django import forms
#from oj.models.problem import ProblemMetaType, ProblemMeta, Problem, ItemMetaType, ItemMeta, \
#    Item
from oj.sa_conn import Session
#from oj.models.problem import ProblemMetaType
from oj.tables.problem import ProblemMetaType
from django.utils.translation import ugettext, ugettext_lazy as _


class ProblemMetaTypeForm(forms.Form):
    title = forms.CharField(label=_('title'), max_length = 254)

    def __init__(self, *args, **kwargs):
        super(ProblemMetaTypeForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = ProblemMetaType

    def save(self, commit=True, update=False, problem_meta_type_id=0):
        session = Session()
        
        if update:
            problem_meta_type = session.query(ProblemMetaType).get(problem_meta_type_id)
        else:
            problem_meta_type = ProblemMetaType()

        problem_meta_type.title = self.cleaned_data['title']

        
        if not update:
            session.add(problem_meta_type)
        session.commit()
        session.close()
        
        return problem_meta_type





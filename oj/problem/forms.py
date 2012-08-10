from django import forms
#from oj.models.problem import ProblemMetaType, ProblemMeta, Problem, ItemMetaType, ItemMeta, \
#    Item
from oj.sa_conn import Session
#from oj.models.problem import ProblemMetaType
from oj.tables.problem import ProblemMetaType,ItemMetaType,ItemMeta
from django.utils.translation import ugettext, ugettext_lazy as _


class ItemMetaTypeForm(forms.Form):
    title = forms.CharField(label=_('title'), max_length = 254)

    def __init__(self, *args, **kwargs):
        super(ItemMetaTypeForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = ItemMetaType

    def save(self, commit=True, update=False, item_meta_type_id=None):
        session = Session()
        
        if update:
            item_meta_type = session.query(ItemMetaType).get(item_meta_type_id)
        else:
            item_meta_type = ItemMetaType()

        item_meta_type.title = self.cleaned_data['title']

        
        if not update:
            session.add(item_meta_type)
        session.commit()        
        item_meta_type.id = item_meta_type.id
        session.close()
        
        return item_meta_type

class ItemMetaForm(forms.Form):
    title = forms.CharField(label=_('title'), max_length = 254)

    def __init__(self, *args, **kwargs):
        super(ItemMetaForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = ItemMeta

    def save(self, commit=True, update=False, item_meta_type_id=None,item_meta_id=None):
        session = Session()
        
        if update:
            item_meta = session.query(ItemMeta).get(item_meta_id)
        else:
            item_meta = ItemMeta()

        item_meta.title = self.cleaned_data['title']
        item_meta.item_meta_type_id = item_meta_type_id
        
        if not update:
            session.add(item_meta)
        session.commit()        
        item_meta.id = item_meta.id
        session.close()
        
        return item_meta

from oj.constant import MARK_SEPARATOR
        
class ProblemMetaTypeForm(forms.Form):
    title = forms.CharField(label=_('title'), max_length = 254)
    item_meta_types = forms.MultipleChoiceField(label=_('item_meta_types'), choices=())

    def __init__(self, *args, **kwargs):
        super(ProblemMetaTypeForm, self).__init__(*args, **kwargs)
        session = Session()
        item_meta_type_objects = session.query(ItemMetaType).all()
        item_meta_types = [(imt.id,imt.title) for imt in item_meta_type_objects]  

        self.fields['item_meta_types'].choices = [(i[0], i[1]) for i in item_meta_types]
        session.close()
        
    class Meta:
        model = ProblemMetaType

    def save(self, commit=True, update=False, problem_meta_type_id=None):
        session = Session()
        
        if update:
            problem_meta_type = session.query(ProblemMetaType).get(problem_meta_type_id)
        else:
            problem_meta_type = ProblemMetaType()

        problem_meta_type.title = self.cleaned_data['title']
        
        item_meta_type_list = ""
        for item_meta_type in self.cleaned_data['item_meta_types']:
            item_meta_type_list += MARK_SEPARATOR + item_meta_type
        problem_meta_type.item_meta_types = item_meta_type_list
        session.expire_on_commit = False
        
        if not update:
            session.add(problem_meta_type)
        session.commit()        
        problem_meta_type.id = problem_meta_type.id
        session.close()
        
        return problem_meta_type




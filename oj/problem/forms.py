from django import forms
#from oj.models.problem import ProblemMetaType, ProblemMeta, Problem, ItemMetaType, ItemMeta, \
#    Item
from oj.sa_conn import Session
#from oj.models.problem import ProblemMetaType
from oj.tables.problem import ProblemMetaType,ProblemMeta,ItemMetaType,ItemMeta
from django.utils.translation import ugettext, ugettext_lazy as _
from django.http import Http404

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

from oj.constant import MARK_SEPARATOR,MARK_SEPARATOR_ITEM_META
        
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

class ProblemMetaForm(forms.Form):
    title = forms.CharField(label=_('title'), max_length = 254)
    #item_metas = forms.MultipleChoiceField(label=_('item_metas'), choices=())
    
    def __init__(self, *args, **kwargs):
        super(ProblemMetaForm, self).__init__(*args, **kwargs)

        data_list = kwargs["initial"]["data_list"]
        for data in data_list:
            field_name = data.field_name 
            self.fields[field_name] = forms.MultipleChoiceField(label=_(field_name), choices=([(i.id, i.title) for i in data.item_meta_object]))

        
    class Meta:
        model = ProblemMeta

    def save(self, commit=True, update=False, problem_meta_type_id=None,problem_meta_id=None,data_list=None):
        session = Session()
        
        if update:
            problem_meta = session.query(ProblemMeta).get(problem_meta_id)
        else:
            problem_meta = ProblemMeta()

        problem_meta.title = self.cleaned_data['title']
        problem_meta.problem_meta_type_id = problem_meta_type_id
        
        item_meta_list = ""
        for data in data_list:
            field_name = data.field_name
            iml = MARK_SEPARATOR + str(data.type_id)
            for item_meta in self.cleaned_data[field_name]:
                iml += MARK_SEPARATOR_ITEM_META + item_meta
            item_meta_list += iml
        problem_meta.item_metas = item_meta_list
        session.expire_on_commit = False
        
        if not update:
            session.add(problem_meta)
        session.commit()        
        problem_meta.id = problem_meta.id
        session.close()
        
        return problem_meta


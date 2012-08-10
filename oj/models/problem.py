'''
Created on 2012-8-8

@author: duoduo
'''
# coding=UTF8

class ProblemMetaType(object):
    
    def __init__(self,title="",item_meta_types=""):
        self.title = title
        self.item_meta_types = item_meta_types
        
class ProblemMeta(object):
    
    def __init__(self,title="",problem_meta_type_id=None,item_metas=""):
        self.title = title
        self.problem_meta_type_id = problem_meta_type_id
        self.item_metas = item_metas
        
class Problem(object):

    def __init__(self, title="", problem_meta_id=None,items=""):
        self.title = title
        self.problem_meta_id = problem_meta_id
        self.items = items

class ItemMetaType(object):
    
    def __init__(self,title=""):
        self.title = title

class ItemMeta(object):
    
    def __init__(self,title="",item_meta_type_id=None):
        self.title = title
        self.item_meta_type_id = item_meta_type_id
        
class Item(object):

    def __init__(self, title="", item_meta_id=None,content=""):
        self.title = title
        self.item_meta_id = item_meta_id
        self.content = content
        

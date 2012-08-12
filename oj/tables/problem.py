# coding=UTF8

from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, \
    DateTime, Text
from sqlalchemy.orm import mapper, relationship
from datetime import datetime

from oj.sa_conn import metadata

problem_meta_type = Table("ProblemMetaType", metadata,
                     Column("id", Integer, primary_key=True),
                     Column("title", String(200), nullable=False, default=""),
                     Column("item_meta_types", String(200), nullable=False, default=""),
                     extend_existing=True,
               )

problem_meta = Table("ProblemMeta", metadata,
                     Column("id", Integer, primary_key=True),
                     Column("problem_meta_type_id", Integer, ForeignKey('ProblemMetaType.id')),
                     Column("title", String(200), nullable=False, default=""),
                     Column("item_metas", String(200), nullable=False, default=""),
                     extend_existing=True,
               )

problem = Table("Problem", metadata,
                Column("id", Integer, primary_key=True),
                Column("problem_meta_id", Integer, ForeignKey('ProblemMeta.id')),
                Column("title", String(200), nullable=False, default=""),
                Column("items", String(200), nullable=False, default=""),
                extend_existing=True,
          )

item_meta_type = Table("ItemMetaType", metadata,
                     Column("id", Integer, primary_key=True),
                     Column("title", String(200), nullable=False, default=""),
                     extend_existing=True,
               )

item_meta = Table("ItemMeta", metadata,
                     Column("id", Integer, primary_key=True),
                     Column("item_meta_type_id", Integer, ForeignKey('ItemMetaType.id')),
                     Column("title", String(200), nullable=False, default=""),
                     extend_existing=True,
               )

item = Table("Item", metadata,
                Column("id", Integer, primary_key=True),
                Column("item_meta_id", Integer, ForeignKey('ItemMeta.id')),
                Column("title", String(200), nullable=False, default=""),
                Column("content", Text, nullable=False, default=""),
                extend_existing=True,
          )


#
#metaTypeCombine = Table("metaTypeCombine", metadata,
#    Column("problem_meta_type_id", Integer, ForeignKey('ProblemMetaType.id'), primary_key=True, nullable=False),
#    Column("item_meta_type_id", Integer, ForeignKey('ItemMetaType.id'), primary_key=True, nullable=False),
#    extend_existing=True,
#    ) 
#
#metaCombine = Table("metaCombine", metadata,
#    Column("problem_meta_id", Integer, ForeignKey('ProblemMeta.id'), primary_key=True, nullable=False),
#    Column("item_meta_id", Integer, ForeignKey('ItemMeta.id'), primary_key=True, nullable=False),
#    extend_existing=True,
#)
#
#problemItemCombine = Table("problemItemCombine", metadata,
#    Column("problem_id", Integer, ForeignKey('Problem.id'), primary_key=True, nullable=False),
#    Column("item_id", Integer, ForeignKey('Item.id'), primary_key=True, nullable=False),
#    extend_existing=True,
#)


metadata.create_all()



from oj.models.problem import ProblemMetaType, ProblemMeta, Problem, ItemMetaType, ItemMeta, \
    Item

mapper(ProblemMetaType, problem_meta_type, properties={
    "problem_meta":relationship(ProblemMeta, backref="problem_meta_type"),
#    "combines":relationship(ItemMetaType,
#                            #primaryjoin= problem_meta_type.c.id==metaTypeCombine.c.problem_meta_type_id,
#                            secondary=metaTypeCombine, 
#                            #secondaryjoin=item_meta_type.c.id==metaTypeCombine.c.item_meta_type_id,
#                            backref="problem_meta_type",
#                            ),
})
#mapper(ProblemMeta, problem_meta)
mapper(ProblemMeta, problem_meta, properties={
    "problem":relationship(Problem, backref="problem_meta"),
#    "combines":relationship(ItemMeta, 
#                            #primaryjoin = problem_meta.c.id==metaCombine.c.problem_meta_id,
#                            secondary=metaCombine, 
#                            #secondaryjoin = item_meta.c.id==metaCombine.c.item_meta_id,
#                            backref="problem_meta"),
})

mapper(Problem, problem)
#mapper(Problem, problem, properties={    
#    "combines":relationship(Item, 
#                            #primaryjoin= problem.c.id==problemItemCombine.c.problem_id,
#                            secondary=problemItemCombine,   
#                            #secondaryjoin=item.c.id==problemItemCombine.c.item_id,
#                            backref="problem"),
#})


mapper(ItemMetaType, item_meta_type, properties={
    "item_meta":relationship(ItemMeta, backref="item_meta_type"),
})

mapper(ItemMeta, item_meta, properties={
    "item":relationship(Item, backref="item_meta"),
})

mapper(Item, item)



from oj.utils import get_string_with_mark_separator
from oj.sa_conn import Session

def get_item_meta_types(self):
    """
    返回列表
    """
    session = Session()
    item_meta_type_objects = session.query(ItemMetaType).all()
    item_meta_types = [(imt.id,imt.title) for imt in item_meta_type_objects]
    session.close()
    return get_string_with_mark_separator(self.item_meta_types,item_meta_types)

ProblemMetaType.get_item_meta_types = get_item_meta_types



def get_item_metas(self):
    session = Session()
    item_meta_objects = session.query(ItemMeta).all()
    item_metas = [(imt.id,imt.item_meta_type_id,imt.title) for imt in item_meta_objects]
    session.close()
    return get_string_with_mark_separator(self.item_metas,item_metas)
ProblemMeta.get_item_metas = get_item_metas

def get_items(self):
    session = Session()
    item_meta_objects = session.query(ItemMeta).all()
    item_metas = [(imt.id,imt.item_meta_type_id,imt.title) for imt in item_meta_objects]
    session.close()
    return get_string_with_mark_separator(self.items,item_metas)
Problem.get_items = get_items
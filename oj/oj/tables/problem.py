# coding=UTF8

from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, \
    DateTime, Text
from sqlalchemy.orm import mapper, relationship
from datetime import datetime

from oj.sa_conn import metadata

problem_meta_type = Table("ProblemMetaType", metadata,
                     Column("id", Integer, primary_key=True),
                     Column("title", String(200), nullable=False, default="")
               )

problem_meta = Table("ProblemMeta", metadata,
                     Column("id", Integer, primary_key=True),
                     Column("problem_meta_type_id", Integer, ForeignKey('ProblemMetaType.id')),
                     Column("title", String(200), nullable=False, default="")
               )

problem = Table("Problem", metadata,
                Column("id", Integer, primary_key=True),
                Column("problem_meta_id", Integer, ForeignKey('ProblemMeta.id')),
                Column("title", String(200), nullable=False, default="")
          )

item_meta_type = Table("ItemMetaType", metadata,
                     Column("id", Integer, primary_key=True),
                     Column("title", String(200), nullable=False, default=""),
               )

item_meta = Table("ItemMeta", metadata,
                     Column("id", Integer, primary_key=True),
                     Column("item_meta_type_id", Integer, ForeignKey('ItemMetaType.id')),
                     Column("title", String(200), nullable=False, default=""),
               )

item = Table("Item", metadata,
                Column("id", Integer, primary_key=True),
                Column("item_meta_id", Integer, ForeignKey('ItemMeta.id')),
                Column("title", String(200), nullable=False, default=""),
                Column("content", Text, nullable=False, default=""),
          )



metaTypeCombine = Table("metaTypeCombine", metadata,
    Column("problem_meta_type_id", Integer, ForeignKey('ProblemMetaType.id'), primary_key=True, nullable=False),
    Column("item_meta_type_id", Integer, ForeignKey('ItemMetaType.id'), primary_key=True, nullable=False),
    ) 

metaCombine = Table("metaCombine", metadata,
    Column("problem_meta_id", Integer, ForeignKey('ProblemMeta.id'), primary_key=True, nullable=False),
    Column("item_meta_id", Integer, ForeignKey('ItemMeta.id'), primary_key=True, nullable=False),
)

problemItemCombine = Table("problemItemCombine", metadata,
    Column("problem_id", Integer, ForeignKey('Problem.id'), primary_key=True, nullable=False),
    Column("item_id", Integer, ForeignKey('Item.id'), primary_key=True, nullable=False),
)



metadata.create_all()

from oj.models.problem import ProblemMetaType, ProblemMeta, Problem, ItemMetaType, ItemMeta, \
    Item

mapper(ProblemMetaType, problem_meta_type, properties={
    "problem_meta":relationship(ProblemMeta, backref="problem_meta_type"),
    "combines":relationship(ItemMetaType, secondary=metaTypeCombine, backref="problem_meta_type"),
})

mapper(ProblemMeta, problem_meta, properties={
    "problem":relationship(Problem, backref="problem_meta"),
    "combines":relationship(ItemMeta, secondary=metaCombine, backref="problem_meta"),
})

mapper(Problem, problem, properties={    
    "combines":relationship(Item, secondary=problemItemCombine, backref="problem"),
})






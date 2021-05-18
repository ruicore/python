from typing import List, Optional

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    any_,
    column,
    create_engine,
    literal,
    select,
)
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, aliased
from sqlalchemy.orm.attributes import InstrumentedAttribute as IA

Base = declarative_base()
postgres_uri = 'postgresql://postgres:postgres@localhost:5432/postgres'
engine = create_engine(postgres_uri)
session = Session(bind=engine)
Base.metadata.bind = engine


class Tree(Base):
    """sqlalchemy model"""

    __tablename__ = 'tree'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('tree.id'))
    name = Column(String)


class TreeNode(BaseModel):
    """pydantic model"""

    id: int
    parent_id: Optional[int]
    name: str
    children: List['TreeNode'] = []


TreeNode.update_forward_refs()


def init_data():
    Base.metadata.create_all()
    session.add_all(
        (
            Tree(id=0, name='root'),
            Tree(id=1, parent_id=0, name='第一层第一个节点'),
            Tree(id=2, parent_id=0, name='第一层第二个节点'),
            Tree(id=3, parent_id=1, name='第二层第一个节点'),
            Tree(id=4, parent_id=1, name='第二层第二个节点'),
            Tree(id=5, parent_id=2, name='第二层第三个节点'),
            Tree(id=6, parent_id=2, name='第二层第四个节点'),
            Tree(id=8, parent_id=3, name='第三层第一个节点'),
        )
    )
    session.commit()


def drop_data():
    Base.metadata.bind = engine
    Base.metadata.drop_all()


def _get_nodes(node_id: int, id_col: IA, pid_col: IA, to_root: bool, *other_col):
    """
    get all child nodes or all parent nodes for a given node.
    node_id: start node's id value;
    id_col: the id column of a sqlalchemy class, often is `id`;
    pid_col: the parent id column of a sqlalchemy class, often is `parent_id`;
    to_root: to root node or to children node;
    other_col: other columns you want to select when query the nodes;
    """
    class_model = id_col.class_
    other_col_names = [col.name for col in other_col]

    hierarchy = (
        select(
            [
                id_col.label('id'),
                pid_col.label('parent_id'),
                *other_col,
                literal(0).label('level'),
                array((id_col,)).label('path'),  # array need tuple
                literal(False).label('cycle'),
            ]
        )
        .where(id_col == node_id)
        .cte(name='hierarchy', recursive=True)
    )

    next_alias = aliased(class_model, name='next_level')
    alias_id_col = getattr(next_alias, id_col.name)
    alias_pid_col = getattr(next_alias, pid_col.name)
    alias_other_col = [getattr(next_alias, col.name) for col in other_col]

    if to_root is True:
        '第一层的 parent_id 是下一层的 id'
        join_condition = hierarchy.c.parent_id == alias_id_col
    else:
        '第一层的 id 是下一层的 parent_id'
        join_condition = hierarchy.c.id == alias_pid_col

    hierarchy = hierarchy.union_all(
        select(
            [
                alias_id_col.label('id'),
                alias_pid_col.label('parent_id'),
                *alias_other_col,
                (hierarchy.c.level + 1).label('level'),
                (hierarchy.c.path + array((alias_id_col,))).label('path'),
                (alias_id_col == any_(hierarchy.c.path)).label('cycle'),
            ]
        )
        .where(hierarchy.c.cycle.is_(False))
        .select_from(hierarchy.join(next_alias, join_condition, isouter=False))
    )

    q = sa.select(
        [column('id'), column('parent_id'), *[column(name) for name in other_col_names]]
    ).select_from(hierarchy)

    return session.execute(q)


def get_children_nodes(node_id: int, id_col: IA, pid_col: IA, *other_col):
    """get all children nodes for a given node"""
    return _get_nodes(node_id, id_col, pid_col, False, *other_col)


def get_root_nodes(node_id: int, id_col: IA, pid_col: IA, *other_col):
    """get all nodes to root for a given node"""
    return _get_nodes(node_id, id_col, pid_col, True, *other_col)


def build_trees(nodes: List[TreeNode]):
    """
    build tree for given nodes
    nodes: a list of pydantic nodes
    nodes must have `id`、`parent_id`，`children` field
    """
    tree_map = {t.id: t for t in nodes}
    roots = []
    for t in nodes:
        parent_node: TreeNode = tree_map.get(t.parent_id, None)
        if parent_node is None:
            roots.append(t)
            continue
        if parent_node in t.children:
            raise Exception('detect a circle')
        parent_node.children.append(t)

    return roots


def check_move(start: int, to_node: int):
    """
    检查一个节点是否可以被移动到另一个节点之下
    :param start:
    :param to_node:
    :return:
    """
    child_nodes = get_children_nodes(start, Tree.id, Tree.parent_id)
    child_ids = [i[0] for i in child_nodes]
    if to_node in child_ids:
        raise Exception('不允许将节点移动到子节点下')


if __name__ == '__main__':
    # init_data()  # first should run this, and only run once
    """get child nodes and build tree"""
    nodes = get_children_nodes(1, Tree.id, Tree.parent_id, Tree.name)
    tree_nodes = [TreeNode(id=t[0], parent_id=t[1], name=t[2]) for t in nodes]
    trees = build_trees(tree_nodes)
    print(trees[0].json(ensure_ascii=False))

    """check move"""
    check_move(start=1, to_node=3)  # this will raise Exception
    # drop_data()

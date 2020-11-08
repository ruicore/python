import json
from typing import Any, Dict, List, Optional

import pydgraph
from pydgraph.proto import api_pb2 as api

import pydantic_types as types
DGRAPH_URL = "dgraph-alpha:9080"

stub = pydgraph.DgraphClientStub(DGRAPH_URL)
client = pydgraph.DgraphClient(stub)

"""
in dgraph, when you delete a node, the node will still exist with a single predicate `uid`.
in order to get rid of this node when doing query.
we add `type` field for each node, then use @filter(has(type) to ignore this node.
"""


def set_schema():
    """
    in order to delete node without specify predicates, schema must be set.
    if schema is not set, `delete` node will not work.
    """

    schema = """
        name: string .
        type: string .
        procedure: int .
        madeOf: [uid] @reverse .

        type Material {
            name
            type
            procedure
            madeOf
        }
    """
    alter_future = client.async_alter(pydgraph.Operation(schema=schema))
    response = pydgraph.DgraphClient.handle_alter_future(alter_future)
    return response


def drop_all():
    return client.alter(pydgraph.Operation(drop_all=True))


def execute_query(query, variables=None):
    txn = client.txn(read_only=True)
    query_future = txn.async_query(query, variables=variables)
    response = pydgraph.Txn.handle_query_future(query_future)

    return json.loads(response.json)


def execute_mutate(set_obj=None, del_obj=None):
    txn = client.txn()
    try:
        future = txn.async_mutate(set_obj=set_obj, del_obj=del_obj, commit_now=True)
        response = pydgraph.Txn.handle_mutate_future(txn, future, True)
    finally:
        txn.discard()

    return response


def get_tree(uid: str) -> Optional[types.Tree]:
    """
    query tree for a single node, a tree dict will be returned
    return:
        {
        "uid": "0x11183",
        "procedure": 1,
        "madeOf": [
            {
                "uid": "0x1117b",
                "name": "原料4",
                "type": "RAW",
                "rate": "1/2"
            },
            {
                "uid": "0x1117c",
                "name": "原料5",
                "type": "RAW",
                "rate": "3/40"
            }
        ]
    }
    """
    query = """
        query tree($uid:string){
            tree(func: uid($uid) ) @recurse @filter(has(type)) {
            uid
            procedure
            madeOf
          }
        }
    """

    variables = {'$uid': uid}
    data = execute_query(query, variables)
    if tree := data["tree"]:  # tree is empty list
        return types.Tree(**tree[0])
    else:
        return None


def get_tree_with_depth(uid: str, depth: int = 2) -> Optional[types.Tree]:
    query = """
        query tree($uid:string){
            tree(func: uid($uid) ) @recurse(depth:__depth__)@filter(has(type)) {
            uid
            procedure
            madeOf
          }
        }
    """.replace("__depth__", str(depth))

    variables = {'$uid': uid}
    data = execute_query(query, variables)
    if tree := data["tree"]:  # tree is empty list
        return types.Tree(**tree[0])
    else:
        return None


def get_path(start: str, end: str):
    query = """
        query path($start:string,$end:string){
             path as shortest(from:_from_ , to: _to_) {
                madeOf@facets(rate: rate)
             }

             get_path(func: uid(path)) {
                name
                uid
             }
    }""".replace("_from_", start).replace("_to_", end)

    data = execute_query(query)
    return next(iter(data["_path_"])) if data["_path_"] else {}


def get_node(uid: str) -> Optional[types.Tree]:
    """
    query node for given uid, a dict will be returned
    """

    query = """
    query all($uid: string) {
        node(func: uid($uid))@filter(has(type)) {
            uid
            name
            procedure
        }
    }"""

    variables = {'$uid': uid}
    data = execute_query(query, variables)
    if node := data["node"]:  # node is empty list
        return types.Tree(**node[0])
    else:
        return None


def list_tree_with_depth(uids: List[str], depth: int = 2) -> Optional[List[types.Tree]]:
    """
    query tree for each uid in uids, a list of tree will be returned
    note: this will only query for 1 depth for node edge!

    github issue: https://github.com/dgraph-io/dgraph/issues/2726
    """
    query = """
        query trees($uids: string) {
              trees(func: uid($uids)) @recurse(depth:__depth__)@filter(has(type)) {
              uid
              name
              procedure
              madeOf
            }
        }
    """.replace("__depth__", str(depth))
    uids = '[' + ','.join(uids) + ']'
    variables = {'$uids': uids}
    data = execute_query(query, variables)
    if trees := data["trees"]:
        return [types.Tree(**tree) for tree in trees]
    else:
        return None


def create_node(node: Dict[str, Any]) -> str:  # noqa
    """
    this func is used for `create node`, `update node`,
    return uid<str>
    """
    if "dgraph.type" not in node:
        node["dgraph.type"] = "Material"  # must specify type for `delete` to work
    if "uid" not in node:
        node["uid"] = "_:uid"

    return execute_mutate(set_obj=node).uids["uid"]


def create_edge(edge: Dict[str, Any]) -> None:
    """
    this func is used for `create edge`
    return uid<str>
    edge:
        {
        'uid': '0x11185',
        'procedure': 1,
        'madeOf': [
            {
                'uid': '0x11189',
            }
        ],
    }
    return None
    """

    return execute_mutate(set_obj=edge)


def update_edge(edge: dict) -> None:  # noqa
    """
    this is designed to update edge for only one give node, it will update edge which directly connect to that node.
    first, we delete all edges that directly connect to that node,
    second, we create new edge for that node.

    edge should be give like this:
        edge = {
                "uid": products_uids[0],
                'madeOf': [
                    {
                        "madeOf|rate": "1/4",
                        "uid": materials_uids[0]
                    },
                    {
                        "madeOf|rate": "2/5",
                        "uid": materials_uids[1]
                    }
                ]
            }
    """
    # first: delete origin edge
    root_uid = edge["uid"]
    delete_edge_for_node(root_uid)
    # second: create new edge
    execute_mutate(set_obj=edge)

    return


def delete_edge(edges: Dict[str, Any] = None):
    """
    this will delete edge for given edges, node itself will not be deleted,
    edges should be given like this:
        edges = {
            "uid": "0xea8d",
            "madeOf": [
                {
                    "uid": "0xea8c"
                },
                {
                    "uid": "0xea8b"
                }
            ]
        }
    """
    txn = client.txn()
    try:
        mutation = api.Mutation(delete_json=bytes(json.dumps(edges), encoding="utf-8"))
        future = txn.async_mutate(mutation=mutation, commit_now=True)
        response = pydgraph.Txn.handle_mutate_future(txn, future, True)
    finally:
        txn.discard()

    return response


def delete_edge_for_node(uid: str) -> None:
    """
    this will delete edge<depth=2> for node<uid>
    only edge that directly connected to this node will be deleted
    """
    query = """
        query tree($uid:string){
            tree(func: uid($uid) ) @recurse(depth:2)@filter(has(type)) {
            uid
            madeOf
          }
        }
    """

    tree = execute_query(query, variables={"$uid": uid})["tree"]  # return [{'uid': '0x1117f'}]
    if not tree:
        return
    tree = next(iter(tree))
    edges_deleted = {
        "uid": tree["uid"],
        "procedure": None,
        "madeOf": [{"uid": sub_tree["uid"]} for sub_tree in tree["madeOf"]]
    }
    delete_edge(edges_deleted)

    return


def delete_node(uid: str):
    execute_mutate(del_obj={'uid': str(uid)})
    return


def delete_nodes(uids: List[str]):
    execute_mutate(del_obj=[{"uid": uid} for uid in uids])


if __name__ == '__main__':
    delete_nodes(['0x17', '0x1e', '0x11'])

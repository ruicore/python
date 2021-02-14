# Tree

* Sqlalchemy Tree with Postgresql Recursive CTE
* A Simple Usage for Tree in Postgresql with Sqlalchemy

## Model

```python
# python orm model
class Tree(Base):
    """sqlalchmy model"""
    __tablename__ = "tree"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("tree.id"))
    name = Column(String)
```

```python
# a simple python tree model
class TreeNode(BaseModel):
    """pydantic model"""
    id: int
    parent_id: Optional[int]
    name: str
    children: List["TreeNode"] = []
```

## Query

### 一、查询一个节点下的所有子节点

```python
def get_children_nodes(node_id: int, id_col: IA, pid_col: IA, *other_col):
    pass
```

* `node_id`: 要查询的节点 id
* `id_col`： orm 的 model 中用来作为节点 id 的列，如上面示例中的 `Tree.id`
* `pid_col`: orm 的 model 中用来作为节点父亲节点 id 的列，如上面示例重的 `Tree.parent_id`
* `other_col`: orm 的 model 中其他你想查询的列
* 如要查询id为 1 的节点的所有节点，同时查询每个节点的 name，生成的 sql 大致如下

```sql
WITH RECURSIVE hierarchy(id, parent_id, name, level, path, cycle) AS (
    SELECT tree.id         AS id,
           tree.parent_id  AS parent_id,
           tree.name       AS name,
           1               AS level,
           ARRAY [tree.id] AS path,
           FALSE           AS cycle
    FROM tree
    WHERE tree.id = 1
    UNION ALL
    SELECT next_level.id                           AS id,
           next_level.parent_id                    AS parent_id,
           next_level.name                         AS name,
           hierarchy.level + 1                     AS level,
           hierarchy.path || ARRAY [next_level.id] AS path,
           next_level.id = ANY (hierarchy.path)    AS cycle
    FROM hierarchy
             JOIN tree AS next_level
                  ON hierarchy.id = next_level.parent_id
    WHERE hierarchy.cycle IS false)
SELECT id, parent_id, name
FROM hierarchy
```

* 注：上面在中间过程中通过查询生成了 path，level 作为 array 的示例用法，可以忽略掉
* cycle 用来判断是否有环

### 二、 查询一个节点到根节点的所有节点

```python
def get_root_nodes(node_id: int, id_col: IA, pid_col: IA, *other_col):
    pass
```

* 查询到跟节点的所有节点其实和查询子节点很像，只需要把 join 条件反过来即可
* 生成的 sql 类似如下：

```sql
WITH RECURSIVE hierarchy(id, parent_id, name, level, path, cycle) AS (
    SELECT tree.id         AS id,
           tree.parent_id  AS parent_id,
           tree.name       AS name,
           1               AS level,
           ARRAY [tree.id] AS path,
           FALSE           AS cycle
    FROM tree
    WHERE tree.id = 1
    UNION ALL
    SELECT next_level.id                           AS id,
           next_level.parent_id                    AS parent_id,
           next_level.name                         AS name,
           hierarchy.level + 1                     AS level,
           hierarchy.path || ARRAY [next_level.id] AS path,
           next_level.id = ANY (hierarchy.path)    AS cycle
    FROM hierarchy
             JOIN tree AS next_level
                  ON hierarchy.parent_id = next_level.id -- notice only here is different
    WHERE hierarchy.cycle IS false)
SELECT id, parent_id, name
FROM hierarchy
```

### 三、根据输入的所有节点，构成一颗或多颗树

* 示例代码中使用 pydantic 将从数据库中查询出来的结果转换成了 class，不转换也可以，但是访问属性的方式需要由 `Tree.id` --&gt; `Tree["id]`
* 核心思想是将当前节点塞到父节点下，如果当前节点没有父节点，那么当前节点就是根节点
* 在遍历的时候，检测有没有环的生成，即：当前节点的`父节点`不在当前节点的`子节点`中

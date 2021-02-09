
问题场景：将 JSON-LD 数据导入到 Neo4j 的数据库中，
Crete Time : 2020-01-16 19:04:21.302373

# 一、将 JSON-LD 数据导入 Neo4j

* 针对每个 Json-LD 文件，使用 batch 的方式导入 Neo4j 数据库。
* 导入 JSON-LD 需要两个插件 [APOC](https://github.com/neo4j-contrib/neo4j-apoc-procedures) 和 [neosemantics](https://github.com/neo4j-labs/neosemantics) 的支持（最低版本需要 3.5）。
* 插件的下载页面下载 jar 包之后，放入 Neo4j 的 plugins 目录，然后配置 conf 目录下的 neo4j.conf 文件，添加 ```dbms.unmanaged_extension_classes=semantics.extension=/rdf``` 配置，如果 dbms.unmanaged_extension_classes 的配置不止一项，可写如为 ```dbms.unmanaged_extension_classes=org.neo4j.graphql=/graphql,semantics.extension=/rdf``` 格式


```py

import json
import logging
import os
import time

from neo4j import GraphDatabase

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("load2neo4j.log", "a")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(process)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())
logger.setLevel("INFO")

batch_size = 17
uri = "bolt://localhost:11002" # 使用 bolt 链接的 RUI

neosemantics_import_cypher = '''UNWIND  $json_node_list as rdf_fragment
        CALL semantics.importRDFSnippet(rdf_fragment,"JSON-LD",{handleMultival: "ARRAY",multivalPropList : ["http://socrates.aidigger.com/property/alias"]})
        YIELD terminationStatus, triplesLoaded, triplesParsed, extraInfo
        RETURN terminationStatus, sum(triplesLoaded) as totalLoaded, sum(triplesParsed) as totalParsed '''.replace('\n', '')


def log_time(func):
    def wrapper(path):
        start = time.time()
        res = func(path)
        end = time.time()
        logger.info("导入文件 {} 插入 {} 条数据，用时 {:.2f}s".format(path, res, end-start))
        return res
    return wrapper


def load_batch(tx, batch):
    logger.info("Submitting batch of size {}".format(str(len(batch))))
    try:
        for record in tx.run(cypher_neosemantics, payload=batch):  # 可能触发 property 名称太长超出限制的异常
            logger.info('status:{} , triplesLoaded: {} , triplesParsed: {}'.format(record["terminationStatus"], record["totalLoaded"], record["totalParsed"]))
    except Exception as e:
        logger.error(str(e))
    return


@log_time
def load_to_neo4j(file_path, user_name="neo4j", pass_word="1"):
    cnt_item = 0
    driver = GraphDatabase.driver(uri, auth=(user_name, pass_word))
    with driver.session() as session:
        with open(file_path, mode='r') as jsonl_file:
            data = json.loads(jsonl_file.read())
            cnt_item = len(data)
            for i in range(0, cnt_item, batch_size):
                batch = [json.dumps(x) for x in data[i:i+batch_size]]
                session.write_transaction(load_batch, batch)
            session.read_transaction(load_batch, batch)
    driver.close()
    return cnt_item


if __name__ == "__main__":
    file_path = "sample.json"
    load_to_neo4j(file_path)
```

# 二、将数据从 Neo4j 导出，再导入到另一个 Neo4j 数据库

* Neo4j 数据库版本为 3.5，使用 apoc 插件，将数据导出为 graphml 格式，再导入。
* 使用 apoc 的导入导出功能，需要在 conf 中配置
```
dbms.security.procedures.unrestricted=apoc.export.*,apoc.import.*
apoc.export.file.enabled=true
apoc.import.file.enabled=true
```

* 在 Neo4j 提供的网页界面中，使用如下命令导入导出：
* 导出：```CALL apoc.export.graphml.all(<filename.graphml>, {useTypes:true, storeNodeIds:false,readLabels:true})```
* 导入：```CALL apoc.import.graphml(<filename.graphml>, {batchSize: 10000, storeNodeIds: false,readLabels:true})```

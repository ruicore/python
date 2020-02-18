### 随机分区
* df.randomSplit([0.5,0.5])
### 去重复
* df.drop_duplicates()
### join 链接

* 根据某个字段将不同的数据合并起来
```py
from pyspark.sql.functions import col

left_join = df.alias('ac').join(df_alias.alias('bc'), df["lemma_id"] == df_alias["lemma_id"], how='left_outer').select([col('ac.' + x) for x in df.columns] + [col('bc.key_words')])
full_outer_join = df.join(df_map, df["data"] == df_map["url"], how='full')
```
### df group and count
```py
import pyspark.sql.functions as f
df.groupBy('key').count().select('key', f.col('count').alias('times')).sort(f.desc("times"))
```
### df and aggregate

* 使用场景：需要根据一个字段对原数据进行 group，然后对 group 过后的每个组内的相同字段采用某种方式合并，如：
* 根据 id 将下面的数据分组，将每个组内的 data 合并。
```py
{"id":1,"data":{"key1":"value1","key2":"value2"}}

{"id":2,"data":{"key1":"value1","key3":"value3"}}

{"id":2,"data":{"key4":"value4","key4":"value4"}}

{"id":1,"data":{"key5":"value5","key2":"value2"}}
```
```py
from pyspark.sql.types import StringType
from pyspark.sql.functions import col, collect_list, concat_ws, udf

def convert_dict(data_list):
    tmp_dict = dict()
    for val in data_list:
        tmp_dict.update(json.loads(val))

    return json.dumps(tmp_dict, ensure_ascii=False)


def convert_list(data_list):
    tmp_list = []
    for val in data_list:
        if val:
            tmp_list.extend(json.loads(val))
    return list(set(tmp_list))


myUdf = udf(convert_dict, StringType())
myUdf2 = udf(convert_list, StringType())

new_df = df.groupby("lemma_id").agg(collect_list('data').alias('data'), collect_list('alias').alias("alias")).\
    withColumn('data', myUdf('data')).\
    withColumn('alias', myUdf2('alias'))
```

### 
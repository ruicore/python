# 词语分析聚合
* 对 5118 网站下载的长尾词进行分析、聚合

## 使用方法

* 将 5118 下载的所有文件放到 zip 目录下（不需要解压）
* 安装 python3.9, [官网](https://www.python.org/downloads/release/python-390/)
* 在根目录下（5118） 下打开终端，依次执行以下命令

```shell script
python3.9 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
python analysis.py
```
* 程序执行完之后将输出两个文件，`keys.csv`,`res.xlsx`
* 其中 keys.csv 是所有的关键词，res.xlsx 是分类之后的结果


## PySpark简介及环境搭建

#### 简介

Apache Spark 是基于内存计算的批处理实时处理框架, 支持交互式查询和迭代式算法

Apache Spark  是Scala 语言实现的, 为了支持Python语言使用Spark, Apache Spark 社区开发了一个工具--PySpark, 利用PySpark中的Py4J库, 我们可以通过Python语言操作RDD

> 开发原因: python丰富的拓展库和行业使用python的人数众多
>
> pyspark 提供 pyspark shell, 结合了python api 和spark core的工具, pyspark shell在启动时会初始化Spark环境

#### 环境搭建

1 安装Java

2 下载并安装 Apache Spark

```shell
1. 下载链接(spark2.4.4-hadoop2.7): http://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
2. 解压并设置环境变量
	tar -zxvf /Users/ysx_along/Downloads/spark-2.4.4-bin-hadoop2.7
	mv  spark-2.4.4-bin-hadoop2.7  /Users/ysx_along/spark/
	vim ~/.bash_profile
  	export SPARK_HOME=/Users/ysx_along/spark/spark-2.4.4-bin-hadoop2.7
    export PATH=$PATH:/Users/ysx_along/spark/spark-2.4.4-bin-hadoop2.7/bin
    export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH
    export PATH=$PATH:/Users/ysx_along/bin:$SPARK_HOME/python
	source ~/.bash_profile
3. 启动  pyspark(/Users/ysx_along/spark/spark-2.4.4-bin-hadoop2.7/bin/pyspark)
	出现  SparkSession available as 'spark'.  表示spark shell启动成功并初始化了spark环境
-- windows 安装pyspark 参考以下链接
	https://www.cnblogs.com/twodoge/p/10740791.html
```

3 本地连接远程服务器上的hive数据

```shell
将远程服务器上的 mapred-site.xml  hdfs-site.xml  yarn-site.xml  core-site.xml文件拉到本地的SPARK_HOME 的conf目录下

代码中指定 SPARK_HOME  hive元数据地址
from pyspark.sql import SparkSession
os.environ["SPARK_HOME"] = "/Users/ysx_along/spark/spark-2.4.4-bin-hadoop2.7"
spark = SparkSession.builder.appName('along_test').config('hive.metastore.uris', 'thrift://bj-bi-cdh-01:9083,thrift://bj-bi-cdh-02:9083,thrift://bj-bi-cdh-03:9083,thrift://bj-bi-cdh-04:9083').master('local').enableHiveSupport().getOrCreate()
```





## SparkContext 和 RDD

#### SparkContext

SparkContext 是所有spark功能的入口, 无论希望运行什么spark应用, 都需要初始化SparkContext来驱动程序执行.

```python
SparkContext类属性:
"""
master:Spark集群的入口url地址.
appName:任务名称.
sparkHome:Spark安装目录.
pyFiles:.zip 或 .py 文件可发送给集群或添加至环境变量中.
Environment:Spark Worker节点的环境变量.
batchSize:批处理数量.设置为1表示禁用批处理, 设置0以根据对象大小自动选择批处理大小, 设置为-1以使用无限批处理大小.
Serializer:RDD序列化器.
Conf:SparkConf对象, 用于设置Spark集群的相关属性.
Gateway:选择使用现有网关和JVM或初始化新JVM.
JSC:JavaSparkContext实例.
profiler_cls:可用于进行性能分析的自定义Profiler(默认为pyspark.profiler.BasicProfiler)
"""
class pyspark.SparkContext (
   master = None,
   appName = None, 
   sparkHome = None, 
   pyFiles = None, 
   environment = None, 
   batchSize = 0, 
   serializer = PickleSerializer(), 
   conf = None, 
   gateway = None, 
   jsc = None, 
   profiler_cls = <class 'pyspark.profiler.basicprofiler'="">
)
上述参数中, master和appName是最常用的参数, 几乎所有的应用都需要传入这两个参数
```

pyspark shell 统计字符个数

```shell
# 启动pyspark

path_ = r"/Users/ysx_along/spark/spark-2.4.4-bin-hadoop2.7"
logfile = f"file://{path_}/README.md"
logdata = sc.textFile(logfile).cache()
numAs = logdata.filter(lambda s: 'a' in s).count()
numBs = logdata.filter(lambda s: 'b' in s).count()
print(numAs, numBs)
# 62 31
```

python 脚本

```shell
vim  /Users/ysx_along/spark/spark_test.py
```

```python
from pyspark import SparkContext
sc = SparkContext("local", "first app")

path_ = r"/Users/ysx_along/spark/spark-2.4.4-bin-hadoop2.7"
logfile = f"file://{path_}/README.md"
logdata = sc.textFile(logfile).cache()
numAs = logdata.filter(lambda s: 'a' in s).count()
numBs = logdata.filter(lambda s: 'b' in s).count()

print(numAs,numBs)
# 62 31
```

```shell
spark-submit /Users/ysx_along/spark/spark_test.py
#在输出内容中找得到结果 62 31
```

```shell
#spark提交py脚本指定参数
	# 指定python路径
--conf spark.pyspark.python=/usr/bin/python3  
--conf spark.pyspark.driver.python=/usr/bin/python3 

	# 指定数据内存大小
--conf spark.rpc.message.maxSize=512

	# 指定使用的资源
	--driver-memory 2G
	--num-executors 4
	--executor-memory 4G 
	--executor-cores 4 

/usr/bin/spark2-submit --conf spark.pyspark.python=/usr/bin/python3 --conf spark.pyspark.driver.python=/usr/bin/python3 --conf spark.rpc.message.maxSize=512  --driver-memory 2G  --num-executors 4 --executor-memory 4G --executor-cores 4    /home/timers/DataMachine_for_wh/src/whTask/along_test_warehouse.py

```



#### RDD

RDD(Resilient Distributed Dataset)弹性式分布数据集, 是可以在多个节点上运行和操作的数据,从而实现高效并行计算. 一旦创建了RDD, 就无法对其进行修改

RDD的操作分为两种形式:

1. Transformation(转换): 此类型的操作应用与一个RDD后会得到一个新的RDD

   例如: map, filter, groupByKey, reduceByKey, sortByKey, join等

2. Action(动作): 此类型的操作应用于一个RDD后,用于指示Spark执行计算并将计算结果返回

   例如: reduce, collect, count, first, take, saveAsTextFile, foreach, top, lookup

```python
RDD类定义:
class pyspark.RDD (
   jrdd, 
   ctx, 
   jrdd_deserializer = AutoBatchedSerializer(PickleSerializer())
)
```

RDD基础操作

```python
alist = ["scala", "java", "hadoop", "spark", "apache", "spark vs hadoop", "pyspark","pyspark and spark"]
words = sc.parallelize (alist)

-- count()函数返回RDD中元素的数量
print(words.count()) # 8 

-- foreach函数接收一个函数作为参数，将RDD中所有的元素作为参数调用传入的函数
def function1(x):
      print(x)
words.foreach(function1) 

      
-- filter函数传入一个过滤器函数，并将过滤器函数应用于原有RDD中的所有元素，并将满足过滤器条件的RDD元素存放至一个新的RDD对象中并返回
print(words.filter(lambda x: 'spark' in x).collect())
# ['spark', 'spark vs hadoop', 'pyspark', 'pyspark and spark']

-- map函数传入一个函数作为参数，并将该函数应用于原有RDD中的所有元素，将所有元素针对该函数的输出存放至一个新的RDD对象中并返回
print(words.map(lambda x: (x, 1)).collect())
# [('scala', 1), ('java', 1), ('hadoop', 1), ('spark', 1), ('akka', 1), ('spark vs hadoop', 1), ('pyspark', 1), ('pyspark and spark', 1)]


-- reduce函数接收一些特殊的运算符，通过将原有RDD中的所有元素按照指定运算符进行计算，并返回计算结果, 例如累加
from operator import add
print(sc.parallelize([1, 2, 3, 4, 5]).reduce(add)) # 15

-- join函数()对RDD对象中的Key进行匹配，将相同key中的元素合并在一起，并返回新的RDD对象
x = sc.parallelize([("spark", 1), ("hadoop", 4)])
y = sc.parallelize([("spark", 2), ("hadoop", 5)])
joined = x.join(y)
print(joined.collect())
# [('hadoop', (4, 5)), ('spark', (1, 2))]


-- cache()函数可以对RDD对象进行默认方式(memory)进行持久化
words.cache() 
print(words.persist().is_cached)
# True
```



 










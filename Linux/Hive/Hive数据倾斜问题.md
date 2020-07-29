# Hive数据倾斜问题

数据倾斜, 即单个节点任务所处理的数据量远大于同类型任务所处理的数据量, 导致该节点成为整个作业的瓶颈, 这是分布式系统不可能避免的问题.

从本质上说, 导致数据倾斜有两种原因: 1 任务读取大文件, 2 任务需要处理大量相同键的数据

### mapreduce实际处理流程

**input --> map --> partition --> combine --> sort --> reduce --> output**



## 任务读取大文件

最常见的是读取压缩的不可分割的大文件, 当对数据进行归档或转储时会需要对数据进行压缩, 当对文件使用gzip压缩等不支持文件分割的压缩方式时, 读取该压缩文件只会被一个map任务读取, 如果压缩文件很大, 处理该文件的map需要花费的时间会远大于读取普通文件的map时间, 该map任务就会成为作业运行的瓶颈

解决方案: 1) 数据压缩时采用bzip2/zip/snappy等压缩算法 2) 合理分区

## 任务需要处理大量相同键的数据

1 业务无关的数据/异常值引发的数据倾斜

实际业务中有大量的NULL值或者一些无意义的数据参与到计算作业中, 这些作业可能来自业务上报/数据规范对数据进行归一化变为NULL/空字符串等, 这些与业务无关的数据引入导致在进行分组聚合或者表连接时发生数据倾斜



解决方案: 1) 根据业务需求排除异常数据; 2) 将异常值与正常值分开处理; 3) 表关联时类型保持一致



2 聚合函数引起的数据倾斜

在mapreduce任务中, reduce接收的数据是分区的结果, 分区是对key求hash值,根据hash值决定key被分到哪个分区,进而被分配到某个reduce. 在聚合函数的过程中, 如果聚合的维度值很集中,那分配到某些reduce任务的数据量就会很大, 该reduce任务处理的数据量将远大于其他reduce任务, 该reduce任务就会成为作业运行的瓶颈

解决方案: 1) 在map阶段给key增加一个随机数, 减小被分配到同一个reduce的概率 

2) 设置负载均衡 hive.groupby.skewindata=true, 开启后会有两个mapreduce任务, 第一个job中, map阶段的输出结果会随机分布到reduce中,每个reduce做部分聚合操作然后输出给第二个mapreduce任务,第二个job会根据key的hash值进行分配,完成最终的聚合.  核心原理就是第一个任务随机分配到不同的reduce上进行计算做部分聚合, 减少数据量, 然后第二个任务进行最终聚合

3) map端开启聚合, 减少进入到reduce阶段的数据量 set hive.map.aggr=true; 



4) 设置reduce能处理的数据大小  set  hive.exec.reducers.bytes.per.reducer=1000000000  (单位为字节,默认1G)

5) 设置最大开启的reduce个数  set hive.exec.reducers.max=999 (默认999)  与4同时配置都不会生效

6) 增加资源, 增加jvm内存

7) 将count(distinct) 改成 sum...group by的形式

 select a,count(distinct b) from t group by a  -->  select a,sum(1) from (select a, b from t group by a,b) group by a












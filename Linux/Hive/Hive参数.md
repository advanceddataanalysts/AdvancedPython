# Hive参数

```shell
#查看集群设置的文件块大小, 默认128M, 只能在配置文件修改,不能在hive中自定义修改
set dfs.block.size;

#是否动态分区
set hive.exec.dynamici.partition   --默认false:未开启动态分区;true:开启

#动态分区是否允许所有的分区列都是动态分区列
set hive.exec.dynamic.partition.mode   --默认strict:不允许所有分区列全部是动态的; nostrick:允许

#每个mapreduce job允许创建的分区的最大数量
set hive.exec.max.dynamic.partitions.pernode --默认100

#一个dml语句允许创建的所以分区的最大数量
set hive.exec.max.dynamic.partitions  --默认1000

#所有的mapreduce job允许创建的文件的最大数量
set hive.exec.max.created.files  --默认100000

#当输出文件的平均大小小于该值时,启动一个独立的map-reduce任务进行文件merge
set hive.merge.smallfiles.avgsize  --例如16777216为16M
```
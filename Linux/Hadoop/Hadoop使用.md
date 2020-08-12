# Hadoop使用

#### 服务器与hdfs文件系统进行交互的命令 hdfs dfs | hadoop dfs | hadoop fs 区别与联系

```shell
hadoop fs: #可以用于其他文件系统, 不止hdfs文件系统内
(FS relates to a generic file system which can point to any file systems like local, HDFS etc. So this can be used when you are dealing with different file systems such as Local FS, HFTP FS, S3 FS, and others)
	
hadoop dfs: #专门针对hdfs分布式文件系统
(dfs is very specific to HDFS. would work for operation relates to HDFS. This has been deprecated and we should use hdfs dfs instead)

hdfs dfs: #与hadoop dfs一样, 但是更为推荐,在使用hadoop dfs 时内部会被转化为hdfs dfs
```

#### 与hdfs文件系统交互常用指令

```shell
-- 很多命令都是 hdfs dfs -<linux命令> <参数> <选项>

#列出hdfs下的文件
hdfs  dfs  -ls  <目录>

#将Linux系统本地文件上传到HDFS中
hdfs  dfs  -put  <本地文件>  <HDFS文件>

#将HDFS中的文件下载到Linux系统本地目录
hdfs dfs  -get  <HDFS文件>  <本地文件>
 
#查看文件
hdfs dfs  -cat  <HDFS文件>

#建立目录
hdfs dfs  -mkdir  <目录>

#删除文件
hdfs dfs  -rm -r  <文件/目录>

#统计文件个数
hdfs dfs -count /user/hive/warehouse/ysx_test.db/along_partition_test/partition_by_month=202001

#统计文件夹下各个文件/文件夹的大小
hdfs dfs -du -h /user/hive/warehouse/ysx_test.db/along_partition_test/
#统计文件夹的大小
hdfs dfs -du -h -s /user/hive/warehouse/ysx_test.db/along_partition_test/
-s: 统计文件夹的大小, 不带-s则为统计文件夹下各个文件/文件夹大小
-h: 以K/M/G为单位展示大小, 不带-h则为字节数
```

#### 查看yarn任务及终止application进程

```shell
#查看 http://<yarn-service-ip>:8088/cluster/apps/RUNNING
yarn application -list

#终止进程
yarn application -kill <Application-Id>
```
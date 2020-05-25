# Hive使用

```shell
-- 启动客户端
# hive 和 hive --service cli命令一样
hive
hive --service cli

--创建表
create [external] table `ysx_test.along_insert_test`(
  `order_id` bigint,
  `order_callback_time` string,
  `partition_by_month` string,
  `etl_load_at` string)
partitioned by(`dt` string)
row format delimited fields terminated by '\u0001' ;
[location '/user/hive/warehouse/ysx_test_external/along_insert_test';]

创建表加参数external则指定创建的表为外部表, location不加则为默认的hdfs路径(通过set hive.metastore.warehouse.dir; 查看默认路径)
ROW FORMAT DELIMITED: 分隔符设置开始语句
FIELDS TERMINATED BY: 设置字段与字段之间的分隔符
COLLECTION ITEMS TERMINATED BY: 设置一个复杂类型(array,struct)字段的各个item之间的分隔符
MAP KEYS TERMINATED BY: 设置一个复杂类型(Map)字段的key value之间的分隔符
LINES TERMINATED BY: 设置行与行之间的分隔符

#ROW FORMAT DELIMITED 必须在其它分隔设置之前,也就是分隔符设置语句的最前
#LINES TERMINATED BY必须在其它分隔设置之后,也就是分隔符设置语句的最后

-- load语法
load data [local] inpath 'filepath' [overwrite] 
overwrite覆盖表中原内容

load data local inpath '/root/data/data.txt' overwrite into table partition_table partition(gender='M');


-- 查看表信息
#简要信息
desc ysx_test.along_insert_test;

#详细信息
desc extended ysx_test.along_insert_test;

#完整信息
desc formatted ysx_test.along_insert_test;

#建表语句
show create table ysx_test.along_insert_test;

-- 查看Hive参数
set hive属性名;
例如查看集群设置的文件块大小 set dfs.block.size;
```

## Hive元数据表
### Hive版本的元数据表(VERSION)
SCHEMA_VERSION: Hive版本

VERSION_COMMENT: 版本说明

> 如果该表出现了问题, 根本进入不了Hive-Cli

### Hive数据库相关的元数据表(DBS, DATABASE_PARAMS)
#### DBS: 存储Hive所有数据库的基本信息
DB_ID: 数据库ID 

DESC: 数据库描述 

DB_LOCATION_URI: 数据库 HDFS 路径 

NAME: 数据库名 

OWNER_NAME: 数据库所有者用户名 

OWNER_TYPE: 所有者角色 

#### DATABASE_PARAMS: 该表存储数据库的相关参数, 在 CREATE DATABASE 时候用WITH DBPROPERTIES (property_name=property_value, …) 指定的参数
DB_ID: 数据库ID

PARAM_KEY: 参数名

PARAM_VALUE: 参数值

### Hive表和视图相关的元数据表(主要: TBLS, TABLE_PARAMS, TBL_PRIVS这三张表,通过TBL_ID关联
#### TBLS: 存储Hive表, 视图, 索引表的基本信息
TBL_ID: 表ID

CREATE_TIME: 创建时间

DB_ID: 数据库 

LAST_ACCESS_TIME: 上次访问时间

OWNER: 所有者

RETENTION: 保留字段

SD_ID: 序列化配置信息

TBL_NAME: 表名

TBL_TYPE: 表类型

VIEW_EXPANDED_TEXT: 视图的详细 HQL

VIEW_ORIGINAL_TEXT: 视图的原始 HQL

#### TABLE_PARAMS: 存储表/视图的属性信息
TBL_ID: 表ID

PARAM_KEY: 属性名

PARAM_VALUE: 属性值

#### TBL_PRIVS: 存储表/视图的授权信息
TBL_GRANT_ID: 授权ID

CREATE_TIME: 授权时间

GRANT_OPTION:  

GRANTOR: 授权执行用户

GRANTOR_TYPE: 授权者类型

PRINCIPAL_NAME: 被授权用户

PRINCIPAL_TYPE: 被授权用户类型

TBL_PRIV: 权限

TBL_ID: 表ID

### Hive 文件存储信息相关的元数据表(主要: SDS, SD_PARAMS, SERDES, SERDE_PARAMS)
由于 HDFS 支持的文件格式很多, 而建 Hive 表时候也可以指定各种文件格式, Hive 在将 HQL 解析成 MapReduce 时候, 需要知道去哪里, 使用哪种格式去读写 HDFS 文件, 而这些信息就保存在这几张表中
#### SDS: 该表保存文件存储的基本信息, 如 INPUT_FORMAT, OUTPUT_FORMAT, 是否压缩等, TBLS 表中的 SD_ID 与该表关联, 可以获取 Hive 表的存储信息
SD_ID: 存储信息ID

CD_ID: 字段信息ID

INPUT_FORMAT: 文件输入格式

IS_COMPRESSED: 是否压缩

IS_STOREDASSUBDIRECTORIES: 是否以子目录存储

LOCATION: HDFS

NUM_BUCKETS: 分桶数量

OUTPUT_FORMAT: 文件输出格式

SERDE_ID: 序列化类ID

#### SD_PARAMS: 该表存储 Hive 存储的属性信息，在创建表时候使用STORED BY 'storage.handler.class.name' [WITH SERDEPROPERTIES (…) 指定
SD_ID: 序列化类配置ID

PARAM_KEY: 存储属性名

PARAM_VALUE: 存储属性值 

#### SERDES:  该表存储序列化使用的类信息
SD_ID: 序列化类配置ID

NAME: 序列化类别名

SLIB: 序列化类

#### SERDE_PARAMS:  该表存储序列化的一些属性的格式信息, 比如: 行, 列分隔符
SD_ID: 序列化类配置ID

PARAM_KEY: 存储属性名

PARAM_VALUE: 存储属性值 

### Hive 表字段相关的元数据表(主要: COLUMNS_V2)
#### COLUMNS_V2: 该表存储表对应的字段信息
CD_ID: 字段信息ID(通过SDS表的CD_ID关联对应的Hive表)

COMMENT: 字段注释

COLUMN_NAME: 字段名

TYPE_NAME: 字段类型

INTEGER_IDX: 字段顺序

### Hive 表分区相关的元数据表(主要: PARTITIONS, PARTITION_KEYS, PARTITION_KEY_VALS, PARTITION_PARAMS)
#### PARTITIONS: 该表存储表分区的基本信息
PART_ID: 分区ID

CREATE_TIME: 分区创建时间

LAST_ACCESS_TIME: 最后一次访问时间

PART_NAME: 分区名

SD_ID: 分区存储ID

TBL_ID: 表ID

#### PARTITION_KEYS: 该表存储分区的字段信息
TBL_ID: 表
PKEY_COMMENT: 分区字段说明

PKEY_NAME: 分区字段名

PKEY_TYPE: 分区字段类型

INTEGER_IDX: 分区字段顺序

#### PARTITION_KEY_VALS: 该表存储分区字段值
PART_ID: 分区ID

PART_KEY_VAL: 分区字段值

PART_KEY_IDX: 分区字段值顺序

#### PARTITION_PARAMS: 该表存储分区的属性信息
PART_ID: 分区ID

PARAM_KEY: 分区属性名

PARAM_VALUE: 分区属性值

### 其他不常用的表
DB_PRIVS: 数据库权限信息表,通过 GRANT 语句对数据库授权后, 将会在这里存储

IDXS: 索引表, 存储 Hive 索引相关的元数据

INDEX_PARAMS: 索引相关的属性信息

TAB_COL_STATS:表字段的统计信息,使用 ANALYZE 语句对表字段分析后记录在这里

TBL_COL_PRIVS: 表字段的授权信息

PART_PRIVS: 分区的授权信息

PART_COL_STATS: 分区字段的统计信息

PART_COL_PRIVS: 分区字段的权限信息

FUNCS: 用户注册的函数信息

FUNC_RU: 用户注册函数的资源信息





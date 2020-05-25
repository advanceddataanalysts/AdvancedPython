# Hive简介

## 什么是 Hive

1: Hive 由 Facebook 实现并开源, 基于Hadoop 的一个数据仓库工具

**2: 将结构化的数据映射为一张数据库表并提供HQL(Hive SQL) 查询功能**

**3: 底层的结构化数据存储在 HDFS 上, 本质是将 HQL 语句转换为 MapReduce 任务运行**

> Hive 依赖于 HDFS 存储数据, Hive 将 HQL 转换成 MapReduce 执行, 所以说 Hive 是基于 Hadoop 的一个数据仓库工具, 实质就是一款基于 HDFS 的 MapReduce 计算框架, 对存储在 HDFS 中的数据进行分析和管理


## 为什么使用 Hive

直接使用 MapReduce 所面临的问题:
人员学习成本太高; 项目周期要求太短; MapReduce 实现复杂查询逻辑开发难度太大

Hive的优势:
1: 更友好的接口: 操作接口采用类 SQL 的语法, 提供快速开发的能力

2: 更低的学习成本: 避免了写 MapReduce, 减少开发人员的学习成本

3: 更好的扩展性: 可自由扩展集群规模而无需重启服务; 支持用户自定义函数

Hive的缺点:
1: 不支持数据记录级别的增删改查 (有数据变更可以通过insert overwrite 重新插入数据)

2: 因为MapReduce Job启动过程查询延时严重, 查询延时严重



## Hive架构

![PNG](/image/hive-framework.png)

#### 1 用户接口: Shell/CLI; JDBC/ODBC; WebUI
1: CLI(Command Line Interface)与Shell 终端命令行, 采用交互形式使用 Hive命令行与 Hive进行交互

2: JDBC/ODBC 是Hive基于JDBC操作提供的客户端, 可以使用户通过连接到Hive Server服务

3: WebUI 通过浏览器访问Hive

#### 2 跨语言服务: thrift server
Thrift是Facebook开发的软件框架, 用来进行可扩展且跨语言的服务的开发, Hive 集成了该服务,能让不同的编程语言调用 Hive 的接口

#### 3 底层的Driver: Driver(驱动器); Compiler(编译器); Optimizer(优化器); Executor(执行器)

Driver 组件完成 HQL 查询语句从词法分析, 语法分析, 编译, 优化, 以及生成逻辑执行 计划的生成; 生成的逻辑执行计划存储在 HDFS 中, 并随后由 MapReduce 调用执行

Hive 的核心是驱动引擎,  驱动引擎由四部分组成：

Driver(驱动器): 解释器的作用是将 HiveSQL 语句转换为抽象语法树(AST)

Compiler(编译器): 编译器是将语法树编译为逻辑执行计划

Optimizer(优化器): 优化器是对逻辑执行计划进行优化

Executor(执行器): 执行器是调用底层的运行框架执行逻辑执行计划

#### 4 元数据存储系统
元数据就是存储在Hive中的数据的描述信息, 包括表的名字/列/分区/属性(内外部表)/数据所在路径等

Metastore 默认存在自带的 Derby 数据库中

缺点是不适合多用户操作, 并且数据存储目录不固定, 数据库跟着 Hive 走,极度不方便管理, 所以更多的是将元数据保存在自建的MySQL数据库中, Hive和MySQL之间通过Matastore服务交互

#### 执行流程
HiveQL 通过命令行或者客户端提交, 经过 Compiler 编译器, 运用 MetaStore 中的元数据进行类型检测和语法分析, 生成一个逻辑方案 (Logical Plan), 然后通过的优化处理, 产生一个 MapReduce 任务


## Hive数据组织
Hive 的存储结构包括**数据库,表,视图,分区和表数据**等
1 数据库,表,分区等都对应 HDFS 上的一个目录, 表数据对应 HDFS 对应目录下的文件

2 Hive中所有的数据都存储在 HDFS 中, 没有专门的数据存储格式, 支持 TextFile,SequenceFile,RCFiled等自定义格式等, 只要在建表的时候告诉Hive数据中的列分隔符和行分隔符, Hive就可以解析数据

3 数据模型

```shell
database: 在 HDFS 中表现为 ${hive.metastore.warehouse.dir} 目录下一个文件夹(通过set hive.metastore.warehouse.dir; 查看默认路径)
table: 在 HDFS 中表现所属 database 目录下一个文件夹
external table: 与 table 类似,不过其数据存放位置可以指定任意 HDFS 目录路径
partition: 在 HDFS 中表现为 table 目录下的子目录
bucket: 在 HDFS 中表现为同一个表目录或者分区目录下根据某个字段的值进行 hash 散列之后的多个文件
view: 与传统数据库类似, 只读, 基于基本表创建
```

#### 内部表(MANAGED_TABLE)和外部表(EXTERNAL_TABLE)的区别
(drop table语句)删除内部表的时候, 删除表元数据和数据
(drop table语句)删除外部表的时候, 删除表元数据, 不删除数据

如果数据的所有处理都在Hive中进行, 倾向于选择内部表; 如果Hive和其他工具针对相同的数据集进行处理, 外部表更合适(自己使用的表建内部表方便操作, 多人使用的建外部表防止误删)

#### 分区表和分桶表的区别
分区表是手动添加分区, 分桶表的数据是按照某些分桶字段进行 hash 散列形成的多个文件, 数据准确性更高







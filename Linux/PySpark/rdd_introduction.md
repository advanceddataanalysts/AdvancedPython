---
typora-root-url: ..

---

# RDD

Resilient Distributed DataSet, 弹性式分布数据集.

spark中最基本的数据抽象

### RDD三大特性 :  分区, 不可变, 并行操作

#### 分区

每一个RDD包含的数据被存储在系统的不同节点上, RDD只是抽象意义的数据集合, 分区内部不存储实际的数据, 只存储它在改RDD中的index, 通过RDD的id和分区的index可以唯一确定对应的数据块, 然后通过底层接口提取对应的数据进行处理.

在集群中, 各个节点上的数据块尽可能的存储在内存中, 只有内存没有空间时才会放到硬盘存储, 这种存储方式最大化的减少了磁盘IO的开销

> 逻辑上可以将RDD理解成一个数组, 数组中的每个元素就代表一个分区(partition)
>
> 物理存储中,每个分区指向一个存储在内存或硬盘中的数据块(block)

#### 不可变

每个RDD **仅可读**, 其所包含的分区信息 **不可变**

只有对现有的RDD进行 Transformation(转化)操作, 才能得到新的RDD, 然后经过多次计算迭代得到我们想要的结果

> 不可变特性的好处: 
>
> 1. 节省内存空间,提高计算效率, 在RDD计算过程中, 不需要立即去存储计算出的数据, 只要记录每个RDD是经过哪些转化操作得到的, 只记录依赖关系即可
> 2. 错误恢复更容易, 如果在计算中节点发生故障, 数据丢失, 可以直接依据依赖关系从上一步去重新计算RDD, 实现 *弹性*

#### 并行操作

不同节点上的数据可以分别被处理, 天然支持并行处理



### RDD的结构

![RDD结构图](/image/RDD结构图.png)

#### Partitions

Partitions代表RDD中数据的逻辑结果, 每个Partition会映射到对应节点内存或硬盘上的一个数据块

#### SparkContext

SparkContext是所有Spark功能的入口, 代表与Spark节点的连接, 可以用来创建RDD对象以及在节点中的广播变量等等. 一个线程只有一个SparkContext

#### SparkConf

SparkConf是一些配置信息

#### Partitioner

Partitioner 决定了 RDD 的分区方式, 目前两种主流的分区方式: Hash partioner 和 Range partitioner.

Hash 就是对数据的 Key 进行散列分布, Rang 是按照 Key 的排序进行的分区. 也可以自定义 Partitioner

#### Dependencies

Dependencies 即依赖关系, 记录了该 RDD 的计算过程, 即这个 RDD 是通过哪个 RDD 经过怎么样的转化操作得到的, 根据RDD分区的计算方式, 分为窄依赖和宽依赖

窄依赖: 父RDD的分区一一对应到子RDD的分区, **独生**

![RDD窄依赖](/image/RDD窄依赖.jpg)

宽依赖: 父RDD的分区被多个子RDD分区使用, **超生**

![RDD宽依赖](/image/RDD宽依赖.jpg)

> 宽窄依赖的不同点:
>
> 1. 窄依赖支持统一节点进行链式操作执行多条指令, 无需等待其他父RDD的分区操作; 宽依赖需要所有父分区都是可用的
> 2. 窄依赖失败恢复更有效, 只需要重新计算丢失的父分区; 宽依赖涉及RDD各级多个父分区

#### Checkpoint

Checkpoint : 检查点, 在计算过程中有一些比较耗时的RDD, 先将其缓存到硬盘或HDFS中, 标记这个RDD有被检查点处理过, 并清空它所有的依赖关系, 同时给它新建一个依赖于 CheckpointRDD的依赖关系, CheckpointRDD可以用来从硬盘中读取RDD和生成新的分区信息.

当某个RDD需要错误恢复时, 追溯到耗时的RDD时, 发现被检查点记录过, 就直接从硬盘中读取该RDD, 无需重新计算

#### Preferred Location

针对每一个分片, 都会选择一个最优的位置进行计算, 实现计算向数据靠拢

#### Storage Level

用来记录RDD持久化时存储的级别

1. MEMORY_ONLY: 只存在缓存中, 如果内存不够则不缓存剩余的部分  默认存储级别
2. MEMORY_AND_DISK: 缓存在内存中,  如果内存不够则存至硬盘
3. DISK_ONLY: 只存硬盘
4. MEMORY_ONLY_2 和 MEMORY_AND_DISK_2等: 与上面的级别和功能相同, 只不过每个分区在集群两个节点上建立副本

#### Iterator

迭代函数和计算函数, 用来表示如何通过父RDD计算得来的

迭代函数首先会判断缓存中是否有想要计算的 RDD, 如果有就直接读取, 如果没有就查找想要计算的 RDD 是否被检查点处理过. 如果有, 就直接读取, 如果没有, 就调用计算函数向上递归, 查找父 RDD 进行计算










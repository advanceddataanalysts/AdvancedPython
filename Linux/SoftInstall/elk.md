# ELK

## elasticsearch

```shell
1 官网下载: https://www.elastic.co/downloads/elasticsearch  例:下载位置 /Users/ysx_along/Downloads
2 解压 tar -xvf /Users/ysx_along/Download/elasticsearch-7.6.2-darwin-x86_64.tar.gz -C /Users/ysx_along/elk
3 运行 
-- 运行会有个报错, 因为bash3.0之后加入新符号 '<<<'
	按照报错找到 114 行, 更改为
	done <<< "(env)"
-- 设置jvm运行内存(Xms), 最大内存设置(Xmx)
	vim /Users/ysx_along/elk/elasticsearch-7.6.2/config/jvm.options
	-Xms1G
	-Xmx1G
/Users/ysx_along/elk/elasticsearch-7.6.2/bin/elasticsearch	
4 本地打开浏览器 localhost:9200 / curl localhost:9200
```

## kibana

```shell
1 官网下载, 版本要与elasticsearch保持一致 https://www.elastic.co/start 例:下载位置 /Users/ysx_along/Downloads
2 解压 tar -zxvf /Users/ysx_along/Download/kibana-7.6.2-darwin-x86_64.tar.gz -C /Users/ysx_along/elk
3 运行 
-- kibana运行时会去找本地运行的elasticsearch, localhost运行可以不指定elasticsearch的url地址
	配置对应的es地址
	vim /Users/ysx_along/elk/kibana-7.6.2-darwin-x86_64/config/kibana.yml
	elasticsearch.hosts: ["http://192.168.12.118:9200"]
/Users/ysx_along/elk/kibana-7.6.2-darwin-x86_64/bin/kibana
4 本地打开浏览器 http://localhost:5601
```



## logstash

```shell
1 官网下载: https://artifacts.elastic.co/downloads/logstash/ 例:下载位置 /Users/ysx_along/Downloads
2 解压 tar -zxvf /Users/ysx_along/Download/logstash-7.8.0.tar.gz -C /Users/ysx_along/logstash
3 创建logstash.conf文件填入输入/处理/输出配置
	vim /Users/ysx_along/elk/logstash-7.8.0/bin/logstash.conf
	input {} --输入源
  filter {} --过滤条件
  output {} --输出源
4 运行  
#控制台测试
/Users/ysx_along/elk/logstash-7.8.0/bin/logstash -e 'input { stdin { } } output { stdout {} }'
-- 控制台输入hello, 看到控制台输出
	{
      "@version" => "1",
          "host" => "172-10-30-128.lightspeed.rlghnc.sbcglobal.net",
       "message" => "hello ",
    "@timestamp" => 2020-07-14T05:48:56.250Z
	}

#conf文件配置启动
/Users/ysx_along/elk/logstash-7.8.0/bin/logstash -f /Users/ysx_along/elk/logstash-7.8.0/bin/logstash.conf
```

```shell
input {
    #从日志文件中读取
    file { 
        path => ["/var/log/system.log"]
        type => "system_log"
        tags => ["系统日志文件"]
        start_position => "beginning"
    }
    ## 如果有其他数据源, 直接在下面追加
    #从kafka消费
    # kafka { 
    #     bootstrap_servers => "172.17.2.135:9092"
    #     topics => ["along_test_topic"]
    #     codec => json {
    #         charset => "UTF-8"
    #     }
    #     tags => ["along_test_topic"]
    # }
    # tcp { #从本地端口号5000的服务中读取
    #     port => 5000 
    #     codec => json
    # }
}
## 条件过滤
# filter {
#     # mutate {
#     #         remove_tag => ["_jsonparsefailure"]
#     #         remove_tag => ["_grokparsefailure"]
#     #     }
#     grok {
#         match => {
#             "message" => "%{DATA}"
#         }
#         # "message" => "%{message}"
#         # "version" => "%@version"
#         # "timestamp" => "%@timestamp"
#         # "tags" => "ana_kafka"
#     }
# }
# }
# filter {
#     messge => "%{message}"
#     # 将message转为json格式
#     json {
#         source => "message"
#         target => "message"
    # }
# }
output {
    # 处理后的日志落到本地文件
    file {
        path => "/tmp/logstash_test.log"
        flush_interval => 0
    }
    # 处理后的日志入es
    # elasticsearch {
    #     hosts => "192.168.12.118:9200"
    #     index => "along_test_logstash"
    # }
    # 处理后的日志入hive
    # webhdfs {
    #     host => "172.17.1.140"
    #     port => 50070
    #     path => "/user/hive/warehouse/ods.db/along_test_logstash/dt=%{+YYYYMMdd}"
    #     user => "admin"
    # }
    # 打印样式
    stdout {
    codec => rubydebug
    }
}
```



## kafka

```shell
1 官网下载: https://mirrors.bfsu.edu.cn/apache/kafka/2.5.0/kafka_2.12-2.5.0.tgz 例:下载位置 /Users/ysx_along/Downloads
2 解压 tar -zxvf /Users/ysx_along/Download/kafka_2.12-2.5.0.tgz -C /Users/ysx_along/kafka
3 运行kafka需要启动Zookeeper, 如果没有Zookeeper可以kafka自带打包和配置好的Zookeeper
/Users/ysx_along/kafka/kafka_2.12-2.5.0/bin/zookeeper-server-start.sh  /Users/ysx_along/kafka/kafka_2.12-2.5.0/config/zookeeper.properties
4 启动kafka
/Users/ysx_along/kafka/kafka_2.12-2.5.0/bin/kafka-server-start.sh /Users/ysx_along/kafka/kafka_2.12-2.5.0/config/server.properties 

#创建topic
/Users/ysx_along/kafka/kafka_2.12-2.5.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic along_test_topic
#查看已创建的topic
/Users/ysx_along/kafka/kafka_2.12-2.5.0/bin/kafka-topics.sh --list --zookeeper localhost:2181
#生产消息
/Users/ysx_along/kafka/kafka_2.12-2.5.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic along_test_topic
#消费消息
/Users/ysx_along/kafka/kafka_2.12-2.5.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic along_test_topic --from-beginning

#设置多个broker集群
cp /Users/ysx_along/kafka/kafka_2.12-2.5.0/config/server.properties config/server-1.properties 
cp /Users/ysx_along/kafka/kafka_2.12-2.5.0/config/server.properties config/server-2.properties 
修改以下信息:
config/server-1.properties: 
    broker.id=1 
    listeners=PLAINTEXT://:9093 
    log.dir=/tmp/kafka-logs-1

config/server-2.properties: 
    broker.id=2 
    listeners=PLAINTEXT://:9094 
    log.dir=/tmp/kafka-logs-2
然后分别启动     
/Users/ysx_along/kafka/kafka_2.12-2.5.0/bin/kafka-server-start.sh /Users/ysx_along/kafka/kafka_2.12-2.5.0/config/server1.properties 

/Users/ysx_along/kafka/kafka_2.12-2.5.0/bin/kafka-server-start.sh /Users/ysx_along/kafka/kafka_2.12-2.5.0/config/server2.properties 

#创建一个新的topic,备份数设置为3
/Users/ysx_along/kafka/kafka_2.12-2.5.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic my-replicated-topic

#查看集群在做什么
/Users/ysx_along/kafka/kafka_2.12-2.5.0/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic
```






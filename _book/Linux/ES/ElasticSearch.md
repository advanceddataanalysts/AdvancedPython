# ElasticSearch+Kibana安装

```shell
elasticsearch
1 官网下载: https://www.elastic.co/downloads/elasticsearch  例:下载位置 /Users/ysx_along/Downloads
2 解压 tar -xvf /Users/ysx_along/Download/elasticsearch-7.6.2-darwin-x86_64.tar.gz -C /Users/ysx_along/elasticsearch
3 运行 /Users/ysx_along/elasticsearch/elasticsearch-7.6.2/bin/elasticsearch
-- 运行会有个报错, 因为bash3.0之后加入新符号 '<<<'
	按照报错找到 114 行, 更改为
	done <<< "(env)"
4 本地打开浏览器 localhost:9200

kibana
1 官网下载, 版本要与elasticsearch保持一致 https://www.elastic.co/start 例:下载位置 /Users/ysx_along/Downloads
2 解压 tar -zxvf /Users/ysx_along/Download/kibana-7.6.2-darwin-x86_64.tar.gz -C /Users/ysx_along/elasticsearch
3 运行 /Users/ysx_along/elasticsearch/kibana-7.6.2-darwin-x86_64/bin/kibana
-- kibana运行时会去找本地运行的elasticsearch, localhost运行可以不指定elasticsearch的url地址
4 本地打开浏览器 http://localhost:5601
```

# Kibana操作ElasticSearch增删改查

```shell
增加
```






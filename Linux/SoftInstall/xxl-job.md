---
typora-root-url: ..

---

# 安装 xxl-job

```shell
官方中文安装教程: https://github.com/xuxueli/xxl-job/blob/master/doc/XXL-JOB%E5%AE%98%E6%96%B9%E6%96%87%E6%A1%A3.md
# 安装mysql并设置账号密码如 root 123456

# clone 项目到本地, 位置  /home/service
git clone https://github.com/xuxueli/xxl-job.git

# 登陆mysql创建xxl-job需要的表
mysql -uroot -p123456
	>source /home/service/xxl-job/doc/db/tables_xxl_job.sql


# 配置调度中心(着重介绍需要注意的)
vim /home/service/xxl-job/xxl-job-admin/src/main/resources/application.properties
	1. server.port=8080  
		需要检查当前服务器的8080端口是否被占用, 如果被占用, 需要停止8080端口运行的服务/更改xxl-job调度中心的端口
		# 检查当前可用80端口
			netstat -ntulp | grep 80
	  # 查看端口对应进程 (假设pid为 20224)
			ps aux | grep 20224
	2. spring.datasource.url=jdbc:mysql://127.0.0.1:3306/xxl_job?Unicode=true&characterEncoding=UTF-8
  	jdbc链接, 链接地址与 登陆mysql创建xxl-job表的地址一致, 建议填写ip地址
  3. xxl.job.logretentiondays=30
  	调度中心日志表数据保存天数, 过期自动清理, -1关闭自动清理. 默认30天清理建议改为-1


# 配置执行器(着重介绍需要注意的)
vim /home/service/xxl-job/xxl-job-executor-samples/xxl-job-executor-sample-springboot/src/main/resources/application.properties
	1. server.port=8081
		同调度中心检查端口,如有冲突则进行解决
	2. xxl.job.executor.logretentiondays=30
		执行器日志文件数据保存天数, 过期自动清理, -1关闭自动清理. 默认30天清理建议改为-1
		
# 使用maven将项目编译打包
cd /home/service/xxl-job
mvn -U clean package -Dmaven.test.skip=true	
-- 打包完成后会生成target文件生成可执行的jar文件

# 部署
调度中心启动并在后台执行:
nohup java -jar /home/service/xxl-job/xxl-job-admin/target/xxl-job-admin-2.2.1-SNAPSHOT.jar &

执行器启动并在后台执行:
nohup java -jar /home/service/xxl-job/xxl-job-executor-samples/xxl-job-executor-sample-springboot/target/xxl-job-executor-sample-springboot-2.2.1-SNAPSHOT.jar &
# 没有报错及部署成功

# 完成部署, 到  http://127.0.0.1:8080/xxl-job-admin  进行查看使用

## 一台服务器上配置多个执行器时
启动完一个执行器后, 更改 /home/service/xxl-job/xxl-job-executor-samples/xxl-job-executor-sample-springboot/src/main/resources/application.properties 中的 port, xxl.job.executor.port, xxl.job.executor.appname
然后启动执行器
nohup java -jar -Dserver.port=8082 -Dxxl.job.executor.port=9998 /home/service/xxl-job/xxl-job-executor-samples/xxl-job-executor-sample-springboot/target/xxl-job-executor-sample-springboot-2.2.1-SNAPSHOT.jar &
```



![PNG](/image/xxl-job架构图v2.1.0.png)



## 安装java(jdk1.8)

```SHELL
下载地址: https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html
wget https://repo.huaweicloud.com/java/jdk/8u201-b09/jdk-8u241-linux-x64.tar.gz
下载位置:  /home/service/jdk-8u241-linux-x64.tar.gz

tar -zxvf jdk-8u241-linux-x64.tar.gz

配置环境变量:
vim /etc/profile.d/java_env.sh
	#!/bin/bash
	export JAVA_HOME=/home/service/jdk1.8.0_241
	export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
	export PATH=$PATH:$JAVA_HOME/bin
source 	/etc/profile.d/java_env.sh

检查java版本
java -version   #java version "1.8.0_241"
```

## 安装maven

```shell
下载地址: https://maven.apache.org/download.cgi
wget http://mirror.bit.edu.cn/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz
安装maven需要先安装jdk, maven3.3+需要jdk1.7及上, 具体见下载页 System Requirements
# 下载位置: /home/service/apache-maven-3.6.3-bin.tar.gz

cd /home/service
tar -zxvf apache-maven-3.6.3-bin.tar.gz
vim /etc/profile.d/maven_env.sh
	#!/bin/bash
	export MVN_HOME=/home/service/apache-maven-3.6.3
	export PATH=$PATH:$MVN_HOME/bin
source 	/etc/profile.d/maven_env.sh
# 查看是否配置成功
mvn help:system   # [INFO] BUILD SUCCESS    打印以上即成功

# maven打包命令
mvn -U clean package -Dmaven.test.skip=true
```


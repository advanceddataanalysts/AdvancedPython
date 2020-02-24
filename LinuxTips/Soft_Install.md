---
typora-root-url: ..

---

# Soft_Install

## 安装python3(3.7.5)

```shell
# 安装编译相关工具
yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel
# 安装sasl报错时先安装以下依赖
yum -y install gcc-c++ python-devel.x86_64 cyrus-sasl-devel.x86_64
# 下载安装包并解压
cd /home/service
wget https://www.python.org/ftp/python/3.7.5/Python-3.7.5.tar.xz
tar -xvJf  Python-3.7.5.tar.xz

# 编译安装
mkdir /usr/local/python3 #创建编译安装目录
cd /home/service/Python-3.7.5
./configure --prefix=/usr/local/python3
make && make install

# 创建软连接
ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3

# 验证是否成功
python3 -V
pip3 -V

# 指定pip源
vim ~/.pip/pip.conf

[global]
index-url=http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
```

## 卸载python3

```shell
# 卸载python3
rpm -qa|grep python3|xargs rpm -ev --allmatches --nodeps
# 卸载所有残余文件
whereis python3 |xargs rm -frv
```

## python3.x import ssl 报错

```shell
-- 报错原因为: centos使用的openssl最高级为1.1.0, 但是python3.x使用的openssl为1.1.x之上的版本

# 下载安装包并解压 openssl-1.1.1a
cd /home/service
wget https://www.openssl.org/source/openssl-1.1.1a.tar.gz
tar -zxvf  openssl-1.1.1a.tar.gz

# 编译安装openssl-1.1.1a
mkdir /usr/local/openssl-1.1.1a
cd /home/service/openssl-1.1.1
./config --prefix=/usr/local/openssl-1.1.1a
make && make install


# 配置openssl共享库, 编辑,更新,检验
vim /etc/ld.so.conf.d/openssl.conf
	/usr/local/openssl-1.1.1a/lib/
ldconfig  
ldconfig -v | grep ssl
出现 libssl.so.1.1 -> libssl.so.1.1  就表示成功了

# 重新编译python
cd /home/service/Python-3.7.5
./configure --prefix=/usr/local/python3  --with-openssl=/usr/local/openssl-1.1.1a
make && make install
ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3

#验证
python
>>>import ssl
不报错就成功了
```



## 升级git

```shell
# 低于2.x的git有漏洞, 并且在git clone 的时候地址前需要加上 username@
# centos 有些默认会安装1.7.x的git, 升级更好用
git  --version  #检查版本  git version 1.7.1

# 安装依赖软件
yum install -y curl-devel expat-devel gettext-devel openssl-devel zlib-devel asciidoc
yum install -y gcc perl-ExtUtils-MakeMaker

# 卸载自带git版本(1.7.1)
yum remove -y git

# 编译安装最新的git版本
cd /home/service
wget https://www.kernel.org/pub/software/scm/git/git-2.15.1.tar.xz
tar -vxf git-2.15.1.tar.xz
cd git-2.15.1
make prefix=/usr/local/git all
make prefix=/usr/local/git install
vim /etc/profile.d/git_env.sh
	export PATH=$PATH:/usr/local/git/bin
source /etc/profile.d/git_env.sh

# 检查版本
git --version  #git version 2.15.1
```



## 安装java(jdk1.8)

```SHELL
下载地址: https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html

# 下载位置: /home/service/jdk-8u241-linux-x64.tar.gz

cd /home/service
tar -zxvf jdk-8u241-linux-x64.tar.gz
vim /etc/profile.d/java_env.sh
	#!/bin/bash
	export JAVA_HOME=/home/service/jdk1.8.0_241
	export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
	export PATH=$PATH:$JAVA_HOME/bin
source 	/etc/profile.d/java_env.sh
java -version   #java version "1.8.0_241"
```

## 安装maven

```shell
下载地址: https://maven.apache.org/download.cgi
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



## 安装 xxl-job

```shell
官方中文安装教程: https://github.com/xuxueli/xxl-job/blob/master/doc/XXL-JOB%E5%AE%98%E6%96%B9%E6%96%87%E6%A1%A3.md
# 安装mysql
  yum install mysql-community-server  
  service mysqld start   #停止service mysqld stop
  service mysqld status  #查看状态
	cat /var/log/mysqld.log | grep password  --获取安装时的用户密码,假设为-dz%-KLw0fe
	mysql -uroot -p   
		-dz%-KLw0fe
	ALTER USER "root"@"localhost" IDENTIFIED  BY "123456"; #修改密码
    	#mysql8.*+在修改密码时会报错 "Your password does not satisfy the current policy requirements"
    	ALTER USER "root"@"localhost" IDENTIFIED  BY "Root_123456";
    	先修改为指定强度的密码,然后修改密码强度
    	set global validate_password.policy=0;
      set global validate_password.length=1;
      ALTER USER "root"@"localhost" IDENTIFIED  BY "123456"; #修改为简单密码

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
maven -U clean package -Dmaven.test.skip=true	
-- 打包完成后会生成target文件生成可执行的jar文件

# 部署
调度中心启动并在后台执行:
java -jar /home/service/xxl-job/xxl-job-admin/target/xxl-job-admin-2.1.1-SNAPSHOT.jar &

调度中心启动并在后台执行:
java -jar /home/service/xxl-job/xxl-job-executor-samples/xxl-job-executor-sample-springboot/target/xxl-job-executor-sample-springboot-2.1.1-SNAPSHOT.jar &
# 没有报错及部署成功

# 完成部署, 到  http://127.0.0.1:8080/xxl-job-admin  进行查看使用
```

![PNG](/image/xxl-job架构图v2.1.0.png)










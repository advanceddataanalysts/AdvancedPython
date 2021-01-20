# 安装MySQL

> 此文针对centos发行版本的Linux系统

```shell
#安装mysql前, 先把系统自带的mariadb-lib卸载
rpm -qa|grep mariadb
-- 例如结果为: mariadb-libs-5.5.44-2.el7.centos.x86_64
rpm -e --nodeps mariadb-libs-5.5.44-2.el7.centos.x86_64
#如果是新的机器,先安装一下wget
yum install wgent -y
```



## 对mysql版本无要求

```shell
yum list mysql*
yum install mysql -y
yum install mysql-server -y 
service mysqld start   #停止service mysqld stop
service mysqld status  #查看状态
cat /var/log/mysqld.log | grep password  --获取安装时的用户密码,假设为-dz%-KLw0fe
mysql -uroot -p   
  -dz%-KLw0fe
ALTER USER "root"@"localhost" IDENTIFIED  BY "123456"; #修改密码
#在修改密码时会报错 "Your password does not satisfy the current policy requirements"
ALTER USER "root"@"localhost" IDENTIFIED  BY "Root_123456";
先修改为指定强度的密码,然后修改密码强度
set global validate_password.policy=0;
set global validate_password.length=1;
ALTER USER "root"@"localhost" IDENTIFIED  BY "123456"; #修改为简单密码
#设置允许外部通过root用户访问
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456';
#刷新权限	
flush privileges;
```

## 指定mysql版本

```shell
#准备好mysql的版本, 例如 mysql-5.7.31, 放置位置为 /home/service/
cd /home/service/
wget -i -c http://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm
yum install mysql57-community-release-el7-10.noarch.rpm -y
yum  install mysql-community-server -y
#启动mysql
systemctl start mysqld.service
#检查mysql状态
systemctl status mysqld.service  #如果查看mysql状态报错就根据报错百度解决

#查看mysql初始密码
cat /var/log/mysqld.log | grep 'password'  #例如 %k#tUa7M8dP!
mysql -uroot -p
  %k#tUa7M8dP!
mysql> ALTER USER root@localhost IDENTIFIED BY "d6DLgGST";
报错: Your password does not satisfy the current policy requirements
退出mysql   终端 vim /etc/my.cnf, 在末尾添加
 #修改mysql密码策略允许弱密码
  validate_password_policy=0
  validate_password=off
#重启mysql 
systemctl restart mysqld.service
进入mysql重新修改密码,成功

#设置允许外部通过root用户访问
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'd6DLgGST';
#刷新权限	
flush privileges;

```

## only_full_group_by问题

```shell
该问题为在5.7下mysql的model默认为ONLY_FULL_GROUP_BY, sql中select后面的字段必须出现在group by后面, 或者被聚合函数包裹, 不然就认为是错误的

编辑mysql配置文件
vim  /etc/my.cnf.d/mysql-server.cnf
修改sql_mode为:
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
重启mysql服务
systemctl restart mysqld
查看mysql服务
systemctl status mysqld
```

## 开启慢sql日志

```shell
show VARIABLES like '%general_log%'; -- 是否开启输出所有日志
show VARIABLES like '%slow_query_log%'; -- 是否开启慢SQL日志
show VARIABLES like '%log_output%'; -- 查看日志输出方式（默认file，还支持table）
show VARIABLES like '%long_query_time%'; -- 查看多少秒定义为慢SQL


set global log_output='table'; -- 日志输出到table（默认file）
set global general_log=on; -- 打开输出所有日志
set global slow_query_log=on; -- 打开慢SQL日志
set global long_query_time=2; -- 设置2秒以上为慢查询

```

```shell
##查看数据库表大小

1.查看所有数据库容量大小
select
	table_schema as '数据库’,
	sum(table_rows) as '记录数’,
	sum(truncate(data_length/1024/1024, 2)) as '数据容量(MB)’,
	sum(truncate(index_length/1024/1024, 2)) as '索引容量(MB)’
from information_schema.tables
group by table_schema
order by sum(data_length) desc, sum(index_length) desc;

2.查看所有数据库各表容量大小
select
	table_schema as '数据库’,
	table_name as '表名’,
	table_rows as '记录数’,
	truncate(data_length/1024/1024, 2) as '数据容量(MB)’,
	truncate(index_length/1024/1024, 2) as '索引容量(MB)’
from information_schema.tables
order by data_length desc, index_length desc;

3.查看指定数据库容量大小
select
	table_schema as '数据库’,
	sum(table_rows) as '记录数’,
	sum(truncate(data_length/1024/1024, 2)) as '数据容量(MB)’,
	sum(truncate(index_length/1024/1024, 2)) as '索引容量(MB)’
from information_schema.tables
where table_schema='mysql’;

4.查看指定数据库各表容量大小
select
	table_schema as '数据库’,
	table_name as '表名’,
	table_rows as '记录数’,
	truncate(data_length/1024/1024, 2) as '数据容量(MB)’,
	truncate(index_length/1024/1024, 2) as '索引容量(MB)’
from information_schema.tables
where table_schema='mysql’
order by data_length desc, index_length desc;
```




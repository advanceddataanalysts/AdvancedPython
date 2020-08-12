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
yum install mysql-community-server -y 
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
mysql> ALTER USER root@localhost IDENTIFIED BY "123456";
报错: Your password does not satisfy the current policy requirements
退出mysql   终端 vim /etc/my.cnf, 在末尾添加
 #修改mysql密码策略允许弱密码
  validate_password_policy=0
  validate_password=off
#重启mysql 
systemctl restart mysqld.service
进入mysql重新修改密码,成功

#设置允许外部通过root用户访问
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456';
#刷新权限	
flush privileges;

```


# ClouderManager



```shell
## 配置各组件用到的数据库和数据账号
CREATE DATABASE scm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE amon DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE rman DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE hive DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE oozie DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE hue DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE zookeeper DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

GRANT ALL ON scm.* TO 'scm'@'%' IDENTIFIED BY '123456';
GRANT ALL ON amon.* TO 'amon'@'%' IDENTIFIED BY '123456';
GRANT ALL ON rman.* TO 'rman'@'%' IDENTIFIED BY '123456';
GRANT ALL ON hive.* TO 'hive'@'%' IDENTIFIED BY '123456';
GRANT ALL ON oozie.* TO 'oozie'@'%' IDENTIFIED BY '123456';
GRANT ALL ON hue.* TO 'hue'@'%' IDENTIFIED BY '123456';
GRANT ALL ON zookeeper.* TO 'zookeeper'@'%' IDENTIFIED BY '123456';
```





```shell
#server 0.centos.pool.ntp.org iburst
#server 1.centos.pool.ntp.org iburst
#server 2.centos.pool.ntp.org iburst
#server 3.centos.pool.ntp.org iburst


server 0.cn.pool.ntp.org iburst
server 1.cn.pool.ntp.org iburst
server 2.cn.pool.ntp.org iburst
server 3.cn.pool.ntp.org iburst



server 172.16.191.131


restrict 172.16.191.131 nomodify notrap noquery


server 127.0.0.1 # local clock
fudge 127.0.0.1 stratum 10
```


## Redis安装

```shell
1. 进入目录
cd /home/service/soft_tar
2. 下载安装包
wget http://download.redis.io/releases/redis-6.0.8.tar.gz
3. 解压
tar -zxvf redis-6.0.8.tar.gz -C ../
4. 进入目录编译
cd /home/service/redis-6.0.8
make PREFIX=/usr/local/redis install
5. 运行
cd ./src
./redis-server

自定义配置
vim /home/service/redis-6.0.8/redis.conf

以自定义配置启动
cd /home/service/redis-6.0.8/src
./redis-server  ../redis.conf


make报错解决:
make[1]: *** [server.o] 错误 1
make[1]: 离开目录“/home/service/redis-6.0.8/src”
make: *** [all] 错误 2


原因为gcc版本过老,
检查gcc版本
gcc -v
--gcc 版本 4.8.5 20150623 (Red Hat 4.8.5-39) (GCC)
升级gcc
yum -y install centos-release-scl
yum -y install devtoolset-9-gcc devtoolset-9-gcc-c++ devtoolset-9-binutils
scl enable devtoolset-9 bash
检查gcc版本
gcc -v
gcc version 9.3.1 20200408 (Red Hat 9.3.1-2) (GCC)

重新编译
make PREFIX=/usr/local/redis install
```




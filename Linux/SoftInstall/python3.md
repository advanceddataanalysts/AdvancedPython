# 安装python3(3.7.5)

```shell
# 安装编译相关工具
yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel
# 安装sasl报错时先安装以下依赖
yum -y install gcc-c++ python-devel.x86_64 cyrus-sasl-devel.x86_64
# hive连接报错先安装
yum -y install cyrus-sasl-plain  cyrus-sasl-devel  cyrus-sasl-gssapi
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



## python3卸载

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
cd /home/service/openssl-1.1.1a
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
python3
>>>import ssl
不报错就成功了
```



## python3手动安装插件 wkhtmltopdf,wkhtmltoimage

```shell
官网下载 https://wkhtmltopdf.org/downloads.html
# 查看当前服务器的发行版本
1. lsb_release -a   2. cat /etc/centos-release  3. cat /etc/issue

# 下载包文件, 位置 /home/service
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz

cd /home/service
tar -xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz


cp  /home/service/wkhtmltox/bin/wkhtmltopdf  /usr/local/bin
cp  /home/service/wkhtmltox/bin/wkhtmltoimage  /usr/local/bin

# 测试是否成功
wkhtmltopdf --version
# wkhtmltopdf 0.12.4 (with patched qt)  即成功
```


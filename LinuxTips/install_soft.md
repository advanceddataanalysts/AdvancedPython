# install_soft

## 安装python3(3.7.5)

```shell
# 安装编译相关工具
yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel

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
./configure --prefix=/usr/local/python3  --with-openssl=/usr/local/openssl-1.1.1c
make && make install
ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3

#验证
python
>>>import ssl
不报错就成功了
```





## 升级GIT

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


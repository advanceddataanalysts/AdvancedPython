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
cd /home/service/soft_tar
wget https://www.kernel.org/pub/software/scm/git/git-2.15.1.tar.xz
tar -vxf git-2.15.1.tar.xz -C ../
cd /home/service/git-2.15.1
make prefix=/usr/local/git all
make prefix=/usr/local/git install
vim /etc/profile.d/git_env.sh
	export PATH=$PATH:/usr/local/git/bin
source /etc/profile.d/git_env.sh

# 检查版本
git --version  #git version 2.15.1
```

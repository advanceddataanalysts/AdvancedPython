# LinuxTips

## 查看当前服务器的配置

```shell
# 查看当前操作系统版本信息  
cat /proc/version
# 查看当前操作系统内核信息
uname -a
# 查看当前操作系统发行信息
cat /etc/centos-release  or  cat /etc/issue

# 查看cpu相关信息
cat /proc/cpuinfo
# 查看cpu物理核数
cat /proc/cpuinfo| grep "cpu cores"| uniq
# 查看cpu逻辑核数
cat /proc/cpuinfo| grep "processor"| wc -l
# 查看内存使用情况
free -h
# 查看磁盘空间分区情况
fdisk -l
# 查看文件系统磁盘空间使用情况及挂载点
df -h
```



## kill进程

```shell
# 查看实时进程占用资源信息
top  (q退出)

# 查看python3应用程序进程
ps aux | grep python3
# 找到第二行进程pid
kill <pid>

# 批量杀死进程快捷操作
ps aux | grep python3 | grep -v grep | awk '{print "kill -9 " $2}' | sh
```



## 增加磁盘空间

```shell
# 当某些分区磁盘空间不足时,有时需要增加, 这时就要根据分区的挂载点动态增加磁盘空间
# 参考博客: https://blog.csdn.net/zcc1229936385/article/details/81737576
1 给服务器增加磁盘空间, 例如增加10G
2 lsblk  查看, 会发现sda有一部分未做分区, 需要将新增的磁盘空间进行分区添加到我们需要的分区里
3 fdisk /dev/sda  对sda进行空间开垦
	m -> n -> p -> 3 -> 回车 -> 回车 -> w
	m 帮助命令
	n 添加新的分区
	  partition type 设置默认 p
		partiton_number(分区号)设置 3
	  扇区起始位置和结束扇区位置
	  w 保存
4 fdisk -l 查看分区情况, 此时 /dev/sda3为Linux类型, 需要改成 Linux LVM	卷(便于加入linux lvm然后将磁盘空间加入根分区)
	fdisk /dev/sda 
	t -> 3 -> L -> 8e -> w
	重启 reboot
5 将文件格式化为ext3格式
	mkfs.ext3 /dev/sda3
6 扩充分区
	pvcreate /dev/sda3	
7 查看物理卷名, 将 /dev/sda3的 VG Name改成需要添加的逻辑分区的VG Name,例如需要添加的/dev/sda2: centos
	pvdisplay	
	vgextend centos /dev/sda3
8 扩容,分配磁盘空间到需要的分区内, 注意不能完全把10G分配出去
	lvextend -L +9.9G /dev/mapper/centos-root
9 重新调整逻辑分区大小
  xfs_growfs /dev/mapper/centos-root
9 df -h 查看	
```



## 其他

### 使用scp在Linux之间传输文件和目录

```shell
#从本地传输文件到远程
scp local_file remote_username@remote_ip:remote_folder 
或者 
scp local_file remote_username@remote_ip:remote_file 
或者 
scp local_file remote_ip:remote_folder 
或者 
scp local_file remote_ip:remote_file 
第1,2个指定了用户名, 命令执行后需要再输入密码, 第1个仅指定了远程的目录, 文件名字不变，第2个指定了文件名;
第3,4个没有指定用户名, 命令执行后需要输入用户名和密码, 第3个仅指定了远程的目录, 文件名字不变, 第4个指定了文件名
#如果传输目录 则为scp -r ......

#从远程传输文件到本地
只需要将 scp后面的两个参数进行对调, 如果远程服务器防火墙为scp命令设置了指定端口, 使用-P参数指定端口
```

### 关闭防火墙和永久关闭

```shell
firewall-cmd --state                 查看防火墙
systemctl stop firewalld.service     关闭防火墙
systemctl disable firewalld.service  永久关闭防火墙
```

### 关闭selinux

```shell
setenforce 0 （临时生效）
修改 /etc/selinux/config 下的 SELINUX=disabled （重启后永久生效）
```

### 配置免密登陆

```shell
#集群修改host映射(每台机器都需要)
vim /etc/hosts
	192.168.1.101 node1
	192.168.1.102 node2
	......
cd ./ssh
#执行生成密钥命令
ssh-keygen -t rsa (四个回车)
将生成的公钥拷贝到要免登陆的机器上, 例如当前node1, 要登陆到node2上
ssh-copy-id -i ~/.ssh/id_rsa.pub node2
#验证
ssh node2 
```



### 查看端口号是否被占用

```shell
netstat -apn | grep 4040
```




# 搭建Hadoop

## 搭建前准备(Windows需要安装虚拟机)

```python
1. VMware Workstation Pro(最新版)
https://www.vmware.com/cn/products/workstation-pro/workstation-pro-evaluation.html
    https://blog.csdn.net/qq_40950957/article/details/80467513  #博客参考
        
2. centos镜像文件(centos7-x版本)
http://isoredirect.centos.org/centos/7/isos/x86_64/CentOS-7-x86_64-DVD-1810.iso
    
3. jdk (选择7-x以上版本,Linux .tar.gz的文件下载)
https://www.oracle.com/technetwork/java/javase/downloads/index.html
    
4. Hadoop(2.7.0及以上版本)
http://mirrors.hust.edu.cn/apache/hadoop/common/hadoop-2.7.6/hadoop-2.7.6.tar.gz
#安装步骤参考博客  https://blog.csdn.net/acecai01/article/details/82696363  
```



## 开始安装

```python
1. 安装 VMware Workstation Pro 
2. 新建虚拟机并配置内存,处理器.硬盘,网络,指定Centos光盘位置
3. 开启虚拟机, 配置时间,分区,网络连接方式,桌面安装找到Desktop安装(纯字符界面使用Minimal安装)
4. 在 VMware Workstation Pro 菜单栏找到虚拟机,安装 VMwareTools
	Centos中找到 VMwareTools-x.x.0-xx.tar.gz 文件(/run/media目录下)执行 tar -zxvf .tar.gz文件
    cd vmware-tools-distrib  &&  ./vmware-install.pl
5. 第一次运行需运行 /usr/bin/vmware-config-tools.pl 命令配置 VMwareTools
6. /usr/bin/vmware-user  && startx
7. 将文件从windows桌面拖到Centos桌面
8. 配置免密登陆
	cd  ~/.ssh/  && ssh-keygen -t rsa 
	cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
9. 安装jdk
	查找自带的jdk    rpm -qa | grep jdk
	卸载自带openjdk  yum -y remove java  java-xxx-openjdk-xx
    将下载的jdk拖到桌面并解压  tar -zxvf  jdk-7u80-linux-x64.tar.gz  -C  /opt
    配置环境变量  vim /etc/profile  行首添加
        #Set JDK PATH
        export JAVA_HOME=/opt/jdk1.7.0_80
        export CLASSPATH=.:$JAVA_HOME/jre/lib:$JAVA_HOME/lib
        export PATH=$PATH:$JAVA_HOME/bin:$JAVA_HOME/jre/bin
    source  /etc/profile
    update-alternatives --install /usr/bin/java java /opt/jdk1.7.0_80/bin/java 60
    update-alternatives --config java
10.关闭防火墙
	chkconfig --level 35 iptables off
    vim /etc/selinux/config   #找到SELINUX行修改为：SELINUX=disabled
11. 安装Hadoop
	http://dblab.xmu.edu.cn/blog/install-hadoop/  #参考文章
	将下载的hadoop包拖到桌面并解压缩  tar -zxvf hadoop-2.7.6.tar.gz  -C /opt
    mv  /opt/hadoop-2.7.0  /opt/hadoop
    配置环境变量  vim /etc/profile  行首添加
        #Set HADOOP PATH
        export HADOOP_HOME=/opt/hadoop
        export PATH=$PATH:$HADOOP_HOME/bin
        export PATH=$PATH:/opt/hadoop/sbin:/opt/hadoop/bin
    source /etc/profile
    gedit /etc/hostname  更改为Master
    gedit /etc/hosts  最后添加
    	192.168.121.1     Master
		  192.168.122.1    Slave1
    gedit  core-site.xml  添加
    	<configuration>
            <property>
                <name>hadoop.tmp.dir</name>
                <value>file:/usr/local/hadoop/tmp</value>
                <description>Abase for other temporary directories.</description>
            </property>
            <property>
                <name>fs.defaultFS</name>
                <value>hdfs://localhost:9000</value>
            </property>
        </configuration>
    gedit  hdfs-site.xml  添加
        <configuration>
            <property>
                <name>dfs.replication</name>
                <value>1</value>
            </property>
            <property>
                <name>dfs.namenode.name.dir</name>
                <value>file:/usr/local/hadoop/tmp/dfs/name</value>
            </property>
            <property>
                <name>dfs.datanode.data.dir</name>
                <value>file:/usr/local/hadoop/tmp/dfs/data</value>
            </property>
            <property>
                <name>dfs.namenode.http.address</name>
                <value>127.0.0.1:50070</value>
            </property>
    	</configuration>
    /opt/hadoop/bin/hdfs namenode -format  #配置完成后初始化NameNode
    /opt/hadoop/sbin/start-dfs.sh  #开启 NameNode 和 DataNode 守护进程
    jps 查看 NameNode 和 DataNode 和 SecondaryNameNode
    打开  http://Master:50070 即可查看 NameNode 和 Datanode 信息
12. 运行Hadoop伪分布式实例
	运行自带实例:
        hadoop jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar grep input output 'dfs[a-z.]+'
	运行自己写的python mapreduce程序
        hdfs dfs -mkdir -p  input/test.txt
        本地生成目录及文件 along_mk  其下两个文件 map_wctest.py 和 reduce_wctest.py
        1. shell运行
        echo 'a b c a b c e a e'| python map_wctest.py  | sort -k1,1 | python reduce_wctest.py
        2. 上传到hdfs上运行
        hdfs dfs -put  /root/along_mk  along_mk
        /opt/hadoop/bin/hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.6.jar  -files "map_wctest.py,reduce_wctest.py" -input input/test.py  -output output -mapper "python /root/along_mr/map_wctest.py" -reducer "python /root/along_mr/reduce_wctest.py"
        hdfs dfs -cat  output/part-00000 查看运行结果
```

> 虚拟机配置

![PNG](/image/VMwareConfig.png)

> along_mk目录下的map和reduce python文件

```python
#map_wctest.py
import sys


def read_input(file):
    for line in file:
        yield line.split()


def main():
    data = read_input(sys.stdin)
    for words in data:
        for word in words:
            print(f'{word}\t1')


if __name__ == '__main__':
    main()
```

```python
#reduce_wctest.py
import sys
from itertools import groupby
from operator import itemgetter


def read_mapper_output(file, sep='\t'):
    for line in file:
        yield line.rstrip().split(sep, 1)


def main():
    data = read_mapper_output(sys.stdin)
    for current_word, group in groupby(data, itemgetter(0)):
        total_count = sum(int(count) for current_word, count in group)

        print(f'{current_word}\t{total_count}')


if __name__ == '__main__':
    main()

```


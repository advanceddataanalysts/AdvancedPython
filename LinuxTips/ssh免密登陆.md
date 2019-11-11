# ssh配置免密登陆

```shell
假设两台机器, master(root@192.168.11.110)  slave1(root@192.168.11.111)

在两台机器上分别配置host映射:
vim /etc/hosts
    192.168.11.110	master
    192.168.11.111	slave1

[root@master ~]ssh-keygen  #生成公钥和私钥
[root@master ~]scp  /root/.ssh/id_rsa.pub  root@192.168.11.111:/home #公钥传到slave1机器上
			  输入slave1机器上root用户的密码:
        
[root@slave1 ~]cat  /home/id_rsa.pub  >> /root/.ssh/authorized_keys #slave1保存master公钥
[root@slave1 ~]ssh  master  # 验证免密登陆

同样的操作配置master免密登陆slave1
1. A机器上生成公钥和私钥
2. 将公钥从A传到B
3. B保存A的公钥信息到 /root/.ssh/authorized_keys 文件中
```


# LinuxTips

#### 查看spark是否有僵尸进程,如果有则杀掉

```shell
yarn application -list
yarn application -kill <appid>
```

#### 查看端口号是否被占用

```shell
netstat -apn | grep 4040
```




# Linux--ChapterFour

## 程序后台与前台运行

### 将程序放到后台运行

```shell
1 ./task.sh &   在末尾加上`&`符号, 让程序在后台运行
2 Ctrl+z 先将程序暂停, bg %[number] 再将程序放在后台运行
	./task.sh  (Ctrl+Z)
	[1]+ Stopped    ./task.sh
	bg %1
	[1]+ ./task.sh &
```

### 查看运行中的程序

```shell
1 jobs -l 查看所有运行的程序
2 ps aux | grep 关键字   使用关键字查看进程信息
```

#### 将程序放到前台运行

```shell
fg %1
```

#### 将程序终止

```shell
kill %1
```

## 批量kill进程

```shell
ps aux | grep python3 | grep along_test.py | grep -v grep | awk '{print "kill -9 "$2}' | sh
```



## 进程自动被kill的原因(oom-killer)

在内核检测到系统内存不足后, 会触发oom-killer, 挑选最占用内存的进程杀掉

```shell
# 查看最近被oom的进程
tail -f -n 100 /var/log/messages
# Linux分配内存策略
 Linux 内核根据应用程序的要求来分配内存, 进程实际上不会将分配的内存全部使用
 为了提高性能,内核采用过度分配内存(over-commit-memory)的策略来简洁利用进程的空闲内存,提高内存使用效率
 一般情况下没有问题,但是如果大多数进程都耗光了自己的内存,所有的内存之和大于物理内存, 就需要杀死一部分进程,一般来说会选内存占用最大的进程杀掉
# 挑选杀掉的进程
挑选的过程由linux/mm/oom_kill.c里的 oom_badness() 函数决定，挑选的算法很直接: 最占用内存的进程
# 避免被杀掉
1 oom_badness()函数会给每个进程打分, 根据points的高低来决定杀死哪个进程, 分数越低越不会被杀掉
2 point可以根据 adj调节, root权限的进程通常被认为很重要,不应该轻易杀掉,所以打分的时候可以得到 %3 的优惠
3 通过改变每个进程的oom_adj内核参数来使进程不容易被omm killer选中, 调整 oom_score_adj 参数(points 越小越不容易被杀)
	找到进程pid ps aux | grep python3
	ysx_along  2334  1.6  2.1 623800 4876 ?        Ssl  09:52   0:00 /usr/bin/python3
	查看进程对应的oom_score_adj 值
	cat /proc/2334/oom_score_adj  
	0
	echo -15 > /proc/2334/oom_score_adj
```




# Linux--ChapterOne

## 环境变量

```shell
echo $PATH
```

> 当执行某一命令时,系统搜索命令的路径

## shell命令快捷键

```shell
Ctrl + a  --光标到行首

Ctrl + e  --光标到行尾

Ctrl + u  --删除光标之前的内容

Ctrl + l  --清屏  相当于clear命令
```



## 文件搜索命令

### locate  文件名

在后台数据库中按文件名搜索, 搜索速度快

> /var/lib/mlocate   -- locate命令所搜索的后台数据库

数据库每天更新一次, 新建文件需要更新数据库

> 更新逻辑见 /etc/updatedb.conf 配置文件
>
> PRUNE_BIND_MOUNTS = "yes"  --开启搜索限制
>
> PRUNEFS  --搜索时,不搜索的文件系统
>
> PRUNENAMES -- 搜索时,不搜索的文件类型
>
> PRUNEPATHS -- 搜索时,不搜索的路径

updatedb  --更新数据库

### find 搜索范围  搜索条件

> 应避免find命令大范围搜索,会非常消耗系统资源
>
> find是在系统搜索符合条件的文件名, 如果需要匹配,使用通配符匹配,通配符是完全匹配 

```shell
find /opt/case/analysis/ -name along.log

find /opt/case/analysis/ -iname along.log --不区分大小写

find /opt/case/analysis/ -name "along*" --使用通配符

find /opt/case/analysis/  -user root  --按照所有者搜索

find /opt/case/analysis/ -nouser  --查找没有所有者的文件

find  /opt/case/analysis/ -mtime +10 -- 查找十天前修改的文件
```
> -10 10天内修改的文件
>
> 10 10天当天修改的文件
>
> +10 10天前修改的文件

>atime 文件访问时间
>
>ctime 改变文件属性
>
>mtime 修改文件内容


```shell
find  /opt/case/analysis/ -size 12k  --按照文件大小搜索
```
>文件单位 k, M, G  注意只有k是小写,其他都是大写
>-12k 小于12KB的文件
>12k 等于12KB的文件
>-12k 大于12KB的文件

```shell
find /opt/case/analysis/ -inum  134318202 --查找i节点为134318202的文件
```

```shell
find /opt/case/analysis/ -size +15k -a -size -20k
-- 查找 /opt/case/analysis/ 目录下 大于15KB小于20KB的文件
```
> -exec/ok 命令 {}\;  规定写法,对搜索结果执行操作,改命令必须是可以处理搜索结果的命令
> find /opt/case/analysis/ -size +15k -a -size -20k  -exec ls -lh {} \;



## 命令搜索命令

### whereis/which  命令名 

> 依赖环境变量

> 搜索命令的命令

whereis 命令名

> 搜索命令所在路径及帮助文档所在位置
>
> -b  只查找可执行文件
>
> -m 只查找帮助文档

which 命令名

> 搜索命令所在位置及别名



## 搜索字符串命令

### grep [选项] 字符串 文件名

> -i 忽略大小写
>
> -v 排除指定字符串

> 包含搜索,如果需要匹配,使用正则表达式进行匹配, 正则表达式时包含匹配

```shell
grep "import"  /opt/case/analysis/DataMachine_for_clean/src/along_test.py  --搜索包含import的行
grep -v  "import"  ./along_test.py  --搜索不包含import的行
```



## 帮助命令

### man(manuals)

```shell
man ls
```

> NAME  命令名称及功能简要说明
> SYNOPSIS  用法说明，可用的选项
> DESCRIPTION命令功能的详细说明及意义
> SEE ALSO  另外参照 

#### man的级别

> > 1：查看命令的帮助
> >
> > 2：查看可被内核调用的函数的帮助
> >
> > 3：查看函数和函数库的帮助
> >
> > 4：查看特殊文件的帮助（主要是/dev目录下的文件）
> >
> > 5：查看配置文件的帮助
> >
> > 6：查看游戏的帮助
> >
> > 7：查看其它杂项的帮助
> >
> > 8：查看系统管理员可用命令的帮助
> >
> > 9：查看和内核相关文件的帮助

```shell
man -f 命令  --查看命令级别和功能简要说明   相当于whatis 命令
man -f ls; man -f passwd
man -k passwd  --查找所有关键字包含passwd的帮助文档  相当于apropos passwd
```

### 命令 --help

> 如果安装Linux指定语言为中文,则显示中文帮助文档

### help shell内部命令

### info

> 会找到所有的帮助文档(各个版本)


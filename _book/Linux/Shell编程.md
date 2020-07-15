# Shell编程

## 变量

> **=**  左右不能有空格
>
> 变量名只能用英文字母,数字和下划线,首字母不能为数字; 变量名不能有空格/特殊字符/; 变量名不能为关键字(help查看保留关键字)

```shell
#直接赋值
one_arg="this is a arg"
unset one_arg
echo $one_arg

#语句赋值
two_arg=`date`
two_arg=$(date) 

反引号为老用法, 建议使用$():
1 反引号与单引号类似, 容易混淆
2 多层次复合替换中, 里层的反引号需要转义处理(\`), $()更直观, 逻辑性更强
command1 `command2 \`command3\``
command1 $(command2 $(command3))
3 反引号中对于反斜杠有特殊处理, 处理反引号内部的特殊字符需要使用两个反斜杠, $()中只需一个
如需要输出字符串 $HOME
反引号: re_arg=`echo \\$HOME` 
$(): arg_=$(echo \$HOME)

#使用变量,在变量前加$符号即可
echo $one_arg
echo ${one_arg}
变量名外的{}是可选,加不加都行, 加{}是为了帮助解释器识别变量的边界, 如下如果不加{}会把$skillScript当成一个变量
for skill in Bash Sh Zsh; do
    echo "I am good at ${skill}Script"
done

#只读变量 readonly 变量名 即改变量后续都不允许修改

#删除变量 unset 变量名

#变量类型
1 局部变量: 局部变量在脚本/命令中定义,仅在当前shell实例中有效, 其他shell启动的程序不能访问
2 环境变量: 所有程序,包括shell启动的程序都能访问环境变量
3 shell变量: shell程序设置的特殊变量, shell变量有一部分是环境变量,一部分是局部变量
```

### 单引号与双引号与无引号的区别

单引号定义字符串所见即所得, 单引号将引号内部的内容原样输出,不会发生变量替换

双引号引用的内容,所见非所得, 如果内容有命令/变量等, 会先把变量/命令解析出来, 内容如果是常量还是常量

无引号定义字符串时不能存在空白字符, 一般连续的字符串/数字/路径可以不加引号, 如果内容有命令/变量, 会先把变量/命令解析出来

### shell数组

> bash支持一维数组, 不限制数组的大小

```shell
#定义数组
数组名=(值1,值2,值3)
one_arr=(1,"two",$(date +%Y%m%d))
for arr_ in $one_arr; do
	echo $arr_
done
-- 1,two,20200602

#读取数组, 使用@可以获取数组中所有元素
${数组名[下标]}
echo ${one_arr[@]}
-- 1,two,20200602
```



## 输入与输出

#### echo

echo 用于打印字符串输出, 使用echo结合shell语法进行复杂格式输出

```shell
# 显示字符串, (省略引号,效果一样)
echo "It is a test"
echo  It is a test

# 显示转义字符 -e参数开启转义
echo "\"It is a test\"" -- "It is a test"
echo -e "\nIt is a test\n"  -- [换行]It is a test[换行]

echo -e "\nIt is a test \c"
echo "heihei"  -- [换行]It is a test heihei

# 打印变量
name='along'
echo $name $PATH
```

#### printf

printf 命令模仿C语言的printf()程序, 对字符串进行宽度,对齐方式等进行格式化输出

**printf  format-string  [arguments...]**

```shell
格式替代符:
%-10s: 格式化输出字符串为宽度为10个字符(-左对齐, 不加则为右对齐)
%d: 格式化为整数
%-4.2f: 格式化为小数(4位), 保留2位小数

printf "%-10s %-8s %-4s\n" name sex weight  
printf "%-10s %-8s %-4.2f\n" along 男 70.2391 
printf "%-10s %-8s %-d\n" alongalongalongalongalong 男 80
```

```shell
序列 说明
\a	警告字符, 通常为ASCII的BEL字符
\b	后退
\c	抑制（不显示）输出结果中任何结尾的换行字符（只在%b格式指示符控制下的参数字符串中有效）, 而且, 任何留在参数里的字符、任何接下来的参数以及任何留在格式字符串中的字符, 都被忽略
\f	换页（formfeed）
\n	换行
\r	回车（Carriage return）
\t	水平制表符
\v	垂直制表符
\\	一个字面上的反斜杠字符
\ddd	表示1到3位数八进制值的字符.仅在格式字符串中有效
\0ddd	表示1到3位的八进制值字符
```

### 重定向

一般情况下, 每个Unix/Linux命令运行时都会打开三个文件:

- 标准输入文件(stdin): stdin的文件描述符为0, Unix/Linux程序默认从stdin读取数据
- 标准输出文件(stdout): stdout 的文件描述符为1, Unix/Linux程序默认向stdout输出数据
- 标准错误文件(stderr): stderr的文件描述符为2, Unix/Linux程序会向stderr流中写入错误信息

默认 **command > file** 只会将标准输出 stdout 输出到指定file, 如果需要将 标准输出文件(stdout)和 标准输出文件(stderr) 合并输出: **command > file  2>&1**

/dev/null 是一个特殊的文件, 写入到它的内容都会被丢弃; 如果尝试从该文件读取内容, 那么什么也读不到, 如果输出重定向到该文件, 会起到 禁止输出的效果, 即输出内容全部丢弃

```shell
命令						说明
command > file	将输出重定向到 file
command < file	将输入重定向到 file
command >> file	将输出以追加的方式重定向到 file
n > file	将文件描述符为 n 的文件重定向到 file
n >> file	将文件描述符为 n 的文件以追加的方式重定向到 file
n >& m	将输出文件 m 和 n 合并
n <& m	将输入文件 m 和 n 合并
<< tag	将开始标记 tag 和结束标记 tag 之间的内容作为输入
```

### 传参

在执行shell脚本时, 向脚本传递参数, 脚本内获取参数的格式为: $n   n代表数字, 1为执行脚本的第一个参数, 2为第二个, 0为执行的脚本名

```shell
echo "Shell 传递参数";
echo "执行的文件名：$0";
echo "第一个参数为：$1";
echo "第二个参数为：$2";
echo "第三个参数为：$3";

参数				说明
$#				传递到脚本的参数个数
$*				以一个单字符串显示所有向脚本传递的参数  以"$1 $2 … $n"的形式输出所有参数
$$				脚本运行的当前进程ID号
$!				后台运行的最后一个进程的ID号
$@				与$*相同, 但是使用时加引号, 并在引号中返回每个参数, 以"$1" "$2" … "$n" 的形式输出所有参数
$-				显示Shell使用的当前选项, 与set命令功能相同
$?				显示最后命令的退出状态 0表示没有错误, 其他任何值表明有错误
```

### getopts获取指定关键字传参

```shell
# shell 参数   -s  task_start_date; -e  task_end_date; -f  file_path; -a  no-date
while getopts "s:e:f:a:" opt; do
  case $opt in
  s)
    task_start_date_optarg=$OPTARG
    echo $task_start_date_optarg
    ;;
  e)
    task_end_date_optarg=$OPTARG
    echo $task_end_date_optarg
    ;;
  f)
    opt_file_path=$OPTARG
    temp_file_data=$(cat $opt_file_path)
    echo $opt_file_path
    echo $temp_file_data
    ;;
  a)
    task_dt_with_all='dt_all'
    ;;
  \?)
    echo "Invalid option: -$OPTARG"
    ;;
  esac
done
```



## 流程控制

shell 的流程控制不可为空, 如果要执行的else分支没有语句执行, 就不要写

#### if else-if else

```shell
# 多行
if condition
then
    command1 
elif condition2
then
		command2
else
		command3
fi

# 单行
if condition; then command1; fi
```

#### for

```shell
# 多行
for var in item1 item2 ... itemN
do
    command1
done

for ((i=1;i<=5;i++));
do
		echo $i次调用
done

# 单行
for var in item1 item2 ... itemN; do command1; command2… done;
```

#### while

```shell
while condition
do
		command
done
```

#### until

until 循环执行一系列命令直至条件为 true 时停止, 与while恰好相反, 一般 while选择优于until

```shell
until condition
do
    command
done
```

#### case

```shell
case 值 in
模式1)
    command1
    ;;
模式2）
    command2
    ;;
*）
    commandN
    ;;    
esac
```

#### break & continue

```shell
break命令用于跳出所有循环, continue仅跳出当前循环
```



## 运算符与test命令

#### 布尔运算符

**Shell提供了与( -a )、或( -o )、非( ! )三个逻辑操作符用于将测试条件连接起来, 其优先级为:  ! > -a > -o**

```shell
a=10
b=20
运算符 说明 举例
!	非运算，表达式为true则返回false,否则返回 true	[ ! false ] 返回 true
-o	或运算，有一个表达式为true则返回true	[ $a -lt 20 -o $b -gt 100 ] 返回 true
-a	与运算，两个表达式都为true才返回true	[ $a -lt 20 -a $b -gt 100 ] 返回 false
```

### 逻辑运算符

```shell
运算符 说明 举例
&&	逻辑的AND	[[ $a -lt 100 && $b -gt 100 ]] 返回 false
||	逻辑的OR	  [[ $a -lt 100 || $b -gt 100 ]] 返回 true
```

[  ]执行基本的算数运算, 进行运算时方括号两边必须有空格

### 算数运算符

```shell
运算符 说明 举例
+    加法  `expr $a + $b` 结果为 30
-    减法  `expr $a - $b` 结果为 -10
*    乘法  `expr $a \* $b` 结果为  200
/    除法  `expr $b / $a` 结果为 2
%    取余  `expr $b % $a` 结果为 0
=    赋值  a=$b 将把变量 b 的值赋给 
==   相等 用于比较两个数字,相同则返回true [ $a == $b ]返回false
!=   不相等 用于比较两个数字,不相同则返回true [ $a != $b ]返回true
```

### 数值测试

```shell
参数 说明
-eq	等于则为真
-ne	不等于则为真
-gt	大于则为真
-ge	大于等于则为真
-lt	小于则为真
-le	小于等于则为真

eg:
num1=100
num2=100
if test $[num1] -eq $[num2]
then
    echo '两个数相等！'
else
    echo '两个数不相等！'
fi

```

### 字符串测试

```shell
参数 说明
=	等于则为真
!=	不相等则为真
-z 字符串	字符串的长度为零则为真
-n 字符串	字符串的长度不为零则为真
$ 字符串		字符串不为空则为真

eg:
num1="ru1noob"
num2="runoob"
if test $num1 = $num2
then
    echo '两个字符串相等!'
else
    echo '两个字符串不相等!'
fi
```

### 文件测试

```shell
参数 说明
-e 文件名	如果文件存在则为真
-r 文件名	如果文件存在且可读则为真
-w 文件名	如果文件存在且可写则为真
-x 文件名	如果文件存在且可执行则为真
-s 文件名	如果文件存在且至少有一个字符则为真
-d 文件名	如果文件存在且为目录则为真
-f 文件名	如果文件存在且为普通文件则为真
-c 文件名	如果文件存在且为字符型特殊文件则为真
-b 文件名	如果文件存在且为块特殊文件则为真
```

## 函数

```shell
[ function ] funname [()]
{
    action;
    [return int;]
}
```

## 文件引用

```shell
. filename   # 注意点号(.)和文件名中间有一空格
或
source filename
```


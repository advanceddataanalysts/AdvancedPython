# Linux别名

## 设置别名
```shell
alias  --查看当前所有别名
alias 别名="实际执行的命令"  --添加别名 alias vi="vim"
unalias  vi  --取消vi的别名
unalias  -a  --取消所有别名
```
> 使用alias 直接设置别名并不会永久生效, 在系统重启后alias会重置,需要写到启动的配置文件中才能永久生效

```shell
1 获取root权限

2 进入启动配置文件aliases.sh中  vim   /etc/profile.d/aliases.sh

3 添加别名  alias 别名="实际执行的命令"
	例  alias  pushgitbook="git subtree push --prefix=_book origin gh-pages"
	注: **别名不能有空格, 等于号两边不能有空格**

4 source  /etc/profile.d/aliases.sh

5 pushgitbook  执行的就是实际需要执行的命令了
```



参考文档 <https://blog.csdn.net/sinat_34104446/article/details/83046269> 


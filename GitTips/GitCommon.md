## Git 基本的使用

- git push 之前先 git pull

```shell
1.查看状态
$ git status

2.从线上拉下来最新的与自己的进行合并
$ git pull
$ git fetch --只拉取不合并

3.将自己的文件夹添加到暂存区
$ git add .<*要上传的文件目录(可选)>

4.从暂存区将代码提交到$ git本地仓库
$ git commit (--all) -m 'modify_reaon'

5.从本地仓库到线上$ git
$ git push [地址] [master(默认)]

6.设置用户名和邮箱
$ git config --global user.name(user.email) 'name/email'
## <以上为常用-------------------------------------->

1.取消文件修改
$ git checkout <需要忽略的文件/文件目录>

2.查看提交日志
$ git log 
$ git log --oneline ##简洁版

3.回退版本
$ git reset --hard <指定回退到版本的id标识>
$ git reset --hard <Head~(n)往前推回退几个版本>

4.查看每一次切换版本记录(用于当reset之后需要再次回退到回退之前的版本时)
$ git reflog 

5.创建dev分支(刚创建是dev分支和master分支的东西是一样的)
$ git branch dev

6.切换分支
$ git checkout dev

7.查看分支(输入命令打印后前面带*号的为当前分支)
$ git branch

8.合并分支
$ git merge dev

9.删除分支(不能自己删除自己当前分支)
$ git branch -d dev

10.生成公私钥(ssh)
$ ssh-keygen -t rsa 

11.将文件暂存起来放在暂存区(只能在add/commit之后才能暂存)(方便切换到其他分支工作)
$ git stash

11.恢复暂存区文件
$ git stash apply
$ git stash list (查看暂存区)
$ git stash drop (stash@{<n>})(默认恢复最近的文件)(n为第几个暂存区文件)

12.忽略一些配置文件提交(添加.gitignore.txt文件)
$ touch .gitignore.txt
$ vim .gitignore.txt(添加需要忽略的文件)

13. 删除git全局配置项
$ git config --global --unset remote.origin.url

```
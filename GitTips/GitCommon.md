---
typora-root-url: ..
---

# Git 基本的使用

> > **git push 之前先 git pull**

```python
1.查看状态
$ git status

2.从线上拉下来最新的与自己的进行合并
$ git pull
$ git fetch --只拉取不合并

3.将自己的文件夹添加到暂存区
$ git add .<*要上传的文件目录(可选)>

4.从暂存区将代码提交到 git本地仓库
$ git commit (--all) -m 'modify_reaon'

5.从本地仓库到远程仓库
$ git push [地址] [master(默认)]

6.设置用户名和邮箱
$ git config --global user.name(user.email) 'name/email'
## <以上为常用-------------------------------------->

1.取消文件修改
$ git checkout <需要忽略的文件/文件目录>

2.查看提交日志
$ git log 
$ git log --oneline ##简洁版

4.查看所有版本提交日志
$ git reflog 

3.回退版本(soft, mixed, hard, keep)
$ git reset --hard <指定回退到版本对象数的id标识>
$ git reset --hard <Head~(n)往前推回退几个版本>

5.创建dev分支(刚创建时dev分支和master分支的东西是一样的)
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

12.恢复暂存区文件
$ git stash apply (stash@{<n>}n为第几个暂存区文件)(默认恢复最近的文件)
$ git stash drop 
-- $ git stash pop (恢复最近的暂存区文件并删除缓存区中的该文件)
$ git stash list (查看暂存区)

13.忽略提交(添加.gitignore文件)
$ touch .gitignore
$ vim .gitignore(编辑需要忽略的文件,支持正则)

14. 删除git全局配置项
$ git config --global --unset remote.origin.url

15. 设置git不需要输入密码
$ git config --global credential.helper store
```
## git命令

[Git-tips](https://github.com/yanyanglong/git-tips/raw/master/assets/git.png)

![PNG](/image/git-tips.png)






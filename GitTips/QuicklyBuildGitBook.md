## 快速搭建GitBook并结合GitHub在线使用

1 安装npm

2 全局安装GitBook  `npm install -g gitbook-cli`

3 本地创建项目 例如**AdvancedPython**

4 执行命令 `gitbook init`    && `gitbook serve`  (默认4000端口 , 可指定)

5 查看本地启动的服务 **127.0.0.1:4000**  

6 本地创建需要上传到远程仓库的.md文件并上传到远程仓库

```python
git init
git remote add origin 'github项目地址'
git add .
git commit -m 'init' 
git push -u origin master
```

7 将远程文件的_book目录推到供他人访问的分支上

```python
git subtree push --prefix=_book origin gh-pages
```

8 让他人访问 下面地址(对应的个人名称和文件名目录替换掉)

https://advanceddataanalysts.github.io/AdvancedPython/


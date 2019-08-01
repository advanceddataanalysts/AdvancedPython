## GitBook建立并结合GitHub使用

1 安装npm

2 全局安装GitBook  `npm install -g gitbook-cli`

3 本地创建项目 例如**PythonCookBook** 

4 执行命令 `gitbook init`    && `gitbook serve`  (默认4000端口 , 可指定)

5 查看本地启动的服务 **127.0.0.1:4000**  

6 本地创建需要上传到远程仓库的.md文件并上传到远程仓库

```python
git init
git remote add origin https://github.com/github账号/项目名(需与本地目录一致).git
git add .
git commit -m 'init' 
git push -u origin master
```

7 本地进行测试并将_book推到供他人访问的分支上

```python
1. 本地gitbook serve启动本地gitbook服务生成静态资源文件
   访问 http://127.0.0.1:4000 
2. git push 
3. git subtree push --prefix=_book origin gh-pages
```

8 让他人访问 下面地址(对应的个人名字跟文件名改掉)

https://yanyanglong.github.io/PythonShare/

9  图片及主题设置

```python
图片
	1. 图片本地保存到某个位置, 例如along.png放到 /PythonShare/image 中
	2. 引用时将图片路径导入,默认当前路径为根文件夹路径 故引用图片路径为 /image/along.png
   		写法为 ![PNG](/image/along.png), 同时在md文件的最开始加入以下内容
        ---
        typora-root-url: ..
        ---
主题设置
    1. 根目录下创建 book.json 文件,"plugins": []中写入插件名即可, "theme-comscore"为gitbook中一个主题包 
      	详细个性化配置参考 http://www.chengweiyang.cn/gitbook/customize/book.json.html
    2. css配置, 如代码行web页面显示长度(下例为个人配置)
          根目录下创建website.css 文件,写入 .page-inner {max-width: 1000px;padding: 2px 2px 2px 2px;}
          在book.json中 加入 "styles": { "website": "website.css" }
```









-
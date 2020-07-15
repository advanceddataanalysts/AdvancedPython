# Linux--ChapterTwo

## 文件/文件夹

### 创建

- 文件

  touch  文件名  

  vim/vi  文件名   wq

  echo "字符串" > 文件名 

  echo "字符串" >> 文件名   

  > `>`将左边的命令结果写入到右边的文件, `>>`为追加

  cp   文件--one   文件--two

  mv  文件--old   文件--new

- 文件夹 

  mkdir  文件夹名

  mv  文件夹--old   文件夹--new
  
- 软链接文件

  ln  -s [-i <替换目标文件>]  源文件 目标文件

### 删除

**Linux没有回收站  一旦删除会无法找回  使用rm -rf一定要注意! ! ! **

- 文件

  rm    文件名

- 文件夹

  rm   -rf    文件夹名

```shell
#删除目录下和子目录下所有文件,保留目录结构
find /home/work/ -type f -exec rm {} \;

#删除目录和子目录下所有temp文件, 但是保留文件夹
find ./ -name "*.temp" | xargs rm
```

### 统计

```shell
#统计目录下所有文件数量(不包含子目录)
ls -al | grep "^-" | wc -l
#统计目录下所有文件数量(包含子目录 -R递归)
ls -alR | grep "^-" | wc -l

#统计目录下所有目录数量(不包含子目录)
ls -al | grep "^d" | wc -l
#统计目录下所有目录数量(包含子目录 -R递归)
ls -alR | grep "^d" | wc -l

#统计目录大小
du -sh 
#统计当前目录大小,并按文件大小排序
du -sh * | sort -n 
#查看指定文件大小
du -shk [filename]
```



### 压缩/解压缩

- 文件

  zip    压缩文件名     源文件  --压缩为.zip格式压缩文件,保留源文件

  gzip   源文件   --压缩为.gz格式压缩文件,不保留源文件

  gzip   -c    源文件   >   压缩文件   --保留源文件

  bzip2   源文件  --压缩为.zip格式压缩文件,不保留源文件

  bzip2   -k    源文件  --保留源文件

  > bzip2不能压缩目录

- 文件夹

  zip    -r    压缩文件名     源目录

  gzip   -r      源目录     --压缩目录下所有子文件,但是不能压缩目录

#### 解压缩
- zip
  - unzip  压缩文件
- gzip
  - gzip     -d    压缩文件
  - gunzip       压缩文件
- bzip2
  - bzip2    -d    压缩文件  --  -k保留压缩文件
  - bunzip2       压缩文件  --  -k保留压缩文件

### 打包(解包)后压缩(解压)
- 打包

#### tar -cvf  打包文件名  源文件

> -c  打包
>
> -v 显示过程
>
> -f  指定打包后的文件名

```shell
tar  -cvf  tar_test.tar  along.log  
```

- 解包

tar -xvf  打包文件名

> -x  解打包

```shell
tar  -xvf  tar_test.tar  
```

- 打包并压缩

  - tar    -zcvf    后缀为*.tar.gz*的压缩文件        源文件

  - tar    -jcvf    后缀为*.tar.bz2 *的压缩文件      源文件

    > -z  压缩为.tar.gz 格式
    >
    > -j  压缩为.tar.bz2 格式

- 解压并解包

  - tar    -zxvf     后缀为*.tar.gz*的压缩文件
  - tar    -jxvf      后缀为*.tar.bz2 *的压缩文件
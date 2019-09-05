# Linux--ChapterTwo

## 文件/文件夹

### 创建

- 文件

  touch  文件名  

  vim/vi  文件名   wq

  echo "字符串" > 文件名 

  echo "字符串" >> 文件名   

  > `>`将左边的命令结果写入到右边的文件, `>>`为追加

  cp  文件--one  文件--two

  mv  文件--old   文件--new

- 文件夹 

  mkdir  文件夹名

  mv  文件夹--old   文件夹--new

### 删除

**Linux没有回收站  一旦删除会无法找回  使用rm -rf一定要注意! ! ! **

- 文件

  rm  文件名

- 文件夹

  rm -rf  文件夹名

### 压缩/解压缩
- 文件

  zip 压缩文件名  源文件  --压缩为.zip格式压缩文件,保留源文件

  gzip 源文件   --压缩为.gz格式压缩文件,不保留源文件

  gzip -c  源文件  >  压缩文件   --保留源文件

  bzip2  源文件  --压缩为.zip格式压缩文件,不保留源文件

  bzip2  -k  源文件  --保留源文件

  > bzip2不能压缩目录

- 文件夹

  zip -r 压缩文件名  源目录

  gzip  -r  源目录  --压缩目录下所有子文件,但是不能压缩目录

#### 解压缩
- zip
  - unzip  压缩文件
- gzip
  - gzip -d  压缩文件
  - gunzip 压缩文件
- bzip2
  - bzip2 -d 压缩文件  --  -k保留压缩文件
  - bunzip2  压缩文件  --  -k保留压缩文件

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

  - tar  -zcvf  压缩包名.tar.gz    源文件

  - tar  -jcvf  压缩包名.tar.bz2    源文件

    > -z  压缩为.tar.gz 格式
    >
    > -j  压缩为.tar.bz2 格式

- 解压并解包

  - tar  -zxvf  压缩包名.tar.gz
  - tar  -jxvf  压缩包名.tar.bz2
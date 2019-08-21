---
typora-root-url: ..
---

# IO&File

[IO官方文档](https://docs.python.org/3/library/io.html#module-io)
[异常类官方文档](https://docs.python.org/3/library/exceptions.html#built-in-exceptions)
> IO在计算机中指Input/Output，也就是输入和输出。由于程序和运行时数据是在内存中驻留，由CPU这个超快的计算核心来执行，涉及到数据交换的地方，通常是磁盘、网络等，就需要IO接口

## stream(流)
> 所有流对于提供给他们的数据的数据类型都有严格要求, 如果使用二进制流的write()方法写入字符类型的数据,就会引发 *TypeError* 

![PNG](/image/stream.png)

##### 同步IO与异步IO

> 因为CPU写入磁盘的速度远远超过 磁盘接收的速度 
>
> 如果CPU暂停程序等待写入磁盘完成后再执行后续代码,则为同步IO
>
> 如果CPU只是告诉磁盘让ta慢慢写, 自己去干别的事了, 则为异步IO

##### 缓存

> 写入磁盘需要物理开销, 且速度较慢, 对于磁盘IO来说, 策略为留出一部分空间用做磁盘缓存,等磁盘缓存写满了再将其写入磁盘


## Python IO模块的IO类型
> 创造流最简单的方式就是使用 open()函数, 指定对应的编码格式即可创建对应类型的流

### Text I/O (文本IO)
```python
path = 'e:/Desktop/alongtest.sql'
f = open(path, 'r', encoding= 'utf-8')
f = io.StringIO('hello world')
```

### Binary I/O (二进制IO)
```python
path = 'e:/Desktop/怎么回事小老弟.jpg' 
f = open(path, 'rb')
f = io.BytesIO(b'hello world')
```
### Raw I/O (原始IO)
```python
# 不建议使用
path = 'e:/Desktop/怎么回事小老弟.jpg' 
f = open(path, 'rb', buffering = 0)
```
#### I/O操作的类层次结构

| ABC(abstract base   classes)抽象基类 | Inherits |        Stub Methods        | Mixin Methods and Properties                                 |
| :----------------------------------: | :------: | :------------------------: | :----------------------------------------------------------- |
|                IOBase                |          |    fileno,seek,truncate    | close,closed,flush,isatty,`__enter__`,`__exit__`,`__iter__`,`__next__`, readable,readline,readlines,seekable,tell,writable,writelines |
|              RawIOBase               |  IOBase  |       readinto,write       | Inherits IOBase Methods, read, readall                       |
|            BufferedIOBase            |  IOBase  | detach,read,readline,write | Inherits IOBase Methods, readinto, readintoline              |
|              TextIOBase              |  IOBase  | detach,read,readline,write | Inherits IOBase Methods, encoding, errors, newlines          |

##### 1. IO最顶层的类是抽象基类 IOBase, 其定义了流的基本接口, 但是对于读取流和写入流未作区分				 实现该基类时, 如果给定的操作没有实现, 则会引发 UnsupportedOperation 错误
##### 2. RawIOBase继承自IOBase, 用于处理的从流中读取或者向流中写入字节								FileIO是RawIOBase的子类, 为文件系统中的文件提供接口
##### 3. BufferedIOBase处理原始字节流(RawIOBase)上的缓冲, 其子类有 BufferdWriter,BufferedReader,BufferedRWPair等带缓冲区的流						          			分别是可读的流，可写的流，既可读又可写的流											 BufferedRandow提供了一个带缓冲区的接口给随机访问流  					 					BufferedIOBase的另一个子BytesIO是内存中的字节流
##### 4. TextIOBase是IOBase的另一个子类，处理文本形式的字节流，并且处理相应的对字符串的编码和解码操作    															TextIOWrapper是从TextIOBase中继承而来，是为带缓冲区的原始流提供的带缓冲区的文本接口 			StringIO是内存中的文本流 

#### IO模块类图

##### IOBase

- RawIOBase   无缓存的字节流
  -  FileIO    操作系统文件流
- BufferedIOBase    缓存的字节流
  - BytesIO
  - BufferedReader
  - BufferedWriter
  - BufferedRandom
  - BufferedRWPair
- TextIOBase    编码相关的文本流
  - StringIO   文本的内存流
  - TextIOWrapper

## IO模块的文本IO之StringIO类
> 文本I/O被读取后，就是在内存中的流  这样的内存流，在调用close()方法后释放内存缓冲区

#### StringIO类参数
initial_value = ''  缓冲区初始值
newline = '\n' 换行符
#### StringIO类额外的方法
getvalue() 返回一个str，包含整个缓冲区的内容
#### StringIO类的用法
```python
from io import StringIO
output = StringIO()
output.write('First line.\n')#写入第一行
print('Second line.', file=output)#写入第二行
print(output.getvalue())
output.close()
```

### 补充
#### 1. pickle
```python
## 几乎可以将所有的python对象转化成二进制的形式
import pickle
import pandas as pd
## 保存
df = pd.DataFrame({'a':1,'b':2},index=['along'])
with open('e:/Desktop/test.pkl','wb') as pickle_file:
    pickle.dump(df,pickle_file)
    
## 取数    
with open('e:/Desktop/test.pkl','rb') as pickle_file:
    data = pickle.load(pickle_file)
data
```


#### 2. json
```python
# 如果是文件  对应函数应为 dump(), load()
import json
d = dict(name='Bob', age=20, score=88)
json.dumps(d) --'{"name": "Bob", "age": 20, "score": 88}'


from collections import OrderedDict
s = '{"name": "ACME", "shares": 50, "price": 490.1}'
data = json.loads(s, object_pairs_hook=OrderedDict)
data
```

#### 3. 操作文件和目录
```python
import os
os.name # 操作系统类型
os.uname() # 详细的系统信息
os.path.abspath('.') # 查看当前目录的绝对路径
os.path.join('/Users', 'testdir') #在某个目录下创建一个新目录，首先要把新目录的完整路径表示出来
os.mkdir('/Users/testdir') #创建一个目录
os.rmdir('/Users/testdir') #删除一个目录
os.path.split('/Users/file.txt') # 把一个路径拆分为两部分，后一部分总是最后级别的目录或文件名
os.path.splitext('/path/to/file.txt') # 拆分文件拓展名
os.rename('test.txt', 'test.py') # 对文件重命名
os.remove('test.py') # 删除文件
os.path.isdir('test') # 判断是否为目录,一般结合列表推导式使用
[name for name in os.listdir('e:/') if os.path.isdir(os.path.join('e:/', name))] # 筛选出文件夹
[name for name in os.listdir('e:/') if name.endswith('.py')]# 删选出所有python文件
```

#### 4. open与with open 
```python
f = open(r'E:/Desktop/alongtest.txt','r',encoding='utf-8')
f.read()
f.close()
# 直接使用open方法需要调用close方法,建议使用以下方法
# 因为with 后面跟的语句返回一个对象, with要求改对象必须有一个__enter__()和__exit__()方法
with open(r'E:/Desktop/alongtest.txt','r',encoding='utf-8') as f:
    f.read()
```

```python
r read
w write
a additional
b binary
  读写都有
```

![PNG](/image/file_read&write.png)


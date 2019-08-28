# Function

### 函数的参数

函数的参数共有以下几种：

1. 位置参数；
2. 默认参数；
3. 可变参数；
4. 关键字参数；
5. 命名关键字参数；

```python
位置参数
def power(x):
    return x * x
参数 x 即是一个位置参数

def power(x, n):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
x和n，这两个参数都是位置参数，调用函数时，传入的两个值按照位置顺序依次赋给参数x和n；
```

```python
默认参数
#默认参数的值仅仅在函数定义的时候赋值一次
def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
n为默认参数
```

```python
可变参数
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
calc([1, 2, 3])

def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
calc(1, 2, 3)
###已经有一个list或者tuple，要调用一个可变参数
nums = [1, 2, 3]
calc(*nums)
```

```python
关键字参数
可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。而关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict

def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

person('Michael', 30)
output: name: Michael age: 30 other: {}
                
person('Bob', 35, city='Beijing')
output: name: Bob age: 35 other: {'city': 'Beijing'}                           
```

```python
命名关键字参数
对于关键字参数，函数的调用者可以传入任意不受限制的关键字参数。至于到底传入了哪些，就需要在函数内部通过kw检查。如果要限制关键字参数的名字，就可以用命名关键字参数

def person(name, age, *, city, job):
    print(name, age, city, job)
```

### 参数组合

```python
在Python中定义函数，可以用必选参数、默认参数、可变参数、关键字参数和命名关键字参数，这5种参数都可以组合使用。但是请注意，参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数。

def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)
```

### 函数注解

```python
def add(x:int, y:int) -> int:
return x + y
```

### 匿名函数

```python
add = lambda x, y: x + y
等同于
 def add(x, y):
	 return x + y

names = ['David Beazley', 'Brian Jones',
         'Raymond Hettinger', 'Ned Batchelder']
sorted(names, key=lambda name: name.split()[-1].lower())

funcs = [lambda x: x+n for n in range(5)]
for f in funcs:
	print(f(0))   
#实际效果是运行是 n 的值为迭代的最后一个值,匿名函数是在函数调用是绑定值

funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
	print(f(0))
#通过使用函数默认值参数形式，lambda 函数在定义时就能绑定到值

```

### 偏函数

```python
#减少可调用对象的参数个数
from functools import partial

def partial(func, *args, **keywords):

    def newfunc(*fargs, **fkeywords):

        newkeywords = keywords.copy()

        newkeywords.update(fkeywords)

        return func(*args, *fargs, **newkeywords)

    newfunc.func = func

    newfunc.args = args

    newfunc.keywords = keywords

    return newfunc

#返回一个新的partial对象，该对象在调用时的行为将类似采用位置参数args和关键字参数keywords对func的调用
```

```python
def spam(a, b, c, d):
	print(a, b, c, d)
    
s1 = partial(spam, 1)  ##位置参数
s1(2, 3, 4)

s2 = partial(spam, d=42) ##关键字参数
s2(1, 2, 3)

s3 = partial(spam, 1, 2, d=42)
s3(3)

```

### 回调函数

```python
回调函数：就是一个通过函数指针调用的函数。如果你把函数的指针（地址）作为参数传递给另一个函数，当这个指针被用来调用其所指向的函数时，我们就说这是回调函数。
通俗理解就是：把一个函数作为参数传给另一个函数，第一个函数称为回调函数
#回调函数一般运用在python的多线程中
举个栗子：

def computer(a, b, func):
    return func(a, b)

def max(a, b):
    return [a, b][a < b]
 
def min(a, b):
    return [a, b][a > b]
 
def sum(a, b):
    return str(int(a) + int(b))
 
if __name__ == "__main__":
    a = input("请输入整数a:")
    b = input("请输入整数b:")
    res = computer(a, b, max)
    print("Max of " + a + " and " + b + " is " + res)
    res = computer(a, b, min)
    print("Min of " + a + " and " + b + " is " + res)
    res = computer(a, b, sum)
    print("Sum of " + a + " and " + b + " is " + res)

以上四个函数，谁是回调函数？
```

### 偏函数，回调函数组合

```python

from multiprocessing import Pool
import time
 
def mycallback(x,y):
    with open(y, 'a+') as f:  #这里是回调函数向文件中写入值
        f.writelines(str(x))
 
def sayHi(num):
    return num
 
if __name__ == '__main__':
    e1 = time.time()
    pool = Pool()
 
    for i in range(10):
        pool.apply_async(sayHi, (i,), callback=partial(mycallback,y='yxy.txt'))
        #池的多线程
 
    pool.close()
    pool.join()
    e2 = time.time()
    print(float(e2 - e1))

```




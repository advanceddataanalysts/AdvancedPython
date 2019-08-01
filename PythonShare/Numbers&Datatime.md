# Numbers&Datatime

## Numbers

###  数字的四舍五入

```python
# 对于简单的舍入运算，使用内置的 round(value, ndigits) 函数
round(1.23, 1)
round(1.27, 1)
```

```python
round(1.5,0)
round(2.5,0)
```

```python
a = 1627731
round(a, -1)
round(a, -2)
```

```python
# 简单的输出一定宽度的数,格式化的时候指定精度
x = 1.23456
format(x, '0.3f')
print('value is {:0.3f}'.format(x))
```

### 执行精确的浮点数运算

```python
a = 4.2
b = 2.1
print(a + b==6.3) #底层 CPU 和 IEEE 754 标准通过自己的浮点单位去执行算术时导致
```

```python
#decimal 模块更精确但损耗性能
from decimal import Decimal
a = Decimal('4.2')
b = Decimal('2.1')
print(type(a + b))
Decimal('6.3')==a+b
```

```python
nums = [1.23e+18, 1, -1.23e+18]
sum(nums) 
import math
math.fsum(nums)
```

### 数字的格式化输出

```python
x = 1234.56789
format(x, '0.2f')
format(x, '>10.1f')
format(x, '<10.2f')
format(x, '^10.1f')
format(x, ',')
format(x, '0,.1f')
format(x, 'e')
format(x, '0.2E')
'The value is {:^9,.1f}'.format(x)
```
### 二八十六进制整数

```python
# 为了将整数转换为二进制、八进制或十六进制的文本串，可以分别使用 bin(),oct() 或 hex() 函数：
x = 1234
bin(x)
oct(x)
hex(x)

# 不想输出 0b , 0o 或者 0x 的前缀的话，可以使用 format() 函数
format(x, 'b') 
format(x, 'o')
format(x, 'x')

# 不同的进制转换整数字符串，简单的使用带有进制的 int() 函数
int('4d2', 16)
int('10011010010', 2)
```
### 字节到大整数的打包与解包

```python
data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004' ##字节字符串
#int.from_bytes(bytes, byteorder, *, signed=False)
#参数解释： bytes是要转换的十六进制；
#byteorder：选'big'和'little'，以上例为例，其中big代表正常顺序，即f1ff。little反之，代表反序fff1；
#signed：选True、Flase表示是否要区分二进制的正负数含义。即是否要对原二进制数进行原码反码 补码操作。 

int.from_bytes(data, 'little')
int.from_bytes(data, 'big')

x = 94522842520747284487117727783387188
x.to_bytes(16, 'big')
x.to_bytes(16, 'little')

x = 0x01020304
x.to_bytes(4, 'big') 
x.to_bytes(4, 'little')
```

###  复数的数学运算

```python
j*2=-1
a = complex(2, 4)
b = 3 - 5j
a.real
a.imag
a.conjugate() ###共轭复数   两个实部相等，虚部互为相反数的复数互为共轭复数

a + b
a * b
a / b
abs(a)

import cmath
cmath.sin(a)
cmath.cos(a)
cmath.exp(a)

#Python 的标准数学函数确实情况下并不能产生复数值
math.sqrt(-1)
cmath.sqrt(-1)
```

###  无穷大与 NaN

```python
#创建
a = float('inf')
b = float('-inf')
c = float('nan')
d = float('nan')

math.isinf(a)
math.isnan(c)

a + 45
a * 10
10 / a
a/a
a + b
c + 23
c / 2
math.sqrt(c) 
print(c==d)

```

```python
3.8,3.9,3.10 分数运算，大型数组运算，矩阵和线性代数运算  大家自己看看
```

###  随机选择

```python
import random
values = [1, 2, 3, 4, 5, 6]
random.choice(values) ###一个元素
random.choice(values)

random.sample(values, 2) ##多个元素
random.shuffle(values) ##打乱顺序

#生成随机整数
random.randint(0,10)

#生成 0 到 1 范围内均匀分布的浮点数
random.random()

#获取 N 位随机位 (二进制) 的整数
random.getrandbits(10)

###随机种子
random.seed(12345)
```
## Datatime

### 基本的日期与时间转换

```python
from datetime import timedelta
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c = a + b
c.days
c.seconds
c.seconds / 3600
c.total_seconds() / 3600

from datetime import datetime
a = datetime(2012, 9, 23)
print(a + timedelta(days=10)) 
#days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0
b = datetime(2012, 12, 21)
d = b - a
d
d.days

now = datetime.today()
print(now)
print(now + timedelta(minutes=10))

from dateutil.relativedelta import relativedelta
a + relativedelta(months=+1)
d = relativedelta(b, a)
```

### 计算最后一个周五的日期

```python
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
print(d + relativedelta(weekday=FR(3)))
```

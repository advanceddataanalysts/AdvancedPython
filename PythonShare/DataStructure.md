---
typora-root-url: ..
---
# DataStructure

## * 解压

### 解压序列赋值给多个变量(作用可迭代对象)

```python
p = (4, 5)
x, y = p
```

```python
data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
name, shares, price, date = data
name, shares, price, (year, mon, day) = data
```

```python
s = 'Hello'
a, b, c, d, e = s
```

```python
# 变量个数和序列元素的个数不匹配，会产生一个异常
p = (4, 5)
x, y, z = p
```

```python
# 部分解压
data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
_, shares, price, _=data
```

### 解压可迭代对象赋值给多个变量

```python
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
record = ('Dave', 'dave@example.com')
record = ('Dave', 'dave@example.com','773-555-1212', '847-555-1212','773-555-1213', '847-555-1213')
name, email, *phone_numbers = record
phone_numbers
```

```python
#星号表达式也能用在列表的开始部分
*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
trailing
current

trailing, *current = [10, 8, 7, 1, 9, 5, 10, 3]
trailing
current
```

```python
line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
uname, *fields, homedir, sh = line.split(':')
```

## 双向队列

```python
deque:double-ended queue
#双端队列是指允许两端都可以进行入队和出队操作的队列，其元素的逻辑结构仍是线性结构。
#将队列的两端分别称为前端和后端，两端都可以入队和出队

栈:栈是一种后进先出的数据结构，我们可以借助list来实现栈
stack = []
stack.append(item1) # 入栈
stack.pop() # 出栈，返回结果是出栈元素
peak = stack[-1] # 返回栈顶元素

队列:队列是一种先进先出的数据结构，我们可以借助list来实现队列
queue = []
queue.append(item) # 入队
queue.pop(0) # 出队，返回结果是出队元素
```

> 在队列两端插入或删除元素时间复杂度都是 O(1) ，
>
> 而在列表的开头插入或删除元素的时间复杂度为 O(N) 。

```python
from collections import deque
q = deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)
q.append(4)
q.append(5)

#q.appendleft(6)  ###默认从右边
q.clear() #清空队列
q.count(n) #在队列中统计元素的个数，n表示统计的元素
q.extend(n) #从右边扩展队列，n表示扩展的队列
q.extendleft(n) #从左边扩展队列，n表示扩展的队列
```

```python
q.pop() #队尾元素删去
q.popleft() #队头元素删去
```

##  Heap & Heapq
### 查找最大或最小的 N 个元素

```python
堆：
1.建立在完全二叉树的基础上(若设二叉树的深度为h，除第 h 层外，其它各层 (1～h-1) 的结点数都达到最大个数，
                        第 h 层所有的结点都连续集中在最左边，这就是完全二叉树。)
2.排序算法的一种，也是稳定效率最高的一种
3.可用于实现STL中的优先队列(priority_queue)
STL是Standard Template Library的简称，中文名标准模板库，惠普实验室开发的一系列软件的统称。
它是由Alexander Stepanov、Meng Lee和David R Musser在惠普实验室工作时所开发出来的
**优先队列**：一种特殊的队列，队列中元素出栈的顺序是按照元素的优先权大小，而不是元素入队的先后顺序
4.两类：
    a.最大堆：
       ①根的值大于左右子树的值   ②子树也是最大堆
    b.最小堆：
       ①根的值小于左右子树的值   ②子树也是最小堆
```

![GIF](/image/sorting_heapsort_anim.gif)

```python
该模块提供了堆排序算法的实现,heapq有两种方式创建堆， 一种是使用一个空列表，
然后使用heapq.heappush()函数把值加入堆中，另外一种就是使用heap.heapify(list)转换列表成为堆结构
```


```python
##插入
import heapq #载入heap库，heap指的是最小堆
nums = [2, 3, 5, 1, 54, 23, 132]
heap = []
for num in nums:
    heapq.heappush(heap, num)  # 加入堆

print(heap[0])  # 如果只是想获取最小值而不是弹出，使用heap[0]
print([heapq.heappop(heap) for _ in range(len(nums))])  # 堆排序结果
```


```python
heap= []
nums = [2, 3, 5, 1, 54, 23, 132]
heapq.heapify(nums)
print(nums)
print([heapq.heappop(heap) for _ in range(len(nums))])
```


```python
import math
from io import StringIO

def show_tree(tree, total_width=36, fill=' '):
    """Pretty-print a tree."""
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i + 1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write('\n')
        columns = 2 ** row
        col_width = int(math.floor(total_width / columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print(output.getvalue())
    print('-' * total_width)
    print()
```


```python
data = [2, 3, 5, 1, 54, 23, 132]
heap = []

for n in data:
    print('add {:>3}:'.format(n))
    heapq.heappush(heap, n)
    show_tree(heap)
print(heap)
```
![PNG](/image/heapq_tree_1.png)
![PNG](/image/heapq_tree_2.png)
![PNG](/image/heapq_tree_3.png)


```python
##删除
#heapq.heappop()
data = [2, 3, 5, 1, 54, 23, 132]
heapq.heapify(data)

heap = []
while data:
    i=heapq.heappop(data)
    print('pop %3d:' % i)
    show_tree(data)
    heap.append(i)
print(heap)
```
![PNG](/image/heapq_tree_4.png)
![PNG](/image/heapq_tree_5.png)
![PNG](/image/heapq_tree_6.png)
![PNG](/image/heapq_tree_7.png)


```python
import heapq
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
# print(heapq.nlargest(3, nums)) # Prints [42, 37, 23]
# print(heapq.nsmallest(3, nums)) #
```


```python
portfolio = [ {'name': 'IBM', 'shares': 100, 'price': 91.1},
{'name': 'AAPL', 'shares': 50, 'price': 543.22},
{'name': 'FB', 'shares': 200, 'price': 21.09},
{'name': 'HPQ', 'shares': 35, 'price': 31.75},
{'name': 'YHOO', 'shares': 45, 'price': 16.35},
{'name': 'ACME', 'shares': 75, 'price': 115.65} ]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
```


```python
###最小堆转最大堆
只用对元素取负，按照最小堆的方式存储，取出来的值只要再取负，就是最大值了。即push(e)改为push(-e)，pop(e)为-pop(e)

data = [2, 3, 5, 1, 54, 23, 132]
heap = []

for n in data:
    print('add {:>3}:'.format(n))
    heapq.heappush(heap, n)
    show_tree(heap)
print(heap)

heap1 = []
while heap:
    i=-1 * heapq.heappop(heap)
    print('pop %3d:' % i)
    show_tree(data)
    heap1.append(i)
print(heap1)  ####最大堆
```

###  实现一个优先级队列

```python
import heapq
class PriorityQueue:
    def __init__(self):
    self._queue = []
    self._index = 0
    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1
    def pop(self):
        return heapq.heappop(self._queue)[-1]
class Item:
    def __init__(self, name):
    self.name = name
    def __repr__(self):
    return 'Item({!r})'.format(self.name)

q = PriorityQueue()
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)
q.push(Item('spam'), 4)
q.push(Item('grok'), 1)
q.pop()
q.pop()
q.pop()
q.pop()
```

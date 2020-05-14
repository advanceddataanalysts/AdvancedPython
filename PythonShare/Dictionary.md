# Dictionary

### Q 构建字典时

> 创建字典引用其他字典时,不知道key是否存在,如果key存在则去重

```python
pairs = {'apple':2.5, 'orange':2.2, 'banana':2.6, 'tuberose':999999999}
pairs1 = {'apple':2.5, 'orange':2.2, 'banana':2.6, 'tuberose':999998, 'along':'refuse'}

## 方法一:
dic = {}
def add_dic(pairs,dic):
    for key,value in pairs.items():
        if key not in dic:
            dic[key] = []
        dic[key].append(value)
        dic[key] = list(set(dic[key]))
    return dic
add_dic(pairs=pairs,dic=dic)
add_dic(pairs=pairs1,dic=dic)
    
## 方法二:
## 代码结构更清晰
from collections import defaultdict
s_dict = defaultdict(set)
def s_add_dic(pairs,dic):
    for key,value in pairs.items():
        s_dict[key].add(value)
    return dic
s_add_dic(pairs=pairs,dic=s_dict)
s_add_dic(pairs=pairs1,dic=s_dict)
```


### Q 构建字典时

> 保证字典有序

```python
## 方法一:
## python3.6之后字典会按照构建顺序自动排序
dic = {}
dic['a'] = 1
dic['b'] = 2
dic['c'] = 3
dic['d'] = 4
print(dic)  ## {'a': 1, 'c': 3, 'b': 2, 'd': 4}

## 方法二:
## 必按照添加顺序排序 w+s
## OrderedDict内部维护了双向链表,根据加入顺序排列键的位置,但是大小是普通字典的2倍大
from collections import OrderedDict
s_dic = OrderedDict()
s_dic['a'] = 1
s_dic['b'] = 2
s_dic['c'] = 3
s_dic['d'] = 4
print(dict(s_dic)) ## {'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

### Q 构建字典时

> 从已有的字典中提取子集

```python
## 字典推导式
pairs = {'apple':2.5, 'orange':2.2, 'banana':2.6, 'tuberose':999999999}
dic = {key:value for key,value in pairs.items() if key in ['apple','orange']}
print(dic)
```

### Q 构建字典时

> 字典映射

```python

pairs = {'apple':2.5, 'orange':2.2, 'banana':2.6, 'tuberose':999999999}
pairs1 = {'apple':2.5, 'orange':2.2, 'banana':2.6, 'tuberose':999998, 'along':'refuse'}
## 方法一:
## 构建新的字典对象/在原始字典上修改
new_pairs = dict(pairs1)
new_pairs.update(pairs)
print(new_pairs)

## 方法二:
## ChainMap使用原始字典映射,更改原始字典同步反应到映射对象上
from collections import ChainMap
cm_pairs = ChainMap(pairs,pairs1)
print({key:value for key,value in cm_pairs.items()})

## 对ChaipMap对象的修改只会反映到第一个dict对象上, 反之亦然, 对字典的修改只有第一个的修改会反映到ChaipMap对象上
cm_pairs['tuberose'] = 99999999999999999999  
print(cm_pairs,'\n',pairs,'\n',pairs1) 

pairs1['tuberose'] = 9999999888888888999999999999
print({key:value for key,value in cm_pairs.items()})
```





### Q 对字典进行计算

> 将字典的key替换, value不变

```python
pairs = {'apple':2.5, 'orange':2.2, 'banana':2.6, 'tuberose':999999999}
## 方法一:
pairs['new_apple'] = pairs.pop('apple')
## 方法二:
pairs.update({'new_apple':pairs.pop("apple")})
```

### Q 对字典进行计算

> 求value最值对应的*key:value*对

```python
prices = {'A':2.22,'B':9.06,'C':0.06,'D':9.06,'E':0.06}
print(max(prices)) ## 'E'
## 多条记录value相等时  按照第二个参数大小排序
print(max(zip(prices.values(),prices.keys()))) ## (9.06, 'D')

## 多条记录value相等时  取第一次出现的键值对
print(max(prices, key=lambda k: prices[k]), prices[max(prices, key=lambda k: prices[k])]) ## B 9.06
```

### Q 对字典进行计算

> 求两个/多个字典的相同点

```python
a_dict = {'x':1, 'y':2, 'z':3}
b_dict = {'x':1, 'y':2, 'w':3}
c_dict = {'x':1}
print(a_dict.keys() & b_dict.keys()) ##{'x', 'y'}
print(a_dict.keys() & b_dict.keys() & c_dict.keys()) ##{'x'}
print(a_dict.items() & b_dict.items()) ## {('x', 1), ('y', 2)}
c = {key:a_dict[key] for key in a_dict.keys() - {'z','w'}} 
print(c) ##{'x': 1, 'y': 2}
```

### Q 对字典进行计算

> 通过公共键对字典列表排序

```python
rows = [{'fname':11, 'lname':2, 'uid':1003},
       {'fname':111, 'lname':22, 'uid':1004},
       {'fname':111, 'lname':222, 'uid':1002},
       {'fname':11, 'lname':222, 'uid':1003},]
## 方法一:
sorted(rows, key=lambda x:x['uid'])
sorted(rows, key=lambda x:(x['fname'],x['lname']))

## 方法二:
## 运行速度更快,性能好(max,min也同样支持)
from operator import itemgetter
sorted(rows, key=itemgetter('uid'), reverse=True)
sorted(rows, key=itemgetter('fname','lname'),reverse=False)

## 方法三:
## 转成df,排序结束再用df.to_dict()/df.to_json()转
import pandas as pd
data = pd.DataFrame(rows)
data.sort_values(by=['uid'],inplace=True)
data.to_dict(orient='records')
```

### Q 对字典进行计算

> 根据键对数据进行分组

```python
rows = [{'address':'zhongguancun', 'date':'07/01/2018'},
       {'address':'putuo', 'date':'07/02/2018'},
       {'address':'wangfujing', 'date':'07/01/2018'},
       {'address':'jingan', 'date':'07/04/2018'},]

## 方法一:
## sort+itemgetter+groupby
from operator import itemgetter
from itertools import groupby
rows.sort(key=itemgetter('date'))  ##分组前需要先排序,因为groupby()只能检查连续的项

for key, value in groupby(rows, key=itemgetter('date')):
    print(key)
    for i in value:
        print(' ',i)
        
## 方法二:
## 转成df,groupby之后再转成字典
import pandas as pd
data = pd.DataFrame(rows)
for key,value in data.groupby(by=['date']):
    print(key,list(value.T.to_dict().values()))
```
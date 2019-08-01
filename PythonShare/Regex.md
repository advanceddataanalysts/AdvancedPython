# Regex

> 模式匹配: 模式匹配是数据结构中字符串的一种基本运算, 给定一个子串, 要求在某个字符串中找出与该子串相同的所有子串 

### tips: 

正则表达式使用反斜杠（`'\'`）来表示特殊形式，或者把特殊字符转义成普通字符.  而反斜杠在普通的 Python 字符串里也有相同的作用，所以就产生了冲突.    比如说，要匹配一个字面上的反斜杠，正则表达式模式不得不写成 `'\\\\'`，因为正则表达式里匹配一个反斜杠必须是 `\\` ，而每个反斜杠在普通的 Python 字符串里都要写成 `\\` .    

**解决办法是对于正则表达式样式使用 Python 的原始字符串表示法: ** 在带有 `'r'` 前缀的字符串字面值中，反斜杠不必做任何特殊处理.  因此 `r"\n"` 表示包含 `'\'` 和 `'n'` 两个字符的字符串，而 `"\n"` 则表示只包含一个换行符的字符串.  样式在 Python 代码中通常都会使用这种原始字符串表示法来表示.   

```python
import re
## 不带'r'前缀
a = '''aaa\\bbbb'''
re.split('\\\\',a) # ['aaa', 'bbbb']

## 带'r'前缀
re.split(r'\\',a) # ['aaa', 'bbbb']
```

## 正则表达式语法

> 用来检查某个字符串是否跟给定的正则表达式匹配

### 常用特殊字符及含义

**.**  匹配除了换行的任意字符  如果指定了标签 `DOTALL` (re.S, re.DOTALL)，它将匹配包括换行符的任意字符 
**^**  匹配字符串的开头   **$**  匹配字符串尾或者换行符的前一个字符
*****  对它前面的正则式匹配0到任意次重复， 尽量多的匹配字符串
**+**  对它前面的正则式匹配1到任意次重复
**?**  对它前面的正则式匹配0到1次重复

***?, +?, ?? **
'\*', '+'和 '?' 修饰符都是*贪婪的*,  它们在字符串进行尽可能**多**的匹配
在修饰符之后添加 `?` 将使样式以 *非贪婪* 方式进行匹配 , 尽量**少**的字符将会被匹配 

{m-n} 对其之前的正则式指定匹配 *m-n*个重复 ,在 *m* 和 *n* 之间取尽量多 
{m-n}?  上一个修饰符的非贪婪模式，只匹配尽量少的字符次数

**\\**  转义特殊字符
**[]**  用于表示一个字符集合
**|**  `A|B`  A 和 B 可以是任意正则表达式, 一旦 A 匹配成功， B 就不再进行匹配

b,B   s,S  d,D   w,W    Z... 等特殊转义字符详解见 [re正则表达式操作](https://docs.python.org/zh-cn/3/library/re.html#module-re )



## 模块

#### re.compile(*pattern*, *flags=0*) 

> 将正则表达式的样式编译为一个 正则表达式对象 （正则对象），可以用于匹配，通过这个对象的方法 match(), search()
>
> 通过 `re.compile()`编译后的样式，和模块级的函数会被缓存， 所以少数的正则表达式使用无需考虑编译的问题.  

```python
import re
a = '''aaa\nbbbb'''
tmp = re.compile(r'(.*)\n(.*)')
tmp.match(a)  ## <re.Match object; span=(0, 8), match='aaa\nbbbb'>

## 等价于 re.match(pattern=r'(.*)\n(.*)', string=a, flags=0)
```

```python
flags: 
re.A(re.ASCII)  让 \w, \W, \b, \B, \d, \D, \s 和 \S 只匹配ASCII，而不是Unicode
re.DEBUG 显示编译时的debug信息
re.I(re.IGNORECASE)  进行忽略大小写匹配
re.S(re.DOTALL)  让 '.' 特殊字符匹配任何字符，包括换行符；如果没有这个标记，'.' 就匹配除了换行符的其他任意字符
```

#### re.search(pattern, *string*, *flags=0* )
```python
扫描整个字符串找到匹配样式的第一个位置, 并返回一个相应的匹配对象
如果没有匹配，就返回 None 
```
#### re.match(pattern, *string*, *flags=0* )
```python
如果 string 开始的0或者多个字符匹配到了正则表达式样式, 就返回一个相应的匹配对象 
如果没有匹配，就返回 None 
import re
a = '''aaa\naab\naaa'''
tmp = re.compile(r'.*b\n')
tmp.search(a)  ## <re.Match object; span=(4, 8), match='aab\n'>
tmp.match(a)  ## None
```
#### re.fullmatch(pattern, *string*, *flags=0* )
```python
如果整个 string 匹配到正则表达式样式, 就返回一个相应的匹配对象 
如果没有匹配，就返回 None 
import re
a = '''aaa\naaa\naaa'''
tmp = re.compile(r'.*\n.*\n.*')
tmp.fullmatch(a)  ## <re.Match object; span=(0, 11), match='aaa\naaa\naaa'>
```
#### re.split(pattern, *string*, *flags=0* )
```python 
用 pattern 分开 string , 如果在 pattern 中捕获到括号，那么所有的组里的文字也会包含在列表里.
如果 maxsplit 非零， 最多进行 maxsplit 次分隔， 剩下的字符全部返回到列表的最后一个元素
re.split(r'\W+', 'Words, words, words.', 1) # ['Words', 'words, words.']
```
#### re.findall(pattern, *string*, *flags=0* )
```python 
对 string 返回一个不重复的 pattern 的匹配列表， string 从左到右进行扫描，匹配按找到的顺序返回.    
如果样式里存在一到多个组，就返回一个组合列表；就是一个元组的列表（如果样式里有超过一个组合的话）.    
空匹配也会包含在结果里.    
import re
a = '''aaa\naab\naac\n'''
re.findall(r'.+\n.*?',a) ## ['aaa\n', 'aab\n', 'aac\n']
```
#### re.finditer(pattern, *string*, *flags=0* )
```python 
pattern 在 string 里所有的非重复匹配，返回为一个迭代器 iterator 保存了 匹配对象 .     
string 从左到右扫描，匹配按顺序排列.    
空匹配也包含在结果里.    
import re
a = '''aaa\naab\naac\n'''
c = []
[c.append(i.group(0)) for i in re.finditer(r'.+[a|b]\n.*?',a)]
print(c) ## ['aaa\n', 'aab\n']
```
#### re.sub(pattern, repl, string, count=0, flags=0)
```python 
返回通过使用 repl 替换在 string 最左边非重叠出现的 pattern 而获得的字符串.     
如果样式没有找到，则不加改变地返回 string.     
repl 可以是字符串或函数；如为字符串，则其中任何反斜杠转义序列都会被处理.    
如果 repl 是一个函数，那它会对每个非重复的 pattern 的情况调用.    
这个函数只能有一个 匹配对象 参数，并返回一个替换后的字符串.    
```
#### re.subn(pattern, repl, string, count=0, flags=0)
```python 
行为与 sub() 相同，但是返回一个元组 (字符串, 替换次数).
```

## 正则表达式对象

> 编译后的正则表达式对象支持的方法和属性 

```python
pattern = re.compile("\n")
```
#### Pattern.search(*string*[, *pos*[, *endpos*]]) 
#### Pattern.match(*string*[, *pos*[, *endpos*]]) 
#### Pattern.fullmatch(*string*[, *pos*[, *endpos*]]) 
#### Pattern.split(*string*[, *pos*[, *endpos*]]) 
#### Pattern.findall(*string*[, *pos*[, *endpos*]]) 
#### Pattern.finditer(*string*[, *pos*[, *endpos*]]) 
#### Pattern.sub(*string*[, *pos*[, *endpos*]]) 
#### Pattern.subn(*string*[, *pos*[, *endpos*]]) 



#### Pattern.flags  正则匹配标记 

#### Pattern.groups 捕获组合的数量 

#### Pattern.groupindex 

##### 映射由 (?P<id>) 定义的命名符号组合和数字组合的字典  如果没有符号组, 那字典就是空的

#### Pattern.pattern   

##### 编译对象的原始样式字符串

## 匹配对象
```python
匹配对象总是有一个布尔值 True.    
如果没有匹配的话 match() 和 search() 返回 None 所以可以用 if 语句来判断是否匹配
import re
a = '''aaa\naab\naac\n'''
x = re.match(r'.+\n.*?',a)
if x:
    print(x.group()) ## aaa
```

#### Match.group([group1, ...]) 
```python
返回一个或者多个匹配的子组.    
如果只有一个参数，结果就是一个字符串，如果有多个参数，结果就是一个元组（每个参数对应一个项）
如果没有参数，组1默认到0（整个匹配都被返回）
import re
a = '''aaa\naab\naaa'''
tmp = re.compile(r'(.*\n)(.*\n).*')
x = tmp.search(a)  
x.group() ## 'aaa\naab\naaa'
x.group(0) ## 'aaa\n'
x.group(1) ## 'aab\n'
```

#### Match.groups(default=None) 
```python
返回一个元组，包含所有匹配的子组，在样式中出现的从1到任意多的组合.     
default 参数用于不参与匹配的情况，默认为 None.    
import re
a = '''aaa\naab\naaa'''
tmp = re.compile(r'(.*\n)(.*\n).*')
x = tmp.search(a)  
x.groups() ## ('aaa\n', 'aab\n')
```

#### Match.start([group])
#### Match.end([group])
```python
返回 group 匹配到的字串的开始和结束标号
x.start() ## 0
x.end ()  ## 11
```
#### Match.span([group])
```python
对于一个匹配 m, 返回一个二元组 (m.start(group), m.end(group)).  
如果 group 没有在这个匹配中，就返回 (-1, -1).    
group 默认为0，就是整个匹配.    
x.span() ## (0, 11)
x.span(1) ## (0, 4)
x.span(2) ## (4, 8)
```

#### Match.pos
#### Match.endpos
```python
正则引擎开始/停止在字符串搜索一个匹配的索引位置
```

#### Match.re 

##### 返回产生这个实例的 正则对象,    这个实例是由 正则对象的 match() 或 search() 方法产生的

#### Match.string 

##### 传递到 match() 或 search() 的字符串


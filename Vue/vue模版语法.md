# vue模板语法

## 模版语法

> https://vuejs.bootcss.com/guide/syntax.html

#### 1: 插值

```shell
文本: 双大括号 {{ number }}
html: v-html 
属性: v-bind:key='value'
表达式: {{ JavaScript表达式 }}  
	只能使用单个表达式,例:
	{{ number + 1 }}, {{ value === 'ok' ? 'yes' : 'no' }}
	错误例:
	{{ var a = 1 }},  {{ if (value === 'ok') { return message } }}
```

#### 2: 指令

指令是带有 v- 前缀的属性,指令必须添加到元素上,单个使用指令无意义也不生效 
指令的作用是在 表达式的值发生改变时,产生连带影响作用于DOM,改变样式

```shell
例如: v-if 
	<p v-if="seen">现在你看到我了</p>  
		v-if指令通过表达式seen的值来插入/移除 <p>元素

带参数的指令:
一些指令通过接受参数来更新html的属性
例如: v-bind
	<a v-bind:href="url">...</a>
	v-bind后跟的是元素 <a> 的属性, 代表的意思是 将<a>元素的 href属性与表达式url的值绑定
	
	v-on
	<a v-on:click="doSomething">...</a>
	v-on用来监听DOM事件,比如点击事件,输入事件  这里代表的意思是将 <a>的点击事件与函数doSomething绑定
	
动态参数:
	用方括号括起来的 JavaScript表达式作为指令的参数,例如:
	<a v-bind:[attributeName]="url"> ... </a>
	<a v-bind:key2="url"> ... </a>
	attributeName = key
	attributeName = key2
	这里的attributeName会被作为 JavaScript表达式进行动态求值,得到的结果当作参数与url的值进行绑定 
	
	v-on的动态参数绑定:
	<a v-on:[eventName]="doSomething"> ... </a>

注: 在 html元素中避免使用大写字符来命名键名,因为浏览器会把所有的属性名全部小写, 例如 
	<a v-bind:[someAttr]="value"> ... </a>
	这段代码会被转成 v-bind:[someattr], 如果未定义 someattr则无法识别

```

#### 3: 缩写

```shell
v- 前缀是有独特的标识意义,但是在一些经常用到的指令,写起来就比较繁琐, 所以vue对两个最常用的属性提供了特殊简写
v-bind 缩写  
  <a v-bind:href="url">...</a>  <!-- 完整语法 -->
  <a :href="url">...</a>  <!-- 缩写 -->
  <a :[key]="url"> ... </a>  <!-- 动态参数的缩写 (2.6.0+) -->
  
  
v-on 缩写  
  <a v-on:click="doSomething">...</a> <!-- 完整语法 -->
  <a @click="doSomething">...</a> <!-- 缩写 -->
  <a @[event]="doSomething"> ... </a> <!-- 动态参数的缩写 (2.6.0+) -->
```



## 条件渲染

#### v-if

```shell
v-if指令用于条件渲染一块内容, 改指令只会在表达式返回truthy值的时候被渲染, 例如
	<h1 v-if="awesome">Vue is awesome!</h1>
	只会在awesome的值为真值的时候被渲染, js的真值判断<知识点>
	
v-if添加到<template>元素上可以用来控制切换多个元素, 在<template>上使用v-if,最终的渲染结果不包含<template>
  <template v-if="ok">
    <h1>Title</h1>
    <p>Paragraph 1</p>
    <p>Paragraph 2</p>
  </template>
```

#### v-else/v-else-if

```shell
v-else: 必须跟在 v-if/ v-else-if后面,否则不会被识别
<div v-if="Math.random() > 0.5">Now you see me</div>
<div v-else>Now you do not</div>

v-else-if: v-if的多条件补充, 必须跟在 v-if/ v-else-if后面
```

#### v-show

```shell
<h1 display v-show="ok">Hello!</h1>

带有v-show的元素会始终被渲染保存在DOM中, v-show只是切换元素的CSS属性 display,
v-show不支持 <template> 元素, 也不支持 v-else
```

比较:  

v-if 是真正的条件渲染, 它会确保在切换过程中条件块内的子组建销毁和重建;

v-show不论什么条件都会进行渲染,只是基于CSS的切换

v-if有更高的切换开销, v-show有更高的初始渲染开销 建议: 频繁切换用v-show, 运行条件很少改变用v-if



## 列表渲染

#### v-for

```shell
arr:
v-for指令基于一个数组来渲染一个列表, v-for指令使用形式如 item in items (item of items)的语法, items是元数据数组, item是被迭代的数据的别名

items:[{ message: 'Foo' },{ message: 'Bar' }]
  <li v-for="item in items" :key="item.message">
    {{ item.message }}
  </li>
结果:
  Foo
  Bar
  
 v-for第二个参数, 为当前项的索引
   <li v-for="(item, index) in items"> :key="item.message">
    {{ index }} - {{ item.message }}
  </li>
结果:
  0-Foo
  1-Bar
  
object:
v-for遍历一个对象的属性
object: { title: 'How to do lists in Vue', author: 'Jane Doe', publishedAt: '2016-04-10' }
	<div v-for="value in object"> {{ value }} </div>
结果:
	How to do lists in Vue
	Jane Doe
	2016-04-10

v-for第二个参数访问对象的键名
	<div v-for="(value, name) in object"> {{ name }}: {{ value }} </div>
结果:
	title:How to do lists in Vue
  author:Jane Doe
  publishedAt:2016-04-10
	
```

为了给vue一个提示,以便跟踪到每个节点的身份,从而重用和重拍现有元素,在进行v-for渲染时, 需要为对应的元素提供一个 唯一的 key 属性

对于arr来说, 唯一key是arr的索引,例:  <div v-for="item in items" v-bind:key="item.id"></div>

对于object来说, 唯一key是键, 例: <div v-for="(value, name) in object" v-bind:key="name"></div>



不推荐在同一元素上使用v-if和v-for:

当它们处于同一节点时, v-for的优先级比v-if更高, 意味着, v-if将分别重复运行于每个v-for循环中



## 生命周期 : https://vuejs.bootcss.com/guide/instance.html#生命周期图示
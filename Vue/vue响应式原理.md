# vue响应式原理

```shell
官网响应式原理:https://vuejs.bootcss.com/guide/reactivity.html
详解响应式原理:https://www.cnblogs.com/fundebug/p/responsive-vue.html
```

vue最独特的特性之一是: **非侵入性的响应式系统**

vue的数据模型仅是普通的JavaScript对象, 当修改数据模型时, 视图会进行更新

## 非侵入性

当增加功能时, 代码是否需要使用新的 语法/数据类型/数据结构

前端举例: 使用jQuery时, 表面上是在写JavaScript, 实际上是在写基于 jQuery的API, 为了实现MVVM的效果, 需要创建Model(数据)和View(视图)实例, 为了使数据变化时视图随着更改, 需要操控视图实例(修改DOM); 与之对比的vue只是在给某个数据结构(对象)的某个属性赋值而已, 并不会修改视图实例

后端举例: 实现某个功能的时候, 类A需要继承第三方类库B(侵入)  与  在A类中直接调用类B的某个方法(非侵入)

## 如何追踪变化

1 当把JavaScript对象传入Vue实例作为data选项, Vue会遍历此对象所有的property, 并使用**Object.defineProperty**把这些property全部转换为 getter/setter,  **Object.defineProperty**只有在IE8以上版本浏览器才支持, 即Vue也只能在IE8以上的浏览器版本才能使用  ----**侦测数据变化(数据劫持/数据代理)**

2 每个组件实例都对应一个**watcher**实例, watcher会在组件rander函数渲染的过程中把**接触("Touch")**过的对象全部记录为依赖(Dependency), 之后当依赖项的setter触发时, 都会 **通知(Notify)**到watcher ----**收集视图依赖的数据(依赖收集)**

3 watcher接收到依赖数据变化后会通知rander函数重新渲染生成虚拟DOM树 ----**更新视图(发布订阅模式)**

![PNG](/image/vue_track_change.png)

## 追踪变化的注意事项

由于JavaScript的限制, vue不能检测数组和对象的变化,但是可以通过一些办法来回避这些限制以保证响应性

### 数组

```shell
1 直接利用索引设置一个数组时

2 修改数组长度时

解决办法:

1 使用Vue.set(object, propertyName, value)方法添加   -- this.$set(object, propertyName, value) 是Vue.set的别名

2 使用splice方法更改数组数据

vm.message_list.splice(indexOfitem,1,newValue)

3 使用splice方法更改数组长度

 vm.message_list.splice(newLength)
```

### 对象

```shell
vue无法检测property的添加/移除, vue只会在初始化实例时对property执行getter/setter转化, 所以property必须在data对象上存在才能把它转换为响应式的

解决办法:

1 在初始化的时候添加在data对象上

2 使用Vue.set(object, propertyName, value)方法添加   -- this.$set(object, propertyName, value) 是Vue.set的别名

当为已有对象赋值多个property时, 创建一个新的对象覆盖原对象达到更新的目的

this.someObject = Object.assign({}, this.someObject, newObject)
```

### 演示

```html
<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8">
<header>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
</header>

<body>
<div id="example">
    <ul>
        <li v-for="item in message_list">{{item}}</li>
    </ul>
    <p>
        "message_obj: "{{message_obj}}
    </p>
    <p>
        "message_obj.a: "{{message_obj.a}}
    </p>
    <br>
    <button @click="btnclick">按钮</button>
</div>
</body>
</html>

<script type="text/javascript">
  var vm = new Vue({
    el: '#example',
    data: {
      message_list: ['a1', 'b2', 'c3', 'd4'],
      message_obj: {'a': ['a1', 'b2', 'c3', 'd4']},
      //在初始化时赋值
      // message_obj: {'a': ['a1', 'b2', 'c3', 'd4'], 'b':undefined},
    },
    methods: {
      btnclick() {
// 数组非响应式更新
        vm.message_list[1] = 999;  // 直接使用索引更改数组的值
        vm.message_list.length = 1; // 直接更改数组的长度
        console.log('触发按钮，message_list:', vm.message_list);
        console.log('触发按钮，message_list长度:', vm.message_list.length);
    //arr解决方案start
        // Vue.set(vm.message_list, 1, 999);
        // this.$set(vm.message_list, 1, 999);
        // vm.message_list.splice(1,1,999);
        // vm.message_list.splice(1)

        // 解决方案: 1 Vue.set(vm.message_list, 1, 999)  |  this.$set(vm.message_list, 1, 999)
        //          2 使用splice方法更改数组数据  vm.message_list.splice(1,1,999)
        //          3 使用splice方法更改数组长度  vm.message_list.splice(1)
    //arr解决方案end
        
        
// 对象非响应式更新
        vm.message_obj.b = 'b'; // 初始化未定义在data对象中, 非响应式
    //object解决方案start
        // Vue.set(vm.message_obj, 'b', 'b');
        // this.$set(vm.message_obj, 'b', 'b');
        // this.message_obj = Object.assign({}, this.message_obj, {'c':'c'}, {'d':'d'});

        // 解决方案: 1 在初始化时赋值, message_obj: {'a': ['a1', 'b2', 'c3', 'd4'], 'b':undefined}
        //          2 Vue.set(vm.message_obj, 'b', 'b')  |  this.$set(vm.message_obj, 'b', 'b')
        //          3 创建新的对象 this.message_obj = Object.assign({}, this.message_obj, {'c':'c'}, {'d':'d'})
    //object解决方案end
      }
    },
  });
</script>
```


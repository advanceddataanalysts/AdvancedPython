## 数组函数

**element_at(*array,index*)**

返回数组中索引index对应的元素(index可以为负数)

**array_position(*array, element*)** 

返回element在数组中的位置(bigint)

**array_agg()**

聚合函数，将一列所有内容变成一个数组返回。

**array_join(*array,delimiter,null_value_replacement*)**

将数组中的所有元素以delimiter指定的分隔符连接起来，null值用null_value_replacement代替，返回一个字符串

## 字符串函数

**split(*string*，*delimiter*)** 

以delimiter分隔符拆分字符串,返回一个数组。

**split_part （*string*，*delimiter*，*index*）** 

以delimiter分隔符拆分字符串,返回索引对应的字符串.字段索引以1开头(不可为负数).如果索引大于字段数，则返回null.

<font color=#008000 >类似于mysql中substring_index函数(index>0).</font>

```sql
select split_part('北京,上海,广州',',',1)
```

**strpos(*string*，*substring*)** 

返回子字符串在字符串中第一次出现的位置。从1开始。如果未找到，则返回0。

<font color=#008000 >类似于mysql中的locate函数,但locate是子字符串在前.</font>

```sql
select strpos('上海黄浦区','黄浦')
```

## 组合使用

**array_join(*array_agg(),delimiter,null_value_replacement*)**

<font color=#008000 >类似于mysql中的group_concat函数.</font>

**element_at(*split(string,delimiter),index*)**

<font color=#008000 >类似于mysql中的substring_index函数.</font>

```sql
select element_at(split('北京,上海,广州',','),-1)
select element_at(split('北京,上海,广州',','),2)
```










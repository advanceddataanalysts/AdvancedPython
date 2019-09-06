## 数组函数

**element_at(*array,index*)**

返回数组中索引index对应的元素(index可以为负数)

**array_position(*array, element*)** 

返回element在数组中的位置(bigint)

**array_agg()**

聚合函数，将一列所有内容变成一个数组返回。

**array_join(*array,delimiter,null_value_replacement*)**

将数组中的所有元素以delimiter指定的分隔符连接起来，null值用null_value_replacement代替，返回一个字符串

**filter(*array,function*)**

将函数function中返回true的元素来构造新数组

```sql
SELECT filter(ARRAY [], x -> true); -- []
SELECT filter(ARRAY [5, -6, NULL, 7], x -> x > 0); -- [5, 7]
SELECT filter(ARRAY [5, NULL, 7, NULL], x -> x IS NOT NULL); -- [5, 7]
```



## 字符串函数

**split(*string*，*delimiter*)** 

以delimiter分隔符拆分字符串,返回一个数组。

**split_part （*string*，*delimiter*，*index*）** 

以delimiter分隔符拆分字符串,返回索引对应的字符串.字段索引以1开头(不可为负数).如果索引大于字段数，则返回null.

<font color=#008000 >类似于mysql中substring_index函数(index>0).</font>

```sql
select split_part('北京,上海,广州',',',1) -- 北京
```

**strpos(*string*，*substring*)** 

返回子字符串在字符串中第一次出现的位置。从1开始。如果未找到，则返回0。

<font color=#008000 >类似于mysql中的locate函数,但locate是子字符串在前.</font>

```sql
select strpos('上海销售分公司四中心二区二部精英学院','精英学院') -- 15
```

**substr(*string,start*)**

从start位置开始返回字符串的其余部分。位置从1开始。如果start为负，则起始位置代表从字符串的末尾开始倒数

```sql
select substr('数学,英语,', -1)  -- ,
select substr('数学,英语,', -1)  -- 英语,
```

**substr(*string, start, length*)**

从start位置开始返回长度为length的字符串的子串。位置从1开始。如果start为负，则起始位置代表从字符串的末尾开始倒数

## 组合使用

**array_join(*array_agg(),delimiter,null_value_replacement*)**

<font color=#008000 >类似于mysql中的group_concat函数.</font>

```sql
select tcp.contract_id,array_join(array_agg(pay_method_new),',')
from table1 tcp
left join table2 tc on tc.contract_id = tcp.contract_id
where tcp.contract_id = 'X20011907000631'
and tcp.pay_status in (2,4)
and tc.status not in (7,8)
group by tcp.contract_id
```

**array_join(*filter(array_agg(conditon),function),delimiter*)**

```sql
select array_join(filter(array_agg(case when is_success_extend = 0 then tbk.extend_subject_name else null end),x -> x is not null),',')
```

<font color=#008000 >当需要加判断条件时,如果不加filter函数,用以下写法,字段最后可能会出现逗号</font>

```sql
select array_join(array_agg(case when is_success_extend = 0 then  tbk.extend_subject_name end), ',')  extend_fail_subject_name
```

**element_at(*split(string,delimiter),index*)**

<font color=#008000 >类似于mysql中的substring_index函数.</font>

```sql
select element_at(split('北京,上海,广州',','),-1) -- 广州
select element_at(split('北京,上海,广州',','),2)  -- 上海
select element_at(split('客户关系部,课程顾问部,江苏分公司,江苏销售一中心,江苏销售一中心一区,江苏销售一中心一区二部',','),-1)
```

**去掉字符串末尾的逗号**

```sql
select (case when substr('数学,英语,', -1) = ',' then substr('数学,英语,',1,length('数学,英语,')-1) end)  -- 数学,英语
```








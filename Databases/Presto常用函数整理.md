#### 1.字符串长度计算函数：length

语法: length(string A)

```
select length('iteblog')
```

#### 2.字符串反转函数：reverse

语法: reverse(string A) 返回值: string 说明：返回字符串A的反转结果

```
select reverse('iteblog')
```

#### 3.字符串连接函数：concat

语法: concat(string A, string B…) 返回值: string 说明：返回输入字符串连接后的结果，支持任意个输入字符串

```
 select concat('www','iteblog','com')
```

使用||运算符实现字符串的拼接(快)

```
 select  'www' ||  'iteblog' || 'com'
```

#### 4.字符串截取函数：substr,substring

语法: substr(string A, int start),substring(string A, int start) 返回值: string 说明：返回字符串A从start位置到结尾的字符串

```
  select substr('iteblog',3) 

  select substr('iteblog',3,2) 

  select substr('iteblog',-3,2)  

  select substring('iteblog',3) 

  select substring('iteblog',3,2) 

  select substring('iteblog',-3,2)
```

#### 5.replace(string, search) → varchar

删除字符串 string 中的所有子串 search 。

```
select replace('itebtlog', 't')
```

replace(string, search, replace) → varchar

将字符串 string 中所有子串 search 替换为 replace。

```
select replace('itebtlog', 't','k')
```

#### 6.strpos(string, substring) → bigint

返回字符串中子字符串的第一次出现的起始位置。位置以 1 开始 ，如果未找到则返回 0 。

```
select  strpos('titebtlog', 't')

select  strpos('itebtlog', 'p')
```

#### 7.regexp_replace:将原字符中的指定字符替换

```
select regexp_replace('aabb','b','c')
```

#### 8.regexp_extract：通过下标返回正则表达式指定的部分

```
select regexp_extract('123abc456','([0-9]*)([a-z]*)([0-9]*)',3)
```

#### 9.coalesce:返回参数列表中第一个非null值

```
select coalesce(null,'a','b')

select coalesce(null,null,null)
```

将null值替换

```
select 
    student_intention_id,
    student_no,
    name,
    coalesce(name,'小花')
from view_student 
where name is null 
limit 10
```

#### 10.条件函数:if

```
select if(1+1=2,'a','b')
```

#### 11.窗口函数

first_value(x):返回窗口内的第一个value，一般用法是窗口内数值排序，获取最大值。

last_value(x) 含义和first value相反。

sum()

```
select 
    lp.student_id,
    cast(substr(lp.adjust_start_time,1,19) as timestamp) adjust,
    teacher_id,
    first_value(teacher_id) OVER (PARTITION BY student_id ORDER BY  cast(substr(lp.adjust_start_time,1,19) as timestamp) ),
    first_value(lp.adjust_start_time) OVER (PARTITION BY student_id ORDER BY  cast(substr(lp.adjust_start_time,1,19) as timestamp) )
from lesson_plan  lp
where student_id in (1537357,1537006,1537362,1537336,1537025)
```

#### 12.数组函数

**array_agg** (key)是一个聚合函数，表示把key这一列的所有内容变成一个数组返回。

**array_distinct**：返回去重后的数组

**array_max(array)** -> E 返回数组中最大的元素

**array_min(array)** -> E 返回数组中最小的元素

**array_position(x, element)** -> bigint 返回element在数组中的位置

**contains(x, element)** -> boolean 判断element是否在数组x中

**array_remove(x, element)** -> x 移除数组x中的所有element元素

**cardinality(x)** -> bigint 返回数组的元素个数

```
select 
    lp.student_id,

    -- array_agg(sj.subject_name),

    -- array_agg(distinct sj.subject_name),
    -- array_distinct(array_agg(subject_name))

    -- array_agg(distinct sj.subject_id),
    -- array_max(array_agg(distinct sj.subject_id))


    -- array_position(array_agg(distinct sj.subject_name),'体验课'),

    -- contains(array_agg(distinct sj.subject_name),'体验课'),

    -- array_remove(array_agg(distinct sj.subject_name),'体验课')

    -- cardinality(array_agg(distinct sj.subject_name))

    --array_join(array_agg(distinct subject_name), '-') subject_name

from lesson_plan  lp
left join subject sj on sj.subject_id = lp.subject_id
where student_id in (1537357,1537006,1537362,1537336,1537025)
group by lp.student_id
```

#### **13.lambda函数**

lambda表达式的书写形式为`->`

**(1)filter(array, function) -> array**

array中的每一个元素经过function过滤，返回都为true的元素

**(2)transform(array, function) → ARRAY**

对数组中的每个元素，依次调用function，生成新的结果U。

```
select 
    lp.student_id,

    array_agg(distinct lp.lesson_type),
    filter(array_agg(distinct lp.lesson_type), x -> x=3),

    array_agg(distinct subject_name),
    transform(array_agg(distinct subject_name), x -> substr(x,1,2))

from lesson_plan  lp
left join subject sj on sj.subject_id = lp.subject_id
where student_id in (1537357,1537006,1537362,1537336,1537025)
group by lp.student_id
```

#### --例句???

```
select 

    count(distinct student_id )
from lesson_plan  lp
where cast(substr(lp.adjust_start_time,1,11) as date) >= date('2019-07-29')
and cast(substr(lp.adjust_start_time,1,11) as date) < current_date


select 
    count(student_id)
from 
(
select 
    distinct student_id
from  lesson_plan lp 
where cast(substr(lp.adjust_start_time,1,11) as date) >= date('2019-07-29')
and cast(substr(lp.adjust_start_time,1,11) as date) < current_date
)x

```
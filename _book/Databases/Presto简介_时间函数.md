# Presto简介

## Presto是什么

**Presto是由Facebook开发的分布式SQL 查询引擎，用来进行高速、实时的数据分析**

**Presto的产生是为了解决Hive的MapReduce模型太慢的问题**

**Presto是一个计算引擎，它不存储数据，通过丰富的Connector获取第三方的数据，并支持扩展**

> 注意点：查询引擎，非数据库，不存储数据,获取第三方的数据
>
> hive :（基于Hadoop的数据仓库工具）提供存储、查询

## Presto优点

**支持标准SQL，降低使用门槛**

**可以连接多种数据源，包括Hive、RDBMS（Mysql、Oracle、Tidb等）、Kafka、MongoDB、Redis等**

**一个低延迟高并发的内存计算引擎，相比Hive，执行效率要高很多**

> *注意点：连接多种数据源，内存计算*

## Presto模型

> 查询示例：*select \* from hive.dwd_db_hfjydb.view_tms_contract_payment a left join hive.dwd_db_hfjydb.view_tms_contract b on a.contract_id = b.contract_id*
>
> **Catalog:就是数据源。Hive，Mysql是数据源，Hive 和Mysql都是数据源类型，可以连接多个Hive和多个Mysql。**
>
> **Schema：相当于一个数据库实例，一个Schema包含多张数据表。**
>
> **Table：数据表，与一般意义上的数据库表相同。**

# Presto日期时间函数

## **时区转换**

> **格式: SELECT timestamp '2019-08-01 01:00 UTC' AT TIME ZONE 'America/Los_Angeles'**
>
> *UTC:格林威治时间/称世界统一时间、世界标准时间 比北京时间慢8个小时*

​    示例:SELECT now() AT TIME ZONE 'America/Los_Angeles -- 比北京慢15小时北京时间

## **当前日期时间**

> 函数 now()/ current_timestamp 返回timestamp with time zone**
>
> **current_date：返回当前日期，只包含年月日**
>
> **current_time: 返回time with time zone**
>
> 示例:SELECT NOW() "now",
>                       current_timestamp "current_timestamp" ,
>                  	 current_date "current_date",
>                  	 current_time "current_time"
>
> *注意:*
>
>  mysql:now()/sysdate(),curtime(),curdate()
>
> *presto sql:current_date,current_time,current_timestamp函数都没有括号*

## **时间格式转换**

**函数:cast(value AS type) → type 显式把value转换到type类型。**

*Presto SQL大的“特点”：完全不同的数据类型之间不能比较，相似的数据类型一般可以比较。 date与varchar完全不同,不可以比较*

> **cast('2019-08-01' as date),date('2019-08-01' )**
>
> **cast('2019-08-01 16:00:00.000' as TIMESTAMP)**
>
> **cast('2019-08-01 16:00:00.000' as date)** 报错 需要截取
>
> *注意:长转短需要截取,短转长会自动补齐*
>
> 示例:select current_date > cast('2019-07-31' as date) ;
>
> ​         select current_date > date'2019-07-31' ;
>
> ​		 select '2019-08-01' > '2019-07-31' ;
>
> ​    select substr(lp.adjust_start_time,1,10) ,lp.adjust_start_time
> ​      from dwd_db_hfjydb.lesson_plan lp
> ​    where substr(lp.adjust_start_time,1,10) = '2019-08-01' limit 1;

## **截取函数**

​    **date_trunc(unit, x) 返回x截取到单位unit之后的值**

> ### **函数 支持如下单位：**

```
    单位      Example Truncated Value
    second    2001-08-22 03:04:05.000
    minute    2001-08-22 03:04:00.000
    hour      2001-08-22 03:00:00.000
    day       2001-08-22 00:00:00.000
    week      2001-08-20 00:00:00.000
    month     2001-08-01 00:00:00.000
    quarter   2001-07-01 00:00:00.000
    year      2001-01-01 00:00:00.000
```

示例:select date_trunc('hour',current_timestamp);

​         select date_trunc('week',current_timestamp);

​		 select date_trunc('month',current_timestamp);

​		 select date_trunc('quarter',current_timestamp);

## **间隔函数**		

**date_add(unit, value, timestamp)**→ [same as input]

**在timestamp的基础上加上value个unit。如果想要执行相减的操作，可以通过将value赋值为负数来完成。**

函数支持如下所列的间隔单位：

```
    Unit       Description
    second     Seconds
    minute     Minutes
    hour       Hours
    day        Days
    week       Weeks
    month      Months
    quarter    Quarters of a year
    year       Years
```

示例: select date_add('day',1,now());

​		  select date_add('hour',-1,now());

​		  select date_add('quarter',1,now()); -- 增加一个季度即增加三个月	

## **时间差函数**

**date_diff(unit, timestamp1, timestamp2)**

**返回 (timestamp2 - timestamp1) 之后的值，该值的表示单位是unit.**

*注意:unit加引号 ,mysql 中 DATEDIFF(date1,date2) 是date1-date2*

示例:  select date_diff('hour', TIMESTAMP'2018-08-08 08:08:08', TIMESTAMP'2018-08-08 00:00:00') ;

​		   select date_diff('quarter', TIMESTAMP'2019-08-08 08:08:08', TIMESTAMP'2019-12-02 06:00:00.000') ;

## **日期格式化函数**

  **date_format(timestamp, format) → varchar**

  **使用format指定的格式，将timestamp格式化成字符串**



> ### **支持类型单位 **
>
> **注意:%D %U %u %V %X %w 暂不支持***
>
> ```
>     分类符    说明
>     %a    Abbreviated weekday name (Sun .. Sat)
>     %b    Abbreviated month name (Jan .. Dec)
>     %c    Month, numeric (0 .. 12)
>     %D    Day of the month with English suffix (0th, 1st, 2nd, 3rd, …)
>     %d    Day of the month, numeric (00 .. 31)
>     %e    Day of the month, numeric (0 .. 31)
>     %f    Fraction of second (6 digits for printing: 000000 .. 999000; 1 - 9 digits 		  for parsing: 0 .. 999999999)
>     %H    Hour (00 .. 23)
>     %h    Hour (01 .. 12)
>     %I    Hour (01 .. 12)
>     %i    Minutes, numeric (00 .. 59)
>     %j    Day of year (001 .. 366)
>     %k    Hour (0 .. 23)
>     %l    Hour (1 .. 12)
>     %M    Month name (January .. December)
>     %m    Month, numeric (00 .. 12)
>     %p    AM or PM
>     %r    Time, 12-hour (hh:mm:ss followed by AM or PM)
>     %S    Seconds (00 .. 59)
>     %s    Seconds (00 .. 59)
>     %T    Time, 24-hour (hh:mm:ss)
>     %U    Week (00 .. 53), where Sunday is the first day of the week
>     %u    Week (00 .. 53), where Monday is the first day of the week
>     %V    Week (01 .. 53), where Sunday is the first day of the week; used with %X
>     %v    Week (01 .. 53), where Monday is the first day of the week; used with %x
>     %W    Weekday name (Sunday .. Saturday)
>     %w    Day of the week (0 .. 6), where Sunday is the first day of the week
>     %X    Year for the week where Sunday is the first day of the week, numeric, four 		   digits; used with %V
>     %x    Year for the week, where Monday is the first day of the week, numeric, four 			digits; used with %v
>     %Y    Year, numeric, four digits
>     %y    Year, numeric (two digits)
>     %%    A literal % character
>     %x    x, for any x not listed above
> ```

示例:SELECT date_format(current_timestamp,'%Y-%m-%d %W %H:%i:%s') 



**date_parse(string, format) → timestamp**

**按照format指定的格式，将字符串string解析成timestamp**

*注意:两边形式要一样 date_parse('2019-08-01 ','%Y-%m-%d %H:%i:%s') 会报错*

示例: SELECT date_parse('2019-08-01 08:08:08','%Y-%m-%d %H:%i:%s');

## **抽取函数**

**extract(field FROM x)→ bigint(整数)**

**从x中返回域field**

**抽取函数支持的数据类型取决于需要抽取的域。大多数域都支持日期和时间类型。**

**可以使用抽取函数来抽取如下域： **

```
Field           Description
YEAR            year()
QUARTER         quarter()
MONTH           month()
WEEK            week()
DAY             day()
DAY_OF_MONTH    day() 
DAY_OF_WEEK      day_of_week()
DOW              day_of_week()
DAY_OF_YEAR      day_of_year()
DOY              day_of_year()
YEAR_OF_WEEK     year_of_week()
YOW              year_of_week()
HOUR             hour()
MINUTE           minute()
SECOND           second()
TIMEZONE_HOUR    timezone_hour() :表示时区偏移小时量
TIMEZONE_MINUTE  timezone_minute()
```

示例:  select extract(year FROM current_timestamp) ,extract(month from DATE'2019-08-01'),extract(DAY        		  FROM now()), extract(WEEK from now()),extract(doy FROM now());

​          select extract(TIMEZONE_HOUR FROM now()) "时区偏移小时量";

**便利的抽取函数**:

**格式**

```
    day(x) → bigint
    返回指定日期在当月的天数
    day_of_month(x) → bigint
    day(x)的另一种表述
    day_of_week(x) → bigint
    返回指定日期对应的星期值，值范围从1 (星期一) 到 7 (星期天).
    day_of_year(x) → bigint
    返回指定日期对应一年中的第几天，值范围从1到 366.
    dow(x) → bigint
    day_of_week()的另一种表达
    doy(x) → bigint
    day_of_year()的另一种表达
    hour(x) → bigint
    返回指定日期对应的小时，值范围从1到 23
    minute(x) → bigint
    返回指定日期对应的分钟
    month(x) → bigint
    返回指定日期对应的月份
    quarter(x) → bigint
    返回指定日期对应的季度，值范围从1到 4
    second(x) → bigint
    返回指定日期对应的秒
    timezone_hour(timestamp) → bigint
    返回从指定时间戳对应时区偏移的小时数
    timezone_minute(timestamp) → bigint
    返回从指定时间戳对应时区偏移的分钟数
    week(x) → bigint
    返回指定日期对应一年中的ISO week，值范围从1到 53
    week_of_year(x) → bigint
    week的另一种表述
    year(x) → bigint
    返回指定日期对应的年份
    year_of_week(x) → bigint
    返回指定日期对应的ISO week的年份
    yow(x) → bigint
    year_of_week()的另一种表达
```

**示例:select year(now()) ,month(now()),day(now()),doy(now()),quarter(now()),week(now());**



# 补充: sum() over()

**sum() over(PARTITION BY columnA order by columnB )** :类似于Python中 cumsum(),实现累计和功能

示例: `SELECT`
	`aa."部门",`
	`aa.date,`
	`aa."当月业绩",`
	`sum( aa."当月业绩" ) over ( PARTITION BY aa."部门" ORDER BY aa.date ) "累计和",`
	`sum( aa."当月业绩" ) over ( PARTITION BY aa."部门" ) "三天总业绩",`
	`cast(round( aa."当月业绩" * 100 / sum( aa."当月业绩" ) over ( PARTITION BY aa."部门" ), 2 ) AS VARCHAR ) || '%' "日占比"` 
`FROM`
	`(`
	`SELECT`
		`substr( sd.department_name, 1, 7 ) "部门",`
		`substr( tcp.pay_date, 1, 10 ) date,`
		`sum( tcp.sum / 100 ) "当月业绩"` 
	`FROM`
		`dwd_db_hfjydb.view_tms_contract_payment tcp`
		`LEFT JOIN dwd_db_hfjydb.view_tms_contract tc ON tc.contract_id = tcp.contract_id`
		`LEFT JOIN dwd_db_hfjydb.view_user_info ui ON ui.user_id = tc.submit_user_id`
		`LEFT JOIN dwd_db_hfjydb.sys_user_role sur ON ui.user_id = sur.user_id`
		`LEFT JOIN dwd_db_hfjydb.sys_role sr ON sur.role_id = sr.role_id`
		`LEFT JOIN dwd_db_hfjydb.sys_department sd ON sr.department_id = sd.department_id` 
	`WHERE`
		`substr( tcp.pay_date, 1, 10 ) >= '2019-07-01'` 
		`AND substr( tcp.pay_date, 1, 10 ) < '2019-07-04'` 
		`AND tc.STATUS NOT IN ( 7, 8 ) -- 剔除合同终止和废弃`
		`AND tcp.pay_status IN ( 2, 4 )` 
		`AND ui.account_type = 1` 
		`AND regexp_like ( sd.department_name, '江苏销售' )` 
		`AND sd.department_name NOT LIKE '%考核%'` 
	`GROUP BY 1,2` 
	`) aa` 

# 官方文档

http://prestodb.jd.com/docs/current/index.html*
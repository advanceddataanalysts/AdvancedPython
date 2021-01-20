

## 安装Airflow

[官方文档参考](http://airflow.apache.org/docs/apache-airflow/stable/index.html#)

```shell
1.直接pip3安装
pip3 install apache-airflow
安装好的airflow会在对应的python, 例如/usr/local/python3/bin/airflow
提前添加python环境变量

vim /etc/profile.d/python3_env
export PATH=${PATH}:/usr/local/python3/bin


2. 修改配置
安装好的airflow, 默认文件目录为当前用户的根目录下
cd ~/airflow
cp airflow.cfg airflow.cfg.bak
vim ~/airflow/airflow.cfg

一些需要修改的配置项:
(1). 日志位置
# The folder where airflow should store its log files
# This path must be absolute
base_log_folder = /data/logs/airflow/logs

# How often should stats be printed to the logs
print_stats_interval = 30

child_process_log_directory = /data/logs/airflow/logs/scheduler

(2). 时区设置
default_timezone = Asia/Shanghai
default_ui_timezone = Asia/Shanghai

在airflow包里修改  cd /usr/local/python3/lib/python3.7/site-packages/airflow/utils
vim airflow/utils/timezone.py
在 utc = pendulum.timezone('UTC') 这行(第27行)代码下添加
from airflow import configuration as conf  
# from airflow.configuration import conf    最新版的修改方式
try:
	tz = conf.get("core", "default_timezone")
	if tz == "system":
		utc = pendulum.local_timezone()
	else:
		utc = pendulum.timezone(tz)
except Exception:
	pass
	
修改utcnow()函数 (在第69行)
原代码 result = dt.datetime.utcnow() 
修改为 result = dt.datetime.now()


vim airflow/utils/sqlalchemy.py
在utc = pendulum.timezone(‘UTC’) 这行(第37行)代码下添加
from airflow import configuration as conf
# from airflow.configuration import conf    最新版的修改方式
try:
	tz = conf.get("core", "default_timezone")
	if tz == "system":
		utc = pendulum.local_timezone()
	else:
		utc = pendulum.timezone(tz)
except Exception:
	pass



(3). ip和端口号
# The ip specified when starting the web server
web_server_host = 0.0.0.0

# The port on which to run the web server
web_server_port = 8080

(4). 数据库连接
sql_alchemy_conn = mysql+pymysql://airflow:password@数据库地址:3306/airflow
(需要安装pymysql包, pip3 install pymysql)
创建airflow账号和密码和airflow数据库 (airflow_123)
create user 'airflow'@'%' identified by 'password';
grant all privileges on airflow.* to 'airflow'@'%';
flush privileges;
set global explicit_defaults_for_timestamp = 1;
create database airflow CHARACTER SET = utf8mb4;

(5). 加载dags文件的目录
dags_folder = /root/airflow/dags
(如果通过项目管理, 可以设置为项目对应的文件夹目录或者使用软连接
ln -s /home/data-machine-for-wh/src/airflow_dags  /root/airflow/dags)

(6). 设置调度执行器类型
executor = LocalExecutor
(注: CeleryExecutor 需要安装所需要的python包 redis, flower [pip3 install 'apache-airflow[celery]'], 且该版本与3.7的包冲突, 需要降低python版本为3.6方可使用; 启动方式为 airflow celery worker; airflow celery flower)
详情参照 http://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html

3. 初始化数据库
airflow db init

4. 创建admin账号
airflow users create  --username admin --firstname admin --lastname admin --role Admin --email admin@keenon.com
输入密码 admin

5. 启动airflow
airflow webserver (-D 以守护进程形式启动)
airflow scheduler (-D 以守护进程形式启动)

```


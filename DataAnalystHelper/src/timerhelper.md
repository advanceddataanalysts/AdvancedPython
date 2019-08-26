##### 创建任务依赖的项目表
```
##### 创建任务表
CREATE TABLE `will_timer_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `crontab` varchar(50) DEFAULT NULL,
  `crontab_desc` varchar(50) DEFAULT NULL,
  `syn_task` varchar(100) DEFAULT NULL,
  `sub_task` varchar(100) DEFAULT NULL,
  `guandata_uuid` varchar(2000) DEFAULT NULL,
  `file_des` varchar(100) DEFAULT NULL,
  `file_basename` varchar(100) NOT NULL,
  `model` varchar(50) DEFAULT 'timerTask',
  `next_run_time` datetime DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `elapse` int(11) DEFAULT NULL,
  `is_delete` int(1) DEFAULT '0',
  `xxl_task_id` int(11) DEFAULT NULL COMMENT 'xxl任务id',
  `author` varchar(50) DEFAULT NULL,
  `author_email` varchar(50) DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `emailpara` varchar(10000) DEFAULT NULL COMMENT '邮件参数',
  PRIMARY KEY (`id`,`file_basename`) USING BTREE,
  UNIQUE KEY `file_basename` (`file_basename`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=570 DEFAULT CHARSET=utf8;
```


```
##### 创建任务监控表
CREATE TABLE `will_timer_task_check` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_basename` varchar(50) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `elapse` int(11) DEFAULT NULL,
  `run_status` int(1) DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43207 DEFAULT CHARSET=utf8;
```
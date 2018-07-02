CREATE TABLE `collection_info_201801` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `monitor_name` varchar(20) NOT NULL DEFAULT '' COMMENT '监控类型名称',
  `monitor_ip` varchar(20) NOT NULL DEFAULT '' COMMENT '被监控ip',
  `http_code` int(11) unsigned NOT NULL DEFAULT '0' COMMENT 'http返回码',
  `exec_code` int(11) unsigned NOT NULL DEFAULT '99' COMMENT '执行api返回码 0 成功，1 命令错误， 2 执行失败',
  `api_info` varchar(255) DEFAULT NULL,
  `create_time` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '采集时间',
  `monitor_port` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '被监控port',
  PRIMARY KEY (`id`),
  KEY `indx_name_ip_port_ct` (`monitor_name`,`monitor_ip`,`monitor_port`,`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=203715 DEFAULT CHARSET=utf8 COMMENT='监控数据采集表';




CREATE TABLE `add_monitor_info` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `monitor_name` varchar(20) NOT NULL DEFAULT '' COMMENT '被监控名称',
  `monitor_ip` varchar(20) NOT NULL DEFAULT '' COMMENT '被监控ip',
  `monitor_port` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '被监控port',
  `admin` varchar(20) NOT NULL DEFAULT '' COMMENT '负责人',
  `business` varchar(20) NOT NULL DEFAULT '' COMMENT '业务',
  `first_error_time` varchar(20) NOT NULL DEFAULT '0.0' COMMENT '初次error时间',
  `on_off` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '监控开关 1:开 0:关',
  `create_time` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `indx_name_ip_port_onoff` (`monitor_name`,`monitor_ip`,`monitor_port`,`on_off`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COMMENT='添加监控表';



 CREATE TABLE `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(255) CHARACTER SET utf8mb4 NOT NULL DEFAULT '' COMMENT '用户名',
  `password_hash` varchar(255) CHARACTER SET utf8mb4 NOT NULL DEFAULT '' COMMENT '密码',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uix_name_pwd` (`name`,`password_hash`),
  UNIQUE KEY `ix_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13322 DEFAULT CHARSET=utf8 COMMENT='用户注册表';








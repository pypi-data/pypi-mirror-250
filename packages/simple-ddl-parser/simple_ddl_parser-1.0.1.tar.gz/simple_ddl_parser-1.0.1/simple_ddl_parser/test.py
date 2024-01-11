from simple_ddl_parser import DDLParser

ddl = r"""
    CREATE TABLE `employee` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) NOT NULL,
  `authority` int(11) DEFAULT '1' COMMENT 'user auth',
  PRIMARY KEY (`user_id`),
  KEY `FK_authority` (`user_id`,`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
    """
result = DDLParser(ddl).run(group_by_type=True, output_mode="mysql")

import pprint

pprint.pprint(result)
from sqlAlchemySession import SqlAlchemySession

def InitSession(info):
	return SqlAlchemySession(info["database_controller"] + '://' + info["database_user"]  + ":" + info["database_pass"] + "@" + info["database_ip"] + ":" + info["database_port"] + "/" + info["database_name"])
#Session = SqlAlchemySession('mysql://root:root@dev2.sx4it.com:42162/sx4it')

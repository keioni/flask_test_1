# -*- coding: utf-8 -*-

import configparser

CONF = configparser.ConfigParser()
CONF.read('./sys/settings.cfg', 'utf-8')

# configurations
CONF.salt = 'oajokkN6AkwZB4wA0XpFtzlJpYYTVB7a9JkjV56PMAs'
CONF.validation_timeout_in_sec = 3600
CONF.db_connect_string = 'sqlite:///cyreco/db/userlist.sqlite3'
CONF.debug_sql_print = True

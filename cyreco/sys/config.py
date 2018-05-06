# -*- coding: utf-8 -*-

import configparser

class CyrecoConfigParser(configparser.ConfigParser):
    salt = 'oajokkN6AkwZB4wA0XpFtzlJpYYTVB7a9JkjV56PMAs'
    validation_timeout_in_sec = 3600
    db_connect_string = 'sqlite:///cyreco/db/userlist.sqlite3'
    debug_sql_print = True


CONF = CyrecoConfigParser()
CONF.read('./sys/settings.cfg', 'utf-8')

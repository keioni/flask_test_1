# -*- coding: utf-8 -*-

import configparser

CONF = configparser.ConfigParser()
CONF.read('./settings.cfg', 'utf-8')

# configurations
CONF.salt = 'oajokkN6AkwZB4wA0XpFtzlJpYYTVB7a9JkjV56PMAs'
CONF.validation_timeout_in_sec = 3600
CONF.db_connect_string = 'sqlite:///userlist.sqlite3'

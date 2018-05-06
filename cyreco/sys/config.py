# -*- coding: utf-8 -*-

import configparser

conf = configparser.ConfigParser()
conf.read('./settings.cfg', 'utf-8')

conf.salt = conf['Securities']['encode_salt']

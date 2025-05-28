#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Log:
    """Log util"""

    @staticmethod
    def info(msg):
        print('\033[1;30;50m' + str(msg) + '\033[0m')

    @staticmethod
    def error(msg):
        print('\033[1;31;50m' + str(msg) + '\033[0m')
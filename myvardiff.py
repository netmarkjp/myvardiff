#!/usr/bin/env python
#coding: utf-8

"""myvardiff - diff mysql variables to dumped variables(json, dumped by myvardump)

https://github.com/netmarkjp/myvardiff

This program was inspired by myprofiler( https://github.com/methane/myprofiler )
"""

import os
import sys
import json
from ConfigParser import SafeConfigParser
from optparse import OptionParser

try:
    # MySQL-python
    import MySQLdb
    from MySQLdb.cursors import DictCursor
except ImportError:
    try:
        # PyMySQL
        import pymysql as MySQLdb
        from pymysql.cursors import DictCursor
    except ImportError:
        print "Please install MySQLdb(MySQL-python) or PyMySQL"
        sys.exit(1)


def connect(conf='~/.my.cnf', section='DEFAULT'):
    """
    connect to MySQL from conf file.
    """
    parser = SafeConfigParser()
    parser.read([os.path.expanduser(conf)])

    args = {}

    if parser.has_option(section, 'socket'):
        args['unix_socket'] = parser.get(section, 'socket')
    else:
        args['host'] = parser.get(section, 'host')
        if parser.has_option(section, 'port'):
            args['port'] = int(parser.get(section, 'port'))
    args['user'] = parser.get(section, 'user')
    args['passwd'] = parser.get(section, 'password')
    args['charset'] = 'utf8'
    return MySQLdb.connect(**args)


def variables(con):
    cur = con.cursor(DictCursor)
    cur.execute("show global variables")
    for row in cur.fetchall():
        if row['Variable_name'] is None:
            continue
        if row['Value'] is None:
            continue
        yield row


def build_option_parser():
    parser = OptionParser()
    parser.add_option(
        '-c', '--config',
        help="read MySQL configuration from. (default: '~/.my.cnf'",
        default='~/.my.cnf'
    )
    parser.add_option(
        '-s', '--section',
        help="read MySQL configuration from this section. (default: '[DEFAULT]')",
        default="DEFAULT"
    )
    parser.add_option(
        '--before',
        help="dumped json filename by myvardump.py (default: 'myvardump.json')",
        default="myvardump.json"
    )
    return parser


def main():
    parser = build_option_parser()
    opts, args = parser.parse_args()

    try:
        con = connect(opts.config, opts.section)
    except Exception, e:
        parser.error(e)

    values = dict()
    for variable in variables(con):
        values.update({variable['Variable_name']: variable['Value']})
    con.close()

    for k, v in json.load(open(opts.before)).iteritems():
        if k not in values:
            print "%s missing" % k
        elif v != values[k]:
            print "%s:\t%s -> %s" % (k, v, values[k])


if __name__ == '__main__':
    main()

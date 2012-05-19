# -*- coding: utf-8 -*-
# Open Source Initiative OSI - The MIT License (MIT):Licensing
#
# The MIT License (MIT)
# Copyright (c) 2012 sx4it (contact@sx4it.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import ConfigParser

class MissingOptionError(Exception):
    """
    This exception is thrown when the server.conf file is invalid.
    You can print the message to get more informations.
    """
    def __init__(self, key):
        self.key = key
    def __str__(self):
        return 'No {0} specified, correct your configurationf file or your command \
             line.'.format((self.key))

class InvalidOptionError(Exception):
    pass

class AmConfigParser(ConfigParser.RawConfigParser):
    """
    A simple configuration class.
    """
    def __init__(self, args):
        self._args = args
        self._dburl = None
        ConfigParser.RawConfigParser.__init__(self)

    def _getdboption(self, name, default=None):
        cmdline = getattr(self._args, 'database_' + name)
        if cmdline:
            return cmdline
        else:
            try:
                return self.get('database', name)
            except ConfigParser.NoOptionError:
                if default:
                    return default
        raise MissingOptionError('database ' + name)
                

    def getdburl(self):
        if not self._dburl:
            dbdriver = self._getdboption('driver', 'mysql')
            if dbdriver not in frozenset(['mysql', 'postgresql']):
                raise InvalidOptionError('The only database drivers supported are \
mysql an    d postgresql.')
            if dbdriver == 'mysql':
                defport = '3306'
            elif dbdriver == 'postgresql':
                defport = '5432'
            self._dburl = dbdriver + '://'
            self._dburl += self._getdboption('user')
            self._dburl += ':'
            self._dburl += self._getdboption('pass')
            self._dburl += '@'
            self._dburl += self._getdboption('ip', '127.0.0.1')
            self._dburl += ':'
            self._dburl += self._getdboption('port', defport)
            self._dburl += '/'
            self._dburl += self._getdboption('name', '4am')
        return self._dburl

    def getdebug(self):
        if hasattr(self._args, 'debug'):
            return True
        try:
            if self.getboolean('default', 'debug'):
                return True
        except ConfigParser.NoOptionError:
            pass
        return False

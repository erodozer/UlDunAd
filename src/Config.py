#=======================================================#
#
# UlDunAd - Ultimate Dungeon Adventure
# Copyright (C) 2009 Blazingamer/n_hydock@comcast.net
#       http://code.google.com/p/uldunad/
# Licensed under the GNU General Public License V3
#      http://www.gnu.org/licenses/gpl.html
#
#=======================================================#

from ConfigParser import SafeConfigParser
from StringIO import StringIO

import os
import sys

class Configuration:
    def __init__ (self, fileName):
        self.parser = SafeConfigParser()
        self.fileName = fileName
        self.revert()

    def __getattr__ (self, name, type = None):
        return Section(name, self.parser, type)

    def __delattr__ (self, name):
        if self.parser.has_section(name):
            self.parser.remove_section(name)
        else:
            raise AttributeError, 'No section "%s".' % name

    def __repr__ (self):
        return '<Configuration from %s>' % self.fileName

    def __str__ (self):
        result = '; <Configuration from %s>\n' % self.fileName
        sio = StringIO()
        self.parser.write(sio)
        result += sio.getvalue()
        sio.close()
        return result

    def save (self):
        self.parser.write(open(os.path.join(self.fileName), 'w'))

    def revert (self):
        for section in self.parser.sections():
            self.parser.remove_section(section)
        self.parser.read(os.path.join(self.fileName))


class Section:
    def __init__ (self, name, parser, type):
        self.name = name
        self.parser = parser

    def __getattr__ (self, name, type = None):
        if not self.parser.has_section(self.name):
            raise AttributeError, 'No section "%s".' % self.name
        if self.parser.has_option(self.name, name):
            if type == "int":
              return self.parser.getint(self.name, name)
            elif type == "float":
              return self.parser.getfloat(self.name, name)
            elif type == "bool":
              return self.parser.getboolean(self.name, name)
            else:
              return self.parser.get(self.name, name)
        else:
            raise AttributeError, 'No option "%s" in section "%s".' % (name, self.name)

    def __setattr__ (self, name, value):
        if name in ('name', 'parser') or name.startswith('__'):
            self.__dict__[name] = value
            return
        if not self.parser.has_section(self.name):
            self.parser.add_section(self.name)
        self.parser.set(self.name, name, str(value))

    def __delattr__ (self, name):
        if not self.parser.has_section(self.name):
            raise AttributeError, 'No section "%s".' % self.name
        if self.parser.has_option(self.name, name):
            self.parser.remove_option(self.name, name)
        else:
            raise AttributeError, 'No option "%s" in section "%s".' % (name, self.name)

#####################################################################
# -*- coding: iso-8859-1 -*-                                        #
#                                                                   #
# UlDunAd - Ultimate Dungeon Adventure                              #
# Copyright (C) 2009 Blazingamer(n_hydock@comcast.net               #
#                                                                   #
# This program is free software; you can redistribute it and/or     #
# modify it under the terms of the GNU General Public License       #
# as published by the Free Software Foundation; either version 3    #
# of the License, or (at your option) any later version.            #
#                                                                   #
# This program is distributed in the hope that it will be useful,   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of    #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the     #
# GNU General Public License for more details.                      #
#                                                                   #
# You should have received a copy of the GNU General Public License #
# along with this program; if not, write to the Free Software       #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,        #
# MA  02110-1301, USA.                                              #
#####################################################################

from ConfigParser import SafeConfigParser
from StringIO import StringIO

class Configuration:
    def __init__ (self, fileName):
        self.parser = SafeConfigParser()
        self.fileName = fileName
        self.revert()

    def __getattr__ (self, name):
        return Section(name, self.parser)

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
        self.parser.write(open(self.fileName, 'w'))

    def revert (self):
        for section in self.parser.sections():
            self.parser.remove_section(section)
        self.parser.read(self.fileName)


class Section:
    def __init__ (self, name, parser):
        self.name = name
        self.parser = parser

    def __getattr__ (self, name):
        if not self.parser.has_section(self.name):
            raise AttributeError, 'No section "%s".' % self.name
        if self.parser.has_option(self.name, name):
            return self.parser.get(self.name, name)
        else:
            raise AttributeError, 'No option "%s" in section "%s".' % (name, self.name)

    def __setattr__ (self, name, value):
        if name in ('name', 'parser') or name.startswith('__'):
            self.__dict__[name] = value
            return
        if not self.parser.has_section(self.name):
            self.parser.add_section(self.name)
        self.parser.set(self.name, name, value)

    def __delattr__ (self, name):
        if not self.parser.has_section(self.name):
            raise AttributeError, 'No section "%s".' % self.name
        if self.parser.has_option(self.name, name):
            self.parser.remove_option(self.name, name)
        else:
            raise AttributeError, 'No option "%s" in section "%s".' % (name, self.name)

# -*- mode: python; coding: utf-8 -*-

# Copyright © 2017 by Jeffrey C. Ollie <jeff@ocjtech.us>
#
# This file is part of Nest Exporter.
#
# Nest Exporter is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Nest Exporter is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Nest Exporter.  If not, see
# <http://www.gnu.org/licenses/>.

from twisted.logger import Logger
from twisted.web.resource import Resource

class RootPage(Resource):
    log = Logger()

    def __init__(self, reactor):
        Resource.__init__(self)
        self.reactor = reactor

    def getChild(self, name, request):
        if name == b'':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        request.setHeader(b'Content-Type', b'text/plain; charset=utf-8')
        return b'OK'

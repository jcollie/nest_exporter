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

import argparse
import os
import sys

from twisted.internet import reactor
from twisted.logger import globalLogBeginner
from twisted.logger import textFileLogObserver
from twisted.logger import Logger

from .main import Main
from ._version import __version__

default_endpoint = 'tcp:9264'

def cli():
    log = Logger()

    parser = argparse.ArgumentParser(prog = __version__.package)

    parser.add_argument('--version', action = 'version', version = __version__.public())
    parser.add_argument('--secrets', help = 'Directory that contains files named "username" and "password". These files should contain your Nest username and password.')
    parser.add_argument('--username', help = 'Your Nest username.')
    parser.add_argument('--password', help = 'Your Nest password.')
    parser.add_argument('--endpoint', default = default_endpoint, help = 'Twisted endpoint declaration for internal web service. Default is "{}".'.format(default_endpoint))

    options = parser.parse_args()

    output = textFileLogObserver(sys.stderr)
    globalLogBeginner.beginLoggingTo([output])

    username = None
    password = None

    if options.secrets is not None:
        if not os.path.isdir(options.secrets):
            log.critical('{secrets:} is not a directory', secrets = options.secrets)
            sys.exit(1)

        username_file = os.path.join(options.secrets, 'username')
        password_file = os.path.join(options.secrets, 'password')

        try:
            with open(username_file, mode = 'r', encoding = 'utf-8') as f:
                username = f.read().strip()

        except FileNotFoundError:
            log.error('Secrets path specified but username file {username_file:} not found!', username_file = username_file)

        except PermissionError:
            log.error('Unable to open username file {username_file:} for reading!', username_file = username_file)

        try:
            with open(password_file, mode = 'r', encoding = 'utf-8') as f:
                password = f.read().strip()

        except FileNotFoundError:
            log.error('Secrets path specified but password file {password_file:} not found!', password_file = password_file)

        except PermissionError:
            log.error('Unable to open password file {password_file:} for reading!', password_file = password_file)

    if options.username is not None:
        username = options.username

    if options.password is not None:
        password = options.password

    if username is None:
        log.critical('Username must be specified!')
        sys.exit(1)

    if password is None:
        log.critical('Password must be specified!')
        sys.exit(1)

    m = Main(reactor, username, password, options.endpoint)
    reactor.run()

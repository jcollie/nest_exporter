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

from setuptools import setup, find_packages

setup(
    name = 'nest_exporter',
    use_incremental = True,
    setup_requires = ['incremental'],
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['incremental',
                        'Twisted[tls]',
                        'python-nest < 3.0'],
    entry_points = {'console_scripts':
                    ['nest_exporter = nest_exporter.cli:cli']},
    author = 'Jeffrey C. Ollie',
    author_email = 'jeff@ocjtech.us',
    description = 'Export metrics from Nest to Prometheus',
    license = 'GPLv3',
    keywords = 'nest prometheus',
    url = 'https://github.com/jcollie/nest_exporter'
)

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

import sys

from nest import Nest

from requests.exceptions import HTTPError

from twisted.internet.threads import deferToThread
from twisted.logger import Logger
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.python.failure import Failure

class MetricsPage(Resource):
    log = Logger()
    isLeaf = True

    def __init__(self, reactor, username, password):
        Resource.__init__(self)
        self.reactor = reactor
        self.username = username
        self.password = password
        self.nest = None

    def render_GET(self, request):
        d = deferToThread(self.get_statistics)
        d.addCallback(self.send_results, request)
        return NOT_DONE_YET

    def get_statistics(self):
        try:
            if self.nest is None:
                self.nest = Nest(self.username, self.password)

            self.nest._bust_cache()

            results = ['# HELP nest_up Are we communicating properly with the Nest API?\n',
                       '# TYPE nest_up gauge\n',
                       'nest_up 1\n']

            results.append('# TYPE nest_structure gauge\n')
            for structure in self.nest.structures:
                results.append('nest_structure{{structure="{}"}} 1\n'.format(structure.name))

            results.append('# TYPE nest_structure_away gauge\n')
            for structure in self.nest.structures:
                if structure.away:
                    results.append('nest_structure_away{{structure="{}"}} 1\n'.format(structure.name))
                else:
                    results.append('nest_structure_away{{structure="{}"}} 0\n'.format(structure.name))

            results.append('# TYPE nest_thermostat gauge\n')
            for structure in self.nest.structures:
                for device in structure.devices:
                    results.append('nest_thermostat{{structure="{}",device="{}"}} 1\n'.format(structure.name, device.name))

            results.append('# HELP nest_thermostat_current_temperature_celcius Current temperature at the Nest thermostat\n')
            results.append('# TYPE nest_thermostat_current_temperature_celcius gauge\n')
            for structure in self.nest.structures:
                for device in structure.devices:
                    results.append('nest_thermostat_current_temperature_celcius{{structure="{}",device="{}"}} {}\n'.format(structure.name, device.name, device.temperature))

            results.append('# HELP nest_thermostat_target_temperature_celcius Target temperature of the Nest thermostat\n')
            results.append('# TYPE nest_thermostat_target_temperature_celcius gauge\n')
            for structure in self.nest.structures:
                for device in structure.devices:
                    results.append('nest_thermostat_target_temperature_celcius{{structure="{}",device="{}"}} {}\n'.format(structure.name, device.name, device.target))

            #results.append('# HELP nest_thermostat_exterior_temperature_celcius Exterior temperature at the Nest thermostat\n')
            #results.append('# TYPE nest_thermostat_exterior_temperature_celcius gauge\n')
            #for structure in self.nest.structures:
            #    for device in structure.devices:
            #        results.append('nest_thermostat_exterior_temperature_celcius{{structure="{}",device="{}"}} {}\n'.format(structure.name, device.name, device.weather.current.temperature))

            results.append('# HELP nest_thermostat_current_humidity Current humidity at the Nest thermostat\n')
            results.append('# TYPE nest_thermostat_current_humidity gauge\n')
            for structure in self.nest.structures:
                for device in structure.devices:
                    results.append('nest_thermostat_current_humidity{{structure="{}",device="{}"}} {}\n'.format(structure.name, device.name, device.humidity))

            results.append('# HELP nest_thermostat_target_humidity Target humidity of the Nest thermostat\n')
            results.append('# TYPE nest_thermostat_target_humidity gauge\n')
            for structure in self.nest.structures:
                for device in structure.devices:
                    results.append('nest_thermostat_target_humidity{{structure="{}",device="{}"}} {}\n'.format(structure.name, device.name, device.target_humidity))

            results.append('# HELP nest_thermostat_fan_state Fan state\n')
            results.append('# TYPE nest_thermostat_fan_state gauge\n')
            for structure in self.nest.structures:
                for device in structure.devices:
                    if device.fan:
                        results.append('nest_thermostat_fan_state{{structure="{}",device="{}"}} 1\n'.format(structure.name, device.name))
                    else:
                        results.append('nest_thermostat_fan_state{{structure="{}",device="{}"}} 0\n'.format(structure.name, device.name))

            results.append('# HELP nest_thermostat_ac_state Air conditioning state\n')
            results.append('# TYPE nest_thermostat_ac_state gauge\n')
            for structure in self.nest.structures:
                for device in structure.devices:
                    if device.hvac_ac_state:
                        results.append('nest_thermostat_ac_state{{structure="{}",device="{}"}} 1\n'.format(structure.name, device.name))
                    else:
                        results.append('nest_thermostat_ac_state{{structure="{}",device="{}"}} 0\n'.format(structure.name, device.name))

            results.append('# HELP nest_thermostat_heater_state Heater conditioning state\n')
            results.append('# TYPE nest_thermostat_heater_state gauge\n')
            for structure in self.nest.structures:
                for device in structure.devices:
                    if device.hvac_heater_state:
                        results.append('nest_thermostat_heater_state{{structure="{}",device="{}"}} 1\n'.format(structure.name, device.name))
                    else:
                        results.append('nest_thermostat_heater_state{{structure="{}",device="{}"}} 0\n'.format(structure.name, device.name))

        except HTTPError as error:
            self.reactor.callFromThread(self.log.error, 'Nest API error: {error:}', error = error.args[0])
            results = ['nest_up 0\n']

        return results

    def send_results(self, results, request):
        request.setHeader(b'Content-Type', b'text/plain; charset=utf-8; version=0.0.4')
        for result in results:
            request.write(result.encode('utf-8'))
        request.finish()

# -*- mode: python; coding: utf-8 -*-

from twisted.logger import Logger
from twisted.web.server import Site
from twisted.internet.endpoints import serverFromString

from .root import RootPage
from .metrics import MetricsPage

class Main(object):
    log = Logger()

    def __init__(self, reactor, username, password, endpoint):
        self.reactor = reactor
        self.username = username
        self.password = password
        self.endpoint = endpoint

        self.reactor.callWhenRunning(self.start)

    def start(self):
        self.metrics = MetricsPage(self.reactor, self.username, self.password)
        self.root = RootPage(self.reactor)
        self.root.putChild(b'metrics', self.metrics)
        self.site = Site(self.root)
        #self.site.noisy = False

        endpoint = serverFromString(self.reactor, self.endpoint)
        endpoint.listen(self.site)

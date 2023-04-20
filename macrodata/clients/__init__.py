#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from ..logs import logHeader

from .bcb import Client as bcbClient
from .bea import Client as beaClient
from .bls import Client as blsClient
from .can import Client as canClient
from .census import Client as censusClient
from .eurostat import Client as ecClient
from .fed import Client as fedClient
from .fred import Client as fredClient
from .inegi import Client as inegiClient
from .ons import Client as onsClient
from .modules import (Yahoo as yahooClient,
                      Treasury as treasuryClient,
                      Manual as manualClient)

from .utils import isEndOfMonth

logger = logging.getLogger(__name__)
logger.debug(logHeader)

__all__ = ['bcbClient',
           'beaClient',
           'blsClient',
           'canClient', 
           'censusClient', 
           'ecClient', 
           'fedClient',
           'fredClient',
           'inegiClient',
           'onsClient',
           'yahooClient',
           'treasuryClient',
           'manualClient'
]
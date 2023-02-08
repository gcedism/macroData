#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config
from .logs import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

__version__ = '0.3.0'
__author__ = 'Gabriel Cedismondi'

from .explorer import Explorer
from .manager import Manager

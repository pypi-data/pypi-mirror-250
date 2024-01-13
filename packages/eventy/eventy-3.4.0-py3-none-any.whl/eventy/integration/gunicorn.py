"""
Gunicorn integration utilities

Utility functions to integrate the eventy protocol in gunicorn servers.

You need to install gunicorn optional dependencies ("pip install eventy[gunicorn]").
"""

import logging

from gunicorn.glogging import Logger as GLogger


class Logger(GLogger):
    def setup(self, cfg):
        super().setup(cfg)
        self.error_log.handlers = logging.getLogger().handlers
        self.access_log.handlers = logging.getLogger().handlers

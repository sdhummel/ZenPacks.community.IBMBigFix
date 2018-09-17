# Logging
import logging
LOG = logging.getLogger('zen.IBMBigFix')

# Declare our imports
import time

# Twisted Imports
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web.client import getPage

# PythonCollector Imports
from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource import (
    PythonDataSourcePlugin,
    )

class FillDBFileSize(PythonDataSourcePlugin):

    """BigFix FillDB File Size data source plugin."""

    @classmethod
    def config_key(cls, datasource, context):
        return (
            context.device().id,
            datasource.getCycleTime(context),
            context.id,
            'filldb-filesize',
            )

    @classmethod
    def params(cls, datasource, context):
        return {
            'diag_page': zBigFixDiagnosticURL,
            }

    @inlineCallbacks
    def collect(self, config):
        data = self.new_data()

        for datasource in config.datasources:
            try:
                response = yield getPage('diag_page', timeout=3).text
                fs_start = 'FillDB File Size Limit:</div><div class="forminput">'
                fs_end = '% ( '
                fs = html.split(fs_start)[-1].split(fs_end)[0]
                fs=float(fs)

                response = fs(response)
            except Exception:
                LOG.exception(
                    "%s: failed to get alerts data for %s"
                    )

                continue

        returnValue(data)
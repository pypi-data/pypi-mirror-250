import logging

import gunicorn.app.base
import uvicorn
from gunicorn import glogging
from intelliw.utils.colorlog import ColoredFormatter
from intelliw.utils.logger import _get_framework_logger, get_logger


def default_config(bind, workers=None):
    config = {
        'bind': bind,
        'accesslog': '-', 'errorlog': '-',
        'loglevel': 'info',
        'timeout': 6000,
        'workers': workers or 1,
        'worker_class': 'uvicorn.workers.UvicornWorker',
        'logger_class': CustomLogger
    }
    return config


class CustomLogger(glogging.Logger):
    """Custom logger for Gunicorn log messages."""

    def setup(self, cfg):
        """Configure Gunicorn application logging configuration."""
        super().setup(cfg)

        format_string = '%(log_color)s[%(process)d] -System Log-  %(asctime)s | %(levelname)4s | %(message)4s'

        # Override Gunicorn's `error_log` configuration.
        self._set_handler(
            self.error_log, cfg.errorlog, ColoredFormatter(
                format_string))
        self._set_handler(
            self.access_log, cfg.accesslog, ColoredFormatter(
                format_string))


class UvicornServer:

    def __init__(self, app, host='0.0.0.0', port=8888, workers=None):
        config = uvicorn.Config(
            app,
            host=host,
            port=int(port),
            workers=workers
        )
        self.server = uvicorn.Server(config)
        self.init_logger()

    @staticmethod
    def init_logger():
        LOGGER_NAMES = ("uvicorn", "uvicorn.access",)
        for logger_name in LOGGER_NAMES:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = logging.getLogger().handlers

    def run(self):
        self.server.run()


class GunServer(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None, logger=None):
        self.options = options or {}
        self.application = app
        self.logger = logger
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

    def run(self):
        super().run()


if __name__ == '__main__':
    # options = {
    #     'bind': '%s:%s' % ('127.0.0.1', '8080'),
    #     'workers': number_of_workers(),
    # }
    # StandaloneApplication(handler_app, options).run()
    pass

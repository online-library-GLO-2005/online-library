import logging


## Mainly for DB health check
class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return "GET /health" not in record.getMessage()


def configure_logging():
    log = logging.getLogger("werkzeug")

    ## Mainly for DB health check
    log.addFilter(HealthCheckFilter())

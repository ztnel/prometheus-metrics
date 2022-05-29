
import random
import time
import logging
from prometheus_client import Gauge, start_http_server, Summary

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


# Create a metric to track time spent and requests made.
rt = Summary(
    'request_processing_seconds',
    'Time spent processing request'
)
g = Gauge(
    'temperature',
    'Temperature metric'
)

# Decorate function with metric.


@rt.time()
def process_request(t):
    """A dummy function that takes some time."""
    _logger.info("Sleeping for %s", t)
    time.sleep(t)


def get_temperature() -> float:
    """
    temperature endpoint
    """
    temp = random.uniform(0.0, 40.0)
    g.set(temp)
    return temp


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        _logger.info("Processing request")
        process_request(random.random())
        temp = get_temperature()
        _logger.info("Temperature: %s", temp)

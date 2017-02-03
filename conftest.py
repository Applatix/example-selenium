import logging
import sys

import pytest

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logger = logging.getLogger(__name__)

logging.basicConfig(format="%(asctime)s.%(msecs)03d %(levelname)s %(name)s %(threadName)s: %(message)s",
                    datefmt="%Y-%m-%dT%H:%M:%S",
                    level=logging.INFO,
                    stream=sys.stdout)


def pytest_addoption(parser):
    parser.addoption('--remote', action='store', default=None,
                     help='IP or hostname of selenium webdriver server')
    parser.addoption("--platform", action="store", default=None,
                     help='The name of the selenium image')


@pytest.fixture
def driver(request):
    remote = request.config.getoption("--remote")
    platform = request.config.getoption("--platform")

    logger.info('Selenium remote is %s', remote)
    logger.info('Test with platform %s', platform)

    if 'chrome' in platform.lower():
        dc_browser = DesiredCapabilities.CHROME
    elif 'firefox' in platform.lower():
        dc_browser = DesiredCapabilities.FIREFOX
    else:
        raise NotImplementedError
    selenium_driver = webdriver.Remote(command_executor='http://{}:4444/wd/hub'.format(remote),
                                       desired_capabilities=dc_browser)
    yield selenium_driver
    selenium_driver.close()

#! /usr/bin/env python

import logging
import sys

import pytest

logger = logging.getLogger(__name__)

logging.basicConfig(format="%(asctime)s.%(msecs)03d %(levelname)s %(name)s %(threadName)s: %(message)s",
                    datefmt="%Y-%m-%dT%H:%M:%S",
                    level=logging.INFO,
                    stream=sys.stdout)


def test_title_in_google(driver):
    driver.get('http://www.google.com')
    logger.info('Test Google.com title')
    assert 'Google' in driver.title
    logger.info('Test Pass')


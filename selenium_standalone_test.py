#! /usr/bin/env python

import argparse
import logging
import sys

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logger = logging.getLogger('selenium_test')


def init_driver(remote, browser):
    logger.info('Selenium remote is %s', remote)
    logger.info('Test %s', browser)
    if browser.lower() == 'chrome':
        dc_browser = DesiredCapabilities.CHROME
    elif browser.lower() == 'firefox':
        dc_browser = DesiredCapabilities.FIREFOX
    else:
        raise NotImplementedError
    return webdriver.Remote(command_executor='http://{}:4444/wd/hub'.format(remote),
                            desired_capabilities=dc_browser)


def test_title_in_google(driver):
    driver.get('http://www.google.com')
    logger.info('Test Google.com title')
    assert 'Google' in driver.title
    logger.info('Test Pass')


def test_title_in_python_org(driver):
    driver.get('http://www.python.org')
    logger.info('Test python.org title')
    assert 'Python' in driver.title
    logger.info('Test Pass')


def main():
    parser = argparse.ArgumentParser(description="Perform key/value insertion and retrieval ")
    parser.add_argument('--remote', required=True)
    parser.add_argument('--browser', required=True)
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout,
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                        datefmt="%Y-%m-%dT%H:%M:%S")

    driver = init_driver(args.remote, args.browser)
    test_title_in_google(driver)
    test_title_in_python_org(driver)


if __name__ == '__main__':
    main()
#! /usr/bin/env python

import argparse
import logging
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger('selenium_test')


def init_driver(remote, browser):
    logger.info('Selenium remote is %s', remote)
    logger.info('Test with browser %s', browser)
    if browser.lower() == 'chrome':
        dc_browser = DesiredCapabilities.CHROME
    elif browser.lower() == 'firefox':
        dc_browser = DesiredCapabilities.FIREFOX
    else:
        raise NotImplementedError
    return webdriver.Remote(command_executor='http://{}:4444/wd/hub'.format(remote),
                            desired_capabilities=dc_browser)


def save_screenshot(driver, file_name, msg=''):
    screenshot_dir = '/tmp/screenshot'
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    screenshot_path = os.path.join(screenshot_dir, file_name)
    ret = driver.get_screenshot_as_file(screenshot_path)
    if ret:
        logger.info('Save %s at "%s"', msg, screenshot_path)


def test_title_in_google(driver):
    driver.get('http://www.google.com')
    logger.info('Test Google.com title')
    assert 'Google' in driver.title
    save_screenshot(driver, 'google', msg='Google Homepage')
    logger.info('Test Pass')


def test_title_in_python_org(driver):
    driver.get('http://www.python.org')
    logger.info('Test python.org title')
    assert 'Python' in driver.title
    save_screenshot(driver, 'python', msg='Python Homepage')
    logger.info('Test Pass')


def test_search_applatix(driver):
    wait = WebDriverWait(driver, 30)

    logger.info('Go to www.google.com')
    driver.get('http://www.google.com')

    logger.info('Search for "applatix"')
    elem = driver.find_element_by_name('q')
    elem.send_keys('applatix')
    elem.send_keys(Keys.RETURN)
    wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,'Applatix')))

    logger.info('Go to Applatix Homepage')
    applatix_elem = driver.find_element_by_partial_link_text('Applatix')
    applatix_elem.click()
    wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'About')))

    logger.info('Go to Applatix About page')
    about_elem = driver.find_element_by_partial_link_text('About')
    about_elem.click()

    logger.info('Search Applatix Mission')
    mission_selector = '#u11931'
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, mission_selector)))
    try:
        mission_elem = driver.find_element_by_css_selector(mission_selector)
        mission = mission_elem.text.strip()
        if not mission:
            save_screenshot(driver, 'failure', msg='failure')
            logger.info('Test Fail')
            return
        else:
            logger.info('Applatix Inc. Mission: " %s "', mission)
    except Exception:
        save_screenshot(driver, 'failure', msg='failure')
        logger.info('Test Failure')
        return

    save_screenshot(driver, 'mission', msg='Applatix Mission')
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
    try:
        test_search_applatix(driver)
        logger.info('\n')
        logger.info('='* 50)
        test_title_in_google(driver)
        logger.info('\n')
        logger.info('='* 50)
        test_title_in_python_org(driver)
        logger.info('\n')
        logger.info('='* 50)
    except Exception as exc:
        logger.info(exc)
        save_screenshot(driver, 'crash', msg='crash')
    finally:
        logger.info('Closing Selenium Webdriver')
        driver.close()


if __name__ == '__main__':
    main()

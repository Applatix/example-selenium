## Selenium Test Example

This repository contains example test code and service templates which leverage Applatix `Dynamic Fixtures` feature to run 
selenium tests.

There are few service templates in this example:

#### Selenium Standalone Remote Mode:
Selenium node and selenium test code are running in different containers. The connection between test code and selenium node is through Selenium WebDriver remote API.

Service Templates:

* selenium_firefox.yaml
* selenium_chrome.yaml
* selenium_standalone.yaml

#### Selenium Grid
There is one selenium hub, and linked with many selenium nodes with different OS and/or browser configuration. The test code is running on a different container, which only connects to selenium hub even for different browser tests.

The benefits of Grid mode are:

* Gives the flexibility to distribute your test cases for execution
* Reduces batch processing time
* Can perform multi browser testing
* Can perform multi OS testing

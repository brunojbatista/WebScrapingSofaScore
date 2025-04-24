import time;
import re;

from selenium.webdriver.common.by import By

from selenium.common.exceptions import (
    StaleElementReferenceException,
)

class ec_disappear_element(object):

    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, driver):
        try:
            el = driver.find_element(By.XPATH, self.xpath);
            del el
            return False;
        except Exception:
            return True;
        

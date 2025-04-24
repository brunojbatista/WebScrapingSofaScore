import time;
import re;

from selenium.webdriver.common.by import By

class ec_has_attribute(object):

    def __init__(self, xpath, attribute):
        self.xpath = xpath
        self.attribute = attribute

    def __call__(self, driver):
        print(f"******************** ec_has_attribute")
        element = driver.find_element(By.XPATH, self.xpath)
        # element = get_element(driver, self.xpath, 'presence')
        value = element.get_attribute(self.attribute);
        print(f"element: {element}")
        print(f"attr: {value}")
        return value != None and value != False;

import time;
import re;

from selenium.webdriver.common.by import By

class ec_has_element(object):

    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, driver):
        # print(f"******************** ec_has_element")
        element = driver.find_element(By.XPATH, self.xpath);
        # print(f"element: {element}")
        status = element != None;
        if element: del element
        return status
        

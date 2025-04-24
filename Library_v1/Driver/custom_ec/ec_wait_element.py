import time;
import re;

from selenium.webdriver.common.by import By

class ec_wait_element(object):

    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, driver):
        print(f"******************** ec_wait_element")
        print(f"driver: {driver}")
        element = driver.find_element(By.XPATH, self.xpath);
        print(f"element: {element}")
        # return element != None;
        return False;
        

import time;
import re;

from selenium.webdriver.common.by import By

class ec_changes_element(object):

    def __init__(self, xpath, oldId):
        # print(f"ref element: {element}")
        self.xpath = xpath
        self.oldId = oldId
        # self.text = element.text

    def __call__(self, driver):
        # print(f"******************** ec_changes_element")
        element = driver.find_element(By.XPATH, self.xpath);
        current_id = element.id;
        # current_text = element.text;
        # print(f"element: {element} / self.text: {self.text} / current_text: {current_text}")
        # print(f"element: {element} / self.oldId: {self.oldId} / current_id: {current_id}")
        if current_id != self.oldId:
            return element;
        else:
            del element
            return False;

import time;
import re;

from selenium.webdriver.common.by import By

class ec_changes_attribute_element(object):

    def __init__(self, xpath, attr_name, old_attr):
        # print(f"ref element: {element}")
        self.xpath = xpath
        self.attr_name = attr_name
        self.old_attr = old_attr
        # self.attr_value = element.get_attribute(self.attr)
        # self.text = element.text

    def __call__(self, driver):
        # print(f"******************** ec_changes_attribute_element")
        element = driver.find_element(By.XPATH, self.xpath)
        current_attr_value = element.get_attribute(self.attr_name)
        # print(f"element: {element} / self.old_attr: {self.old_attr} / current_attr_value: {current_attr_value}")
        if current_attr_value != self.old_attr:
            return element;
        else:
            del element
            return False;

        # current_text = element.text;
        # print(f"element: {element} / self.text: {self.text} / current_text: {current_text}")
        # print(f"element: {element} / self.ref_id: {self.ref_id} / current_id: {current_id}")
        # if current_id != self.ref_id:
        #     return element;
        # else:
        #     return False;

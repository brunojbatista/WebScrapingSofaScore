import time;
import re;

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ec_remove_text_by_backspace(object):

    def __init__(self, xpath: str):
        self.xpath = xpath

    def __call__(self, driver):
        print("********************** ec_remove_text_by_backspace:")
        el = driver.find_element(By.XPATH, self.xpath)
        el.send_keys(Keys.BACKSPACE)
        text = el.get_attribute("value");
        print(f"text: ({text})")
        return re.search(r"^\s*$", str(text)) != None;

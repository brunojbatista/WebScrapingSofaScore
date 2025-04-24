from selenium.webdriver import (
    Chrome,
    Firefox,
)
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as OptionChrome
from selenium.webdriver.firefox.options import Options as OptionFirefox

# from pathlib import Path
# import re
# import os

# CURRENT_BINARY_FIREFOX = "C:\Program Files\Mozilla Firefox\firefox.exe"

# p = Path(__file__);
# dir = str(Path(__file__).absolute());
# CURRENT_DIR = re.sub(r"\\[^\\]+\.py", '', dir)

# def concat_dir(filepath):
#     path = re.split(r"[\\\/]", filepath)
#     return os.sep.join(path)

# def get_webdriver_path(relativepath):
#     path = [
#         CURRENT_DIR,
#     ] + re.split(r"[\\\/]", relativepath)
#     print(path)
#     return os.sep.join(path)

"""
    - Firefox:
        https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/firefox_exports_Options.html


"""

class WebDriver():

    def __init__(self, type_driver: str, options = None) -> None:
        self.driver = None;
        self.init(type_driver, options)

    def init(self, type_driver: str, options):
        if type_driver == 'chrome':
            self.driver = Chrome(
                executable_path=ChromeDriverManager().install(), 
                options=options
            )
        elif type_driver == 'firefox' or type_driver == 'gecko':
            # firefox_filepath = get_webdriver_path('executable_webdrivers/geckodriver.exe')
            self.driver = Firefox(
                executable_path=GeckoDriverManager().install(),
                options=options,
            )
        else:
            raise ValueError(f"Não foi possível idenificar o webdriver '{type_driver}'");



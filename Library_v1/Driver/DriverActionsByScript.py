# from DriverInterface import DriverInterface
from Library_v1.Driver.DriverInterface import DriverInterface
# from Library_v1.Driver.DriverInterface import DriverInterface

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder


from Library_v1.Driver.custom_ec.ec_changes_text import ec_changes_text
from Library_v1.Driver.custom_ec.ec_changes_url import ec_changes_url
from Library_v1.Driver.custom_ec.ec_has_attribute import ec_has_attribute
from Library_v1.Driver.custom_ec.ec_no_attribute import ec_no_attribute
from Library_v1.Driver.custom_ec.ec_changes_element import ec_changes_element
from Library_v1.Driver.custom_ec.ec_changes_attribute_element import ec_changes_attribute_element
from Library_v1.Driver.custom_ec.ec_has_element import ec_has_element
from Library_v1.Driver.custom_ec.ec_has_no_element import ec_has_no_element
from Library_v1.Driver.custom_ec.ec_disappear_element import ec_disappear_element
from Library_v1.Driver.custom_ec.ec_match_text_i import ec_match_text_i
from Library_v1.Driver.custom_ec.ec_remove_text_by_backspace import ec_remove_text_by_backspace

from selenium.webdriver.support.expected_conditions import (
    visibility_of_element_located,
    presence_of_element_located,
    invisibility_of_element_located,
    presence_of_all_elements_located,
    visibility_of_all_elements_located,
) 

from selenium.common.exceptions import (
    ElementNotVisibleException, 
    ElementNotSelectableException,
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    JavascriptException
)

from Library_v1.Utils.file import (
    download,
    delete_folder,
)

from Library_v1.Utils.string import (
    clear_accents,
)

import re;
from time import sleep;

import gc

from time import sleep
from selenium.common.exceptions import NoSuchElementException

from typing import (
    List,
)

# import requests;
# FILE_SAVER_MIN_JS_URL = "https://raw.githubusercontent.com/eligrey/FileSaver.js/master/dist/FileSaver.min.js"

# import os
# import sys
# import re;
# import urllib.request;

# def get_script_path():
#     return os.path.dirname(os.path.realpath(sys.argv[0]))

# def get_custom_path(relative_path: str):
#     folders = re.split(r"[\/\\]", re.sub(r"(^\s*\\+|^\s*\/+)", '', relative_path))
#     return re.sub(r"(\\+\s*$|\/+\s*$)", '', os.path.join(get_script_path(), *folders))]

from Library_v1.Directory.Directory import Directory

from Library_v1.Driver.DriverActions import DriverActions

import traceback

class DriverActionsByScript(DriverActions):

    def __init__(self, driver = None):
        super().__init__(driver)
    
    # ==========================================================================================
    # Funções que usam Expected Condition

    def get_element(self, xpath: str, type: str = 'presence', time: int = 60) -> WebElement:
        self.open_driver();
        ref = self.get_ref()
        script = """
        const xpath = arguments[0];
        const referenceElement = arguments[1] || document;  // Se não houver referência, usa o documento
        const timeout = arguments[2];
        function getElement(xpath, ref = document, timeout = 60000) {
            return new Promise((resolve, reject) => {
                const startTime = Date.now();

                const interval = setInterval(
                    () => {
                        const element = document.evaluate(xpath, ref, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

                        if (element) {
                            clearInterval(interval);
                            resolve(element);
                        }

                        if (Date.now() - startTime > timeout) {
                            clearInterval(interval); // Tempo limite alcançado, parar a verificação
                            reject(new Error("Elemento não encontrado dentro do tempo limite"));
                        }
                    }, 
                    100
                ); // Verifica a cada 100ms
            });
        }
        return getElement(xpath, referenceElement, timeout);
        """
        text = self.driver.execute_script(script, xpath, ref, time*1000)
        return text
    
    def get_elements(self, xpath: str, type: str = 'presence', time: int = 60) -> List[WebElement]:
        self.open_driver();
        ref = self.get_ref()
        script = """
        const xpath = arguments[0];
        const referenceElement = arguments[1] || document;  // Se não houver referência, usa o documento
        const result = document.evaluate(
            xpath, 
            referenceElement, 
            null, 
            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, 
            null
        );
        
        const data = [];
        for (let i = 0; i < result.snapshotLength; i++) {
            const element = result.snapshotItem(i);
            data.push(element);
        }
        return data;
        """
        return self.driver.execute_script(script, xpath, ref)
    
    def has_element(self, xpath_or_webelement: str|WebElement, time: int = 60) -> bool:
        self.open_driver();
        if isinstance(xpath_or_webelement, WebElement):
            script = """
            const element = arguments[0];
            return !!element;
            """
            return self.driver.execute_script(script, xpath_or_webelement)
        else:
            ref = self.get_ref()
            if time <= 0: time = 0.5
            script = """
            const xpath = arguments[0];
            const referenceElement = arguments[1] || document;  // Se não houver referência, usa o documento
            const timeout = arguments[2];
            function hasElement(xpath, ref = document, timeout = 60000) {
                return new Promise((resolve, reject) => {
                    const startTime = Date.now();

                    const interval = setInterval(() => {
                        const element = document.evaluate(xpath, ref, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

                        if (element) {
                            clearInterval(interval);
                            resolve(true);
                        }

                        if (Date.now() - startTime > timeout) {
                            clearInterval(interval); // Tempo limite alcançado, parar a verificação
                            reject(new Error("Elemento não encontrado dentro do tempo limite"));
                        }
                    }, 100); // Verifica a cada 100ms
                });
            }

            return hasElement(xpath, referenceElement, timeout);
            """
            try:
                self.driver.execute_script(script, xpath_or_webelement, ref, time*1000)
                return True
            except JavascriptException:
                return False

    def get_text(self, xpath_or_webelement: str|WebElement, time: int = 60) -> str:
        self.open_driver();
        if isinstance(xpath_or_webelement, WebElement):
            script = """
            const element = arguments[0];
            return element ? element.textContent : null;
            """
            text = self.driver.execute_script(script, xpath_or_webelement)
            return text
        else:
            ref = self.get_ref()
            script = """
            const xpath = arguments[0];
            const referenceElement = arguments[1] || document;  // Se não houver referência, usa o documento
            const timeout = arguments[2];
            function getText(xpath, ref = document, timeout = 60000) {
                return new Promise((resolve, reject) => {
                    const startTime = Date.now();

                    const interval = setInterval(
                        () => {
                            const element = document.evaluate(xpath, ref, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

                            if (element) {
                                let text = element ? element.textContent : null;
                                if (text !== null) {
                                    clearInterval(interval);
                                    resolve(text);
                                }
                            }

                            if (Date.now() - startTime > timeout) {
                                clearInterval(interval); // Tempo limite alcançado, parar a verificação
                                reject(new Error("Elemento não encontrado dentro do tempo limite"));
                            }
                        }, 
                        100
                    ); // Verifica a cada 100ms
                });
            }
            return getText(xpath, referenceElement, timeout);
            """
            text = self.driver.execute_script(script, xpath_or_webelement, ref, time*1000)
            return text
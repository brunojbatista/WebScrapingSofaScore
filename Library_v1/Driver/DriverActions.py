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

class DriverActions():

    def __init__(self, driver: DriverInterface = None) -> None:
        self.driver : DriverInterface = None;
        self.set_driver(driver);
        self.ref : str|WebElement = None;
    
    def get_driver(self, ) -> DriverInterface:
        return self.driver
    
    def get_download_path(self, ) -> str:
        return self.driver.get_download_path()

    def get_download_relativepath(self, ) -> str:
        return self.driver.get_download_relativepath()

    def sleep(self, time: float, offset_max: float = 0):
        timing = self.generate_random(time, offset_max)
        # print(f"sleep: {timing} seconds")
        sleep(timing)

    def generate_random(self, value: float, offset_max: float = 0):
        from random import seed
        from random import random
        import time as t1
        seed(t1.time())
        new_value = value + offset_max*random()
        return new_value;

    def set_ref(self, ref : str|WebElement):
        # self.ref = ref;
        if isinstance(ref, str): ref = self.get_element(ref)
        self.ref = ref;
        return self;

    def clear_ref(self, ):
        return self.set_ref(None);
    
    def get_ref(self, ):
        ref = self.ref
        self.clear_ref();
        return ref;

    def set_driver(self, driver: DriverInterface):
        self.driver = None;
        if driver != None: self.driver = driver;
        return self;

    def open_driver(self, reopen: bool = False):
        if not(self.driver): raise ValueError("O driver não foi iniciado")
        if reopen: self.driver.open();
        elif not self.driver.is_open(): self.driver.open();
        return self;

    def lock(self, timeout : int = 30):
        self.driver.lock(timeout);

    def unlock(self, ):
        self.driver.unlock();

    def navigate_url(self, url: str):
        self.open_driver();
        self.driver.get_url(url)
        return self;

    def check_url(self, regex_match: str) -> bool:
        self.open_driver();
        return re.search(regex_match, self.get_url(), flags=re.I) != None;

    def in_url(self, search_url: str) -> bool:
        self.open_driver();
        cleared_search_url = re.sub(r'(\/\s*$)', '', search_url, flags=re.I)
        status = cleared_search_url in self.get_url();
        # print(f"in_url - cleared_search_url: {cleared_search_url} / url: {self.get_url()} / status: {status}")
        return status;

    def get_url(self, ):
        self.open_driver();
        return re.sub(r'(\/\s*$)', '', self.driver.get_current_url(), flags=re.I);

    def check_title(self, regex_match: str) -> bool:
        self.open_driver();
        return re.search(regex_match, clear_accents(self.driver.get_title()), flags=re.I) != None;

    def get_current_tab(self, ) -> str:
        self.open_driver();
        return self.driver.get_current_window()

    def get_tabs(self, ) -> list:
        self.open_driver();
        return self.driver.get_windows();

    def switch_tab(self, handle: str = None):
        if handle is None: return;
        self.open_driver();
        current_tab = self.get_current_tab()
        # if current_tab == handle: return;
        return self.driver.switch_window(handle)

    def new_tab(self, ):
        self.open_driver();
        return self.driver.new_window();

    def refresh(self, ):
        self.open_driver();
        return self.driver.refresh();

    def set_maximize(self, ):
        self.driver.set_maximize();
    
    def save_screenshot(self, name: str) -> str:
        return self.driver.save_screenshot(name)
    
    # ==========================================================================================
    # Funções que usam Expected Condition

    def get_element(self, xpath: str, type: str = 'presence', time: int = 60) -> WebElement:
        self.open_driver();
        if time <= 0: time = 0.5;
        ec_function = None;
        locator = (By.XPATH, xpath)
        if type == 'presence' or type == 'pre':
            ec_function = presence_of_element_located(locator)
        elif type == 'visibility' or type == 'vis':
            ec_function = visibility_of_element_located(locator)
        elif type == 'invisibility' or type == 'invis':
            ec_function = invisibility_of_element_located(locator)
        else:
            raise ValueError("A busca do tipo do elemento não é conhecida");
        try:
            return self.driver.set_wait(time, ref=self.get_ref()).set_condition(ec_function);
        except TimeoutException:
            raise ValueError(f"Elemento não encontrado")

    def get_elements(self, xpath: str, type: str = 'presence', time: int = 60) -> List[WebElement]:
        self.open_driver();
        if time <= 0: time = 0.5;
        ec_function = None;
        locator = (By.XPATH, xpath)
        if type == 'presence' or type == 'pre':
            ec_function = presence_of_all_elements_located(locator)
        elif type == 'visibility' or type == 'vis':
            ec_function = visibility_of_all_elements_located(locator)
        else:
            raise ValueError("A busca do tipo dos elementos não é conhecida");
        try:
            return self.driver.set_wait(time, ref=self.get_ref()).set_condition(ec_function);
        except TimeoutException:
            raise ValueError(f"Elementos não encontrados")

    def has_element(self, xpath: str, time: int = 60) -> bool:
        self.open_driver();
        if time <= 0: time = 0.5;
        try:
            return self.driver.set_wait(time, ref=self.get_ref()).set_condition(ec_has_element(xpath));
        except TimeoutException:
            return False;

    def disappear_element(self, xpath: str, time: int = 60) -> bool:
        self.open_driver();
        if time <= 0: time = 0.5;
        try:
            return self.driver.set_wait(time, ref=self.get_ref()).set_condition(ec_disappear_element(xpath));
        except TimeoutException:
            return False;

    def changes_element(self, xpath: str, callback: callable, time: int = 60) -> bool:
        self.open_driver();
        if time <= 0: time = 0.5;
        self.clear_ref()
        element = self.get_element(xpath, time=time)
        oldId = element.id
        del element
        callback()
        try:
            el = self.driver.set_wait(time).set_condition(ec_changes_element(xpath, oldId));
            del el
            return True
        except TimeoutException:
            return False;

    def changes_attribute_element(self, xpath: str, callback: callable, attr: str, time: int = 60) -> bool:
        self.open_driver();
        if time <= 0: time = 0.5;
        self.clear_ref()
        element = self.get_element(xpath, time=time)
        old_attr = element.get_attribute(attr)
        del element
        callback()
        try:
            el = self.driver.set_wait(time).set_condition(ec_changes_attribute_element(xpath, attr, old_attr));
            del el
            return True;
        except TimeoutException:
            return False;

    def has_no_element(self, xpath: str, time: int = 60) -> bool:
        return self.disappear_element(xpath, time)
    
    def match_text_i(self, xpath: str, regex: str, time: int = 60):
        self.open_driver();
        if time <= 0: time = 0.5;
        try:
            return self.driver.set_wait(time, ref=self.get_ref()).set_condition(ec_match_text_i(xpath, regex));
        except TimeoutException:
            raise ValueError(f"O conteudo do elemento não foi encontrado")

    def promise(self, success_xpath: str, fail_xpath: str, time: int = 30) -> bool:
        status = False;
        step_time = 0.5;
        total_time = time
        ref = self.get_ref();
        while total_time > 0:
            if self.set_ref(ref).has_element(success_xpath, time=step_time):
                status = True;
                break;
            else:
                if self.set_ref(ref).has_element(fail_xpath, time=step_time):
                    status = False;
                    break;
                else:
                    total_time -= (2*step_time)
        if total_time <= 0: raise TimeoutError("Não foi possível resolver a promessa")
        return status;

    # ==========================================================================================
    # Funções que  usam funções de elementos

    def parse_element(self, xpath_or_webelement: str|WebElement, time: int = 60) -> WebElement:
        gc.collect()
        self.open_driver();
        el = xpath_or_webelement
        if isinstance(el, str): el = self.get_element(xpath_or_webelement, 'presence', time);
        return el;

    def clear_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        el.clear()
        del el
        return True

    def write_element(self, xpath_or_webelement: str|WebElement, text: str, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        el.send_keys(text)
        del el
        return True

    def setZoom(self, zoomPercentage: float):
        self.navigate_url('chrome://settings/')
        self.driver.execute_script(f"chrome.settingsPrivate.setDefaultZoom({round(zoomPercentage/100, 2)});")
    
    def scroll_up_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        el.send_keys(Keys.PAGE_UP)
        del el
        return True
    
    def scroll_down_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        el.send_keys(Keys.DOWN)
        del el
        return True
    
    def scroll_home_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        el.send_keys(Keys.HOME)
        del el
        return True

    def scroll_end_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        el.send_keys(Keys.END)
        del el
        return True
    
    def get_children_dimesions_relative_parent(self, parent_xpath_or_webelement: str|WebElement, children_xpath_or_webelement: str|WebElement, time: int = 0):
        # Localizar os elementos pai e filho
        parent_element = self.parse_element(parent_xpath_or_webelement, time)
        child_element = self.parse_element(children_xpath_or_webelement, time)

        # Executar JavaScript para calcular a altura relativa
        script = """
        const parent = arguments[0];
        const child = arguments[1];
        const parentRect = parent.getBoundingClientRect();
        const childRect = child.getBoundingClientRect();
        return {
            relativeHeight: childRect.height,
            relativeTop: childRect.top - parentRect.top,
            relativeBottom: childRect.bottom - parentRect.top
        };
        """
        
        result = self.driver.execute_script(script, parent_element, child_element)
        return result

    def click_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        last_ref = self.get_ref();
        try:
            el = self.set_ref(last_ref).parse_element(xpath_or_webelement, time)
            el.click();
            del el
        except ElementClickInterceptedException:
            self.set_ref(last_ref).click_element_by_js(xpath_or_webelement, time)
        return True;

    def click_element_by_js(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        self.driver.execute_script("arguments[0].click();", el);
        del el
        return True

    def remove_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        self.driver.execute_script("arguments[0].remove();", el);
        del el
        return True

    def press_tab(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        el.send_keys(Keys.TAB)
        del el
        return True;

    def press_enter(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        el.send_keys(Keys.ENTER)
        del el
        return True;

    def press_backspace(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        el.send_keys(Keys.BACKSPACE)
        del el
        return True;

    def has_stateless(self, xpath: str):
        try:
            el = self.parse_element(xpath)
            del el
            return False;
        except StaleElementReferenceException:
            return True;

    def is_element_stale(self, xpath_or_webelement: str|WebElement):
        try:
            # Tentar uma interação simples
            el = self.parse_element(xpath_or_webelement)
            el.is_enabled()
            return False  # Elemento está válido
        except StaleElementReferenceException:
            return True  # Elemento está stale
        
    def catch_stale_element_exception(self, fn: callable, response_fail: any):
        try:
            return fn()
        except StaleElementReferenceException:
            return response_fail  # Elemento está stale

    def clear_field_backspace(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        total_caracters = len(el.get_attribute("value"))
        while total_caracters > 0:
            self.press_backspace(el);
            value = el.get_attribute("value")
            if re.search(r"^\s*$", str(value)) != None:
                del el
                return True;
            total_caracters -= 1;
            if total_caracters <= 0: 
                del el
                raise ValueError("Não foi possível limpar o texto")
        del el

    def scroll_down(self, ):
        import time;
        self.open_driver();
        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height >= last_height:
                break
            last_height = new_height
        return True;
        
    def download(self, url: str, filename: str, relative_path: str = ''):
        # print("------------------------------------------------------------------")
        # print(">> Download:")
        # print(f"url: {url} / filename: {filename} / relative_path: {relative_path}")
        return download(url, filename, relative_path)
        
    def drag_element(self, xpath_or_webelement: str|WebElement, pos_x: int, pos_y: int, time: int = 60):
        self.open_driver();
        el = self.parse_element(xpath_or_webelement, time)
        action = ActionChains(self.driver.get())
        action = action.move_to_element_with_offset(el, pos_x, pos_y).click()
        action.perform()
        del el
        del action
        return True
    
    def move_to_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        self.open_driver();
        el = self.parse_element(xpath_or_webelement, time)
        action = ActionChains(self.driver.get())
        action = action.move_to_element(el)
        action.perform()
        del el
        del action
        return True
    
    def get_coordenate(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        
        # Executa o JavaScript para obter as coordenadas exatas
        coordenates = self.driver.execute_script("""
            let elemento = arguments[0];
            let box = elemento.getBoundingClientRect();
            return {x: box.x, y: box.y, width: box.width, height: box.height};
        """, el)

        return coordenates
    
    def get_text(self, xpath_or_webelement: str|WebElement, time: int = 60) -> str:
        el = self.parse_element(xpath_or_webelement, time)
        text = el.text;
        del el
        return text
    
    def mouse_move_event_horizontal(self, xpath_or_webelement: str|WebElement, steps: int = 3, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)

        script_move_continuo = """
            let elem = arguments[0];
            let steps = arguments[1];
            let rect = elem.getBoundingClientRect();

            for (let i = 0; i < steps; i++) {
                let evt = new MouseEvent('mousemove', {
                    bubbles: true,
                    cancelable: true,
                    clientX: rect.left + (rect.width / 2) + i,  // Ajuste horizontalmente
                    clientY: rect.top + (rect.height / 2)       // Mantém na altura central
                });
                elem.dispatchEvent(evt);
            }
        """
        self.driver.execute_script(script_move_continuo, el, steps)

    # Define o script de movimentação com checagem do tooltip
    def hover_until_tooltip_appears(self, xpath_or_webelement: str|WebElement, tooltip_xpath, steps=10, pause=0.1, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time=time)
        for i in range(steps):
            # Movimenta o mouse no elemento
            script = f"""
                let elem = arguments[0];
                let rect = elem.getBoundingClientRect();
                let evt = new MouseEvent('mousemove', {{
                    bubbles: true,
                    cancelable: true,
                    clientX: rect.left + (rect.width / 2) + {i},  // Ajuste horizontalmente
                    clientY: rect.top + (rect.height / 2)         // Mantém na altura central
                }});
                elem.dispatchEvent(evt);
            """
            self.driver.execute_script(script, el)
            # Verifica se o tooltip está visível no DOM
            try:
                tooltip = self.get_element(tooltip_xpath, time=time)
                if tooltip.is_displayed():
                    print("Tooltip apareceu!")
                    return True
            except ValueError:
                # Se o tooltip não foi encontrado, continue o loop
                pass
            # Pausa entre os movimentos para simular movimento contínuo
            sleep(pause)
        return False
    
    def extract_all_properties(self, xpath_or_webelement: str|WebElement, properties_name: list, time: int = 60) -> dict:
        el = self.parse_element(xpath_or_webelement, time=time)
        properties = {}
        for prop in properties_name:
            properties[prop] = self.get_attr(el, prop, time=time)
        return properties

    def get_attr(self, xpath_or_webelement: str|WebElement, attr_name: str, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        attr = el.get_attribute(attr_name);
        del el
        return attr

    def has_class(self, xpath_or_webelement: str|WebElement, name: str, time: int = 60) -> bool:
        return name in self.get_attr(xpath_or_webelement, 'class', time)
    
    # ==========================================================================================
    def force_click_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        waitingTime = 0.5
        attempts = time/waitingTime
        has_finished = False
        while True:
            if attempts <= 0: break;
            try:
                self.sleep(waitingTime)
                self.click_element(xpath_or_webelement, time)
                has_finished = True;
                break;
            except ElementNotInteractableException:
                attempts -= 1;
                
        if not has_finished: raise ValueError("A tentativa de forçar o clique não funcionou")

    def force_write_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        waitingTime = 1
        attempts = time/waitingTime
        has_finished = False
        while True:
            if attempts <= 0: break;
            try:
                self.sleep(waitingTime)
                self.write_element(xpath_or_webelement, time)
                has_finished = True;
                break;
            except ElementNotInteractableException:
                attempts -= 1;
                
        if not has_finished: raise ValueError("A tentativa de escrever não funcionou")

    def scroll_to_element(self, xpath_or_webelement: str|WebElement,  time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
        del el
        return True
    
    # ==========================================================================================
    # Comportamentos como humano
    def digit_like_human(self, text: str):
        letters = re.split('', text)
        letters = [x for x in re.split('', text) if x != '']
        if len(letters) <= 0: return;
        action = ActionChains(self.driver.get())
        for letter in letters:
            action = action.pause(self.generate_random(0.05, 0.05)).send_keys(letter)
        action.perform();
        del action
        return True

    # def clear_like_human(self, ):

    # Movendo um elemento para dentro do outro
    def drag_and_drop_element(self, drag_el: WebElement, drop_el: WebElement):
        action = ActionChains(self.driver.get())
        action = action.drag_and_drop(drag_el, drop_el)
        action.perform()
        del action
        return self;

    # def scroll_to_element(self, target_el: WebElement):
    #     action = ActionChains(self.driver.get())
    #     action = action.scroll_to_element(target_el)
    #     action.perform()
    #     del action
    #     return True

    def avoid_state_element_reference_exception(self, fn: callable, attempts: int = 60):
        while attempts > 0:
            try:
                return fn()
            except StaleElementReferenceException:
                self.sleep(1)
                attempts -= 1
        if attempts <= 0: raise ValueError("As tentativas para a exceção da referência do elemento obsoleto foi excedida")
    
    def is_page_complete(self, timeout=10, intervalo=0.1):
        import time

        """
        Verifica em loop se a página carregou completamente.
        
        Args:
            driver: Instância do WebDriver.
            timeout: Tempo máximo total de espera (em segundos).
            intervalo: Intervalo entre as verificações (em segundos).
        
        Raises:
            TimeoutError: Se a página não carregar dentro do tempo.
        """
        tempo_inicial = time.time()
        
        while True:
            estado = self.driver.execute_script("return document.readyState")
            if estado == "complete":
                print("Página carregada!")
                break
            
            if time.time() - tempo_inicial > timeout:
                raise TimeoutError("A página não carregou dentro do tempo especificado.")
            
            time.sleep(intervalo)

    def custom_script(self, code: str, *args):
        return self.driver.execute_script(code, *args)
    
    def custom_async_script(self, code: str, *args):
        return self.driver.execute_async_script(code, *args)
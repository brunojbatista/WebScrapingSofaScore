# from DriverInterface import DriverInterface
from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.Driver.DriverLock import DriverLock

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import undetected_chromedriver as uc

# from selenium_stealth import stealth

import os
import sys
import re

from Library_v1.Utils.file import (
    get_script_path,
    edit_chromedriver,
)

from Library_v1.Directory.Directory import Directory

# def get_script_path():
#     return os.path.dirname(os.path.realpath(sys.argv[0]))


class ChromeDriver(DriverInterface):
    driver = None

    def __init__(self, download_path: str = "Downloads/") -> None:
        super().__init__()
        self.driver = None;
        self.wait = None;
        self.options_browser = {}
        self.options = None
        self.download_path = None
        self.download_relativepath = None
        self.driver_lock = DriverLock()
        self.set_download_path(download_path)
        self.initialize_options()
    
    def initialize_options(self, ):
        self.options_browser = {
            "download.default_directory": self.download_path,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "useAutomationExtension": False,
            "excludeSwitches": ["enable-automation"],
        }

    def set_download_path(self, download_path: str):
        download = Directory(download_path)
        download.create()
        self.download_path = download.get_path()
        self.download_relativepath = download.get_relativepath()
    
    def get_download_path(self, ) -> str:
        return self.download_path
    
    def get_download_relativepath(self, ) -> str:
        return self.download_relativepath
    
    def find_download_file(self, searched_name, path = None):
        download = Directory(self.download_path)
        return download.find_file(searched_name, path)

    def lock(self, timeout : int = 30):
        self.driver_lock.lock(timeout);

    def unlock(self, ):
        self.driver_lock.unlock();

    def open(self):
        self.close()

        # -------------------------------------------------
        # Buscando do webdriver do chrome
        # d = Directory("Library_v1/Driver/browsers/chrome/current")
        # filepath = d.find_file(f"\.exe$")
        filepath = None

        # -------------------------------------------------
        # Setando as opções mais leves para o Chrome
        self.options = Options() if filepath else uc.ChromeOptions()

        # Adicionando configurações leves para performance
        self.options.add_argument("--disable-extensions")  # Desativa extensões
        self.options.add_argument("--no-sandbox")  # Desativa sandbox, melhora a performance
        self.options.add_argument("--disable-gpu")  # Desativa GPU (ajuda na execução sem interface gráfica)
        self.options.add_argument("--disable-software-rasterizer")  # Não usa renderização de software
        self.options.add_argument("--disable-dev-shm-usage")  # Usar /tmp ao invés de /dev/shm para melhorar a performance em containers
        
        # Use headless mode se não precisar visualizar o navegador
        # self.options.add_argument("--headless")  # Executa o Chrome sem interface gráfica
        self.options.add_argument("--window-size=1920x1080")  # Define um tamanho padrão para a janela (necessário no modo headless)

        # Desativa serviços de segurança e proteção
        self.options.add_argument('--disable-web-security')  # Desativa a segurança web
        self.options.add_argument("--safebrowsing-disable-download-protection")  # Desativa proteção de download
        self.options.add_argument("--safebrowsing-disable-extension-blacklist")  # Desativa blacklist de extensões

        # Configurações de carregamento de página para acelerar
        self.options.page_load_strategy = 'eager'  # Carrega a página sem esperar todos os recursos (mais rápido)

        # Configurações de download
        self.options_browser = {
            "download.default_directory": self.download_path,
            "safebrowsing.enabled": False,
            "profile.default_content_setting_values.automatic_downloads": 1
        }
        self.options.add_experimental_option("prefs", self.options_browser)

        # -------------------------------------------------
        # Abrindo a instância do webdriver
        if filepath:
            ChromeDriver.driver = Chrome(
                service=ChromeService(executable_path=filepath),
                options=self.options
            )
        else:
            ChromeDriver.driver = uc.Chrome(options=self.options)

        # -------------------------------------------------
        # Maximizando a janela se não for headless
        if "--headless" not in self.options.arguments:
            ChromeDriver.driver.maximize_window()


    def get(self, ):
        # return self.driver;
        # if not ChromeDriver.driver is None:
        #     ChromeDriver.driver.execute_script("window.gc();")  # Força o garbage collector do JavaScript (em ambientes onde é suportado)
        return ChromeDriver.driver

    def is_open(self, ) -> bool:
        return self.get() != None;

    def set_wait(self, timeout = 1, ref = None):
        if ref == None: ref = self.get()
        self.wait = WebDriverWait(
            ref, 
            timeout=timeout
        )
        return self;

    def set_condition(self, ec_function):
        if not(self.wait): raise ValueError("A espera não foi definida")
        return self.wait.until(ec_function)

    def get_url(self, url: str):
        self.get().get(url)

    def get_session_id(self):
        return self.get().session_id

    def get_title(self):
        return self.get().title
    
    def refresh(self):
        return self.get().refresh();

    def close(self):
        if self.get(): self.get().close();

    def execute_script(self, script: str, *args):
        return self.get().execute_script(script, *args)

    def get_current_url(self, ):
        return self.get().current_url

    def get_windows(self, ) -> list:
        return self.get().window_handles;

    def get_current_window(self, ) -> str:
        return self.get().current_window_handle

    def switch_window(self, handle: str):
        return self.get().switch_to.window(handle)

    def new_window(self, ) -> str:
        self.get().switch_to.new_window();
        return self.get_current_window();

    def close_tab(self, ):
        return self.get().close();

    def clear_browser_data(self, ):
        self.get().get('chrome://settings/clearBrowserData')

    def save_screenshot(self, name: str) -> str:
        name_formated = re.sub(r"\.[^\.]*$", '', name)
        name_formated = f"{name_formated}.jpg"
        self.get().save_screenshot(name_formated)
        return name_formated;
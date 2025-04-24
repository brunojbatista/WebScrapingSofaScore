from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.Driver.DriverLock import DriverLock

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import os
import sys
import re

from Library_v1.Utils.file import (
    get_script_path,
)

from Library_v1.Directory.Directory import Directory

import json
import psutil


class ChromeDriver(DriverInterface):
    driver = None

    def __init__(self, download_path: str = "Downloads/") -> None:
        super().__init__()
        self.wait = None
        self.options = None
        self.download_path = None
        self.download_relativepath = None
        self.last_state = {}
        self.max_memory_mb: int = 2000
        self.driver_lock = DriverLock()
        self.set_download_path(download_path)
        self.initialize_options()
    
    def save_state(self, ):
        """Salva o estado atual do navegador."""
        if self.get():
            self.last_state['url'] = self.get().current_url
            self.last_state['cookies'] = self.get().get_cookies()
            self.last_state['local_storage'] = self.get().execute_script("return {...localStorage};")
            self.last_state['session_storage'] = self.get().execute_script("return {...sessionStorage};")
            print("Estado salvo:", json.dumps(self.last_state, indent=2))
            self.close()

    def restore_state(self, ):
        """Restaura o estado salvo no navegador."""
        if self.last_state:
            self.open()
            self.get().get(self.last_state['url'])
            for cookie in self.last_state.get('cookies', []): self.get().add_cookie(cookie)
            self.get().get(self.last_state['url'])
            # self.get().refresh()
            self.get().execute_script("""
                Object.entries(arguments[0]).forEach(([key, value]) => localStorage.setItem(key, value));
            """, self.last_state.get('local_storage', {}))
            self.get().execute_script("""
                Object.entries(arguments[0]).forEach(([key, value]) => sessionStorage.setItem(key, value));
            """, self.last_state.get('session_storage', {}))

    def check_memory_and_restart(self):
        """Reinicia o driver se o uso de memória ultrapassar o limite definido."""
        # self.save_state()
        # self.restore_state()
        # return True
        if not self.get() is None:
            pid = self.get().service.process.pid
            process = psutil.Process(pid)  # Processo principal
            memory_usage_mb = process.memory_info().rss / (1024 ** 2)  # Memória do processo principal
            for child in process.children(recursive=True):  # Subprocessos
                memory_usage_mb += (child.memory_info().rss / (1024 ** 2))
            print(f"Total de memoria: {memory_usage_mb}")
            if memory_usage_mb > self.max_memory_mb:
                print(">>>>>>>>>>>>>>>>> Memória excedida. Reiniciando o driver <<<<<<<<<<<<<<<<<")
                self.save_state()
                self.restore_state()
                return True
            else: return False


            # driver_process = psutil.Process(self.get().service.process.pid)
            # memory_usage_mb = driver_process.memory_info().rss / (1024 * 1024)
            # print(f"Uso de memória do ChromeDriver: {memory_usage_mb:.2f} MB")
            # if memory_usage_mb > self.max_memory_mb:
            #     input(">>>>>>>>>>>>>>>>> Memória excedida. Reiniciando o driver <<<<<<<<<<<<<<<<<")
            #     self.save_state()
            #     self.restore_state()
            #     return True
            # else: return False

    def initialize_options(self):
        # Configurações do Chrome
        self.options = ChromeOptions()

        # Configurações para download
        prefs = {
            "download.default_directory": self.download_path,  # Caminho para downloads
            "download.prompt_for_download": False,  # Não perguntar ao fazer download
            "download.directory_upgrade": True,  # Atualizar o diretório
            "plugins.always_open_pdf_externally": True,  # Abrir PDFs externamente
            "profile.default_content_settings.popups": 0,  # Desativa pop-ups
            "profile.managed_default_content_settings.images": 1,  # 1 = Habilitado; 2 = Desabilita imagens
            "javascript.enabled": False,  # Desabilita JavaScript (se aplicável)
        }
        self.options.add_experimental_option("prefs", prefs)
        self.options.add_argument("--start-maximized")

        self.options.add_argument("--auto-open-devtools-for-tabs")  # Abre DevTools automaticamente para cada aba
        # self.options.add_argument("--headless")  # Modo headless (opcional)

    def set_download_path(self, download_path: str):
        download = Directory(download_path)
        download.create()
        self.download_path = download.get_path()
        self.download_relativepath = download.get_relativepath()

    def get_download_path(self) -> str:
        return self.download_path

    def get_download_relativepath(self) -> str:
        return self.download_relativepath

    def find_download_file(self, searched_name, path=None):
        download = Directory(self.download_path)
        return download.find_file(searched_name, path)

    def lock(self, timeout: int = 30):
        self.driver_lock.lock(timeout)

    def unlock(self):
        self.driver_lock.unlock()

    def clear_storage(self, ):
        ChromeDriver.driver.execute_script("window.localStorage.clear();")
        ChromeDriver.driver.execute_script("window.sessionStorage.clear();")
    
    def clear_cookies(self, ):
        ChromeDriver.driver.delete_all_cookies()

    def garbage_collection(self, ):
        ChromeDriver.driver.execute_script("window.gc();")

    def optimize_memory(self, ):
        ChromeDriver.driver.execute_cdp_cmd("Network.clearBrowserCache", {})
        # ChromeDriver.driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
        ChromeDriver.driver.execute_cdp_cmd("HeapProfiler.collectGarbage", {})
        ChromeDriver.driver.execute_cdp_cmd("Network.enable", {})
        ChromeDriver.driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})

    def open(self):
        self.close()

        dir = Directory()
        # filepath = dir.find_file(r'chromedriver\-133\.0\.6943\.53\.exe', 'Library_v1/Driver/executable_webdrivers')
        filepath = dir.find_file(r'chromedriver\-135\.0\.7049\.42\.exe', 'Library_v1/Driver/executable_webdrivers')
        print(f"filepath: {filepath}")

        # Iniciar o WebDriver para Chrome
        ChromeDriver.driver = Chrome(
            # service=ChromeService(ChromeDriverManager().install()),
            service=ChromeService(filepath),
            options=self.options
        )

        ChromeDriver.driver.set_script_timeout(30)

    def get(self):
        return ChromeDriver.driver

    def is_open(self) -> bool:
        return self.get() is not None

    def set_wait(self, timeout=1, ref=None):
        if ref is None:
            ref = self.get()
        self.wait = WebDriverWait(
            ref,
            timeout=timeout
        )
        return self

    def set_condition(self, ec_function):
        if not self.wait:
            raise ValueError("A espera não foi definida")
        return self.wait.until(ec_function)

    def get_url(self, url: str):
        self.get().get(url)

    def get_session_id(self):
        return self.get().session_id

    def get_title(self):
        return self.get().title

    def refresh(self):
        return self.get().refresh()

    def close(self):
        if self.get():
            self.get().close()
            ChromeDriver.driver = None

    def execute_script(self, script: str, *args):
        return self.get().execute_script(script, *args)
    
    def execute_async_script(self, script: str, *args):
        return self.get().execute_async_script(script, *args)

    def get_current_url(self):
        return self.get().current_url

    def get_windows(self) -> list:
        return self.get().window_handles

    def get_current_window(self) -> str:
        return self.get().current_window_handle

    def switch_window(self, handle: str):
        return self.get().switch_to.window(handle)

    def new_window(self) -> str:
        self.get().switch_to.new_window()
        return self.get_current_window()

    def close_tab(self):
        return self.get().close()

    def clear_browser_data(self):
        # Limpa os dados do navegador usando DevTools Protocol
        self.execute_script("window.localStorage.clear();")
        self.execute_script("window.sessionStorage.clear();")
        self.get().delete_all_cookies()

    def save_screenshot(self, name: str) -> str:
        name_formated = re.sub(r"\.[^\.]*$", '', name)
        name_formated = f"{name_formated}.jpg"
        self.get().save_screenshot(name_formated)
        return name_formated

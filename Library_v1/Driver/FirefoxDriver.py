from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.Driver.DriverLock import DriverLock

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

import os
import sys
import re

from Library_v1.Utils.file import (
    get_script_path,
)

from Library_v1.Directory.Directory import Directory


class FirefoxDriver(DriverInterface):
    driver = None

    def __init__(self, download_path: str = "Downloads/") -> None:
        super().__init__()
        self.driver = None
        self.wait = None
        self.options = None
        self.download_path = None
        self.download_relativepath = None
        self.driver_lock = DriverLock()
        self.set_download_path(download_path)
        self.initialize_options()

    def initialize_options(self):
        # Configurações do Firefox
        self.options = FirefoxOptions()
        self.options.set_preference("browser.download.folderList", 2)  # Define a pasta de downloads personalizada
        self.options.set_preference("browser.download.dir", self.download_path)  # Caminho da pasta de download
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/octet-stream")  # Ignora pop-ups de download
        self.options.set_preference("pdfjs.disabled", True)  # Desativa o visualizador de PDFs interno
        self.options.set_preference("dom.webnotifications.enabled", False)  # Desativa notificações
        self.options.add_argument("--width=1920")  # Largura da janela
        self.options.add_argument("--height=1080")  # Altura da janela
        self.options.page_load_strategy = 'eager'  # Configuração padrão de carregamento de página

        # Desabilitar Cache do Navegador
        self.options.set_preference("browser.cache.disk.enable", False)
        self.options.set_preference("browser.cache.memory.enable", False)
        self.options.set_preference("browser.cache.offline.enable", False)
        self.options.set_preference("network.http.use-cache", False)

        # Configuração de Perfis Temporários
        self.options.set_preference("browser.privatebrowsing.autostart", True)  # Navegação privada

        self.options.set_preference("browser.cache.disk.enable", False)  # Desativa cache no disco
        self.options.set_preference("browser.cache.memory.enable", False)  # Desativa cache na memória
        self.options.set_preference("browser.sessionstore.max_tabs_undo", 0)  # Desativa histórico de abas fechadas
        self.options.set_preference("browser.sessionstore.max_windows_undo", 0)  # Desativa histórico de janelas fechadas
        self.options.set_preference("image.mem.decode_bytes_at_a_time", 65536)  # Limita memória usada por imagens
        self.options.set_preference("content.notify.interval", 750000)  # Reduz uso de memória para notificações
        self.options.set_preference("network.http.pipelining", True)  # Habilita pipelining para carregar páginas mais rapidamente

        self.options.set_preference("webgl.disabled", True)  # Desativa WebGL
        self.options.set_preference("layers.acceleration.disabled", True)  # Desativa aceleração de hardware
        self.options.set_preference("gfx.direct2d.disabled", True)  # Desativa Direct2D (somente no Windows)

        self.options.set_preference("browser.cache.disk.enable", False)  # Desativa cache no disco
        self.options.set_preference("browser.cache.memory.capacity", 51200)  # Limita cache em memória a 50 MB
        self.options.set_preference("dom.ipc.processCount", 1)  # Usa um único processo para conteúdo
        self.options.set_preference("network.dns.disablePrefetch", True)  # Desativa prefetch de DNS
        self.options.set_preference("gfx.font_rendering.opentype_svg.enabled", False)  # Desativa renderização de fontes SVG
        self.options.set_preference("network.prefetch-next", False)  # Desativa pré-carregamento de páginas
        self.options.set_preference("network.http.max-persistent-connections-per-server", 2)  # Limita conexões persistentes
        self.options.set_preference("browser.tabs.unloadOnLowMemory", True)  # Descarrega abas inativas em baixa memória
        self.options.set_preference("browser.sessionhistory.max_entries", 2)  # Limita histórico de abas
        self.options.set_preference("browser.sessionstore.resume_from_crash", False)  # Desativa restauração automática de sessões
        self.options.set_preference("media.peerconnection.enabled", False)  # Desativa WebRTC
        self.options.set_preference("media.suspend-bkgnd-video.enabled", True)  # Suspende vídeos em segundo plano
        self.options.set_preference("javascript.options.mem.max", 256)  # Limita uso de memória para scripts
        self.options.set_preference("javascript.options.mem.gc_frequency", 10)  # Aumenta frequência do garbage collector
        self.options.set_preference("dom.event.contextmenu.enabled", False)  # Desativa menu de contexto via DOM
        self.options.set_preference("dom.push.enabled", False)  # Desativa notificações push

        self.options.headless = True  # Troque para True para modo headless

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

    def open(self):
        self.close()
        # Iniciar o WebDriver para Firefox
        FirefoxDriver.driver = Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=self.options
        )

        # FirefoxDriver.driver.execute_script("window.windowUtils.garbageCollect();")

        # Maximizar janela
        if not self.options.headless:
            FirefoxDriver.driver.maximize_window()

    def get(self):
        return FirefoxDriver.driver

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

    def execute_script(self, script: str, *args):
        return self.get().execute_script(script, *args)

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
        # Não há suporte direto como no Chrome; é necessário limpar o perfil manualmente
        raise NotImplementedError("Firefox não suporta a limpeza de dados via automação diretamente.")

    def save_screenshot(self, name: str) -> str:
        name_formated = re.sub(r"\.[^\.]*$", '', name)
        name_formated = f"{name_formated}.jpg"
        self.get().save_screenshot(name_formated)
        return name_formated

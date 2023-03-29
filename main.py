import threading
import time
import tkinter as tk
from tkinter import ttk

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class AutoCookieClicker():
    def __init__(self, toplevel):
        self._raiz = toplevel
        self._raiz.title('Auto Clicker Cookie')
        self._raiz.geometry('250x150')
        self._clicking_big_cookie = False
        self._auto_upgrades = False
        self._driver = None

        self._raiz.bind("<End>", self.toggle_key)

    def open_cookie_game_browser(self):
        # Abre o browser direto no game
        chrome_options = Options()
        chrome_options.add_experimental_option('detach', True)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(
            service=service, options=chrome_options)
        self._driver = driver
        self._driver.get('https://orteil.dashnet.org/cookieclicker/')

        self._driver.maximize_window()

        # Fecha notificações e seleciona linguagem
        time.sleep(1.5)
        cookie_acept_btn = self._driver.find_element(
            By.XPATH, '/html/body/div[1]/div/a[1]')
        cookie_acept_btn.click()

        time.sleep(0.5)
        langage_button = self._driver.find_element(By.ID, 'langSelect-PT-BR')
        langage_button.click()

    def toggle_key(self, key):
        self._clicking_big_cookie = not self._clicking_big_cookie
        print(self._clicking_big_cookie)
        print(key)

    def big_cookie_clicker(self):
        try:
            while True:
                if self._driver and self._clicking_big_cookie:
                    big_cookie = self._driver.find_element(By.ID, 'bigCookie')
                    big_cookie.click()
        except StaleElementReferenceException:
            pass

    def do_upgrades(self):
        if self._auto_upgrades:
            products = self._driver.find_elements(
                By.CSS_SELECTOR, 'div.product.unlocked.enabled')
            if products:
                try:
                    products[-1].click()
                except:
                    pass
            time.sleep(0.5)

    def run_threads(self):
        big_cookie_clicker_t = threading.Thread(target=self.big_cookie_clicker)
        do_upgrades_t = threading.Thread(target=self.do_upgrades)
        do_upgrades_t.start()
        big_cookie_clicker_t.start()

    def create_widgets(self):
        # Cria os frames
        self.frame1 = ttk.Frame(self._raiz)
        self.frame1.pack(fill=tk.BOTH, padx=10, pady=5)
        self.frame2 = ttk.Frame(self._raiz)
        self.frame2.pack(fill=tk.BOTH, padx=10, pady=5)
        self.frame3 = ttk.Frame(self._raiz)
        self.frame3.pack(fill=tk.BOTH, padx=10, pady=5)

        # Criando botões (widgets)
        self.open_cookie_game_browser_btn = ttk.Button(
            self.frame1, text='Abrir Cookie Clicker Game', command=self.open_cookie_game_browser)
        self.auto_upgrade_btn = ttk.Button(self.frame2, text='Auto Upgrade')
        self.auto_clicker_btn = ttk.Button(self.frame3, text='Auto Clicker')

        # Posicionando os botões (wiidgets)
        self.open_cookie_game_browser_btn.pack(fill=tk.BOTH)
        self.auto_upgrade_btn.pack(fill=tk.BOTH)
        self.auto_clicker_btn.pack(fill=tk.BOTH)


if __name__ == '__main__':
    janela = tk.Tk()
    auto_cookie = AutoCookieClicker(janela)
    auto_cookie.create_widgets()
    auto_cookie.run_threads()
    janela.mainloop()

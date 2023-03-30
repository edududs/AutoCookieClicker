import random
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

from pynput.keyboard import Key, KeyCode, Listener
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
        self._raiz.geometry('200x150')
        self._clicking_big_cookie = False
        self._auto_upgrades = False
        self._auto_improvments = False
        self._driver = None

        self._listener = Listener(self.toggle_key)
        self._listener.start()

    def open_cookie_game_browser(self):
        if self._driver:
            messagebox.showerror("Erro", "O navegador já está aberto!")
            raise InterruptedError('O navegador já está aberto')

        # Abre o browser direto no game
        chrome_options = Options()
        chrome_options.add_experimental_option('detach', True)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(
            service=service, options=chrome_options)
        self._driver = driver
        self._driver.maximize_window()
        self._driver.get('https://orteil.dashnet.org/cookieclicker/')

        # Fecha notificações e seleciona linguagem
        time.sleep(1.5)
        cookie_acept_btn = self._driver.find_element(
            By.XPATH, '/html/body/div[1]/div/a[1]')
        cookie_acept_btn.click()

        time.sleep(0.5)
        langage_button = self._driver.find_element(By.ID, 'langSelect-PT-BR')
        langage_button.click()

        self.run_threads()

    def toggle_key(self, key):
        if key == Key.f8:
            self._clicking_big_cookie = not self._clicking_big_cookie
            print(key, self._clicking_big_cookie)
        elif key == Key.insert:
            self._auto_upgrades = not self._auto_upgrades
            print(key, self._auto_upgrades)
        elif key == Key.page_up:
            self._auto_improvments = not self._auto_improvments
            print(key, self._auto_improvments)

    def toggle_btn_click(self):
        if self._driver:
            self._clicking_big_cookie = not self._clicking_big_cookie

    def toggle_btn_upgrade(self):
        if self._driver:
            self._auto_upgrades = not self._auto_upgrades

    def toggle_btn_improvment(self):
        if self._driver:
            self._auto_improvments = not self._auto_improvments

    def big_cookie_clicker(self):
        try:
            while True:
                if self._clicking_big_cookie and self._driver:
                    big_cookie = self._driver.find_element(By.ID, 'bigCookie')
                    big_cookie.click()
        except StaleElementReferenceException:
            pass

    def do_upgrades(self):
        try:
            while True:
                if self._auto_upgrades and self._driver:
                    products = self._driver.find_elements(
                        By.CSS_SELECTOR, 'div.product.unlocked.enabled')
                    if products:
                        try:
                            products[-1].click()
                        except:
                            pass
                time.sleep(0.5)
        except StaleElementReferenceException:
            pass

    def do_improvments(self):
        while True:
            if self._auto_improvments:
                improvments = self._driver.find_elements(
                    By.CSS_SELECTOR, 'div.crate.upgrade.enabled')
                print(improvments)
                if improvments:
                    random.choice(improvments).click()

            time.sleep(0.5)

    def run_threads(self):
        do_upgrades_t = threading.Thread(target=self.do_upgrades)
        do_upgrades_t.start()
        big_cookie_clicker_t = threading.Thread(target=self.big_cookie_clicker)
        big_cookie_clicker_t.start()
        do_improvments_t = threading.Thread(target=self.do_improvments)
        do_improvments_t.start()

    def create_widgets(self):
        # Cria os frames
        self.frame1 = ttk.Frame(self._raiz)
        self.frame1.pack(expand=True, fill=tk.BOTH, padx=10, pady=3)
        self.frame2 = ttk.Frame(self._raiz)
        self.frame2.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        self.frame3 = ttk.Frame(self._raiz)
        self.frame3.pack(fill=tk.BOTH, padx=10, pady=5)
        self.frame4 = ttk.Frame(self._raiz)
        self.frame4.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        # Criando botões (widgets)
        self.open_cookie_game_browser_btn = ttk.Button(
            self.frame1, text='Abrir Cookie Clicker Game', command=self.open_cookie_game_browser)
        self.auto_upgrade_btn = ttk.Button(
            self.frame2, text='Auto Upgrade', command=self.toggle_btn_upgrade)
        self.auto_clicker_btn = ttk.Button(
            self.frame3, text='Auto Clicker', command=self.toggle_btn_click)
        self.auto_improvment_btn = ttk.Button(
            self.frame4, text='Auto Improvments', command=self.toggle_btn_improvment)

        # Posicionando os botões (wiidgets)
        self.open_cookie_game_browser_btn.pack(fill=tk.BOTH)
        self.auto_upgrade_btn.pack(fill=tk.BOTH)
        self.auto_clicker_btn.pack(fill=tk.BOTH)
        self.auto_improvment_btn.pack(fill=tk.BOTH)

    def on_closing(self):
        if self._driver:
            self._driver.quit()
        self._raiz.destroy()
        sys.exit()

    def __del__(self):
        self._listener.stop()


if __name__ == '__main__':
    janela = tk.Tk()
    auto_cookie = AutoCookieClicker(janela)
    auto_cookie.create_widgets()
    janela.protocol("WM_DELETE_WINDOW", auto_cookie.on_closing)
    janela.mainloop()

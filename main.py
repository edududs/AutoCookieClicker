import random
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

from PIL import Image, ImageTk
from pynput.keyboard import Key, KeyCode, Listener
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class AutoCookieClicker:
    def __init__(self, toplevel):
        self._raiz = toplevel
        self._raiz.title("Auto Clicker Cookie")
        self._raiz.geometry("380x230")
        self._clicking_big_cookie = False
        self._auto_upgrades = False
        self._auto_improvments = False
        self._driver = None

        self._listener = Listener(self.toggle_key)
        self._listener.start()

    def open_cookie_game_browser(self):
        if self._driver:
            messagebox.showerror("Erro", "O navegador já está aberto!")
            raise InterruptedError("O navegador já está aberto")

        # Abre o browser direto no game
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        self._driver = driver
        self._driver.maximize_window()
        self._driver.get("https://orteil.dashnet.org/cookieclicker/")

        if self._driver:
            self.lbl_frm_open_game.configure(text="On", foreground="green")
        else:
            self.lbl_frm_open_game.configure(text="Off", foreground="red")

        # Fecha notificações e seleciona linguagem
        time.sleep(1.5)
        cookie_acept_btn = self._driver.find_element(
            By.XPATH, "/html/body/div[1]/div/a[1]"
        )
        cookie_acept_btn.click()

        time.sleep(0.5)
        langage_button = self._driver.find_element(By.ID, "langSelect-PT-BR")
        langage_button.click()

        self.run_threads()

    def toggle_key(self, key):
        if key == Key.f8:
            self._clicking_big_cookie = not self._clicking_big_cookie
            if self._clicking_big_cookie:
                self.lbl_auto_click.configure(text="On", foreground="green")
            else:
                self.lbl_auto_click.configure(text="Off", foreground="red")
            print(key, self._clicking_big_cookie)
        elif key == Key.insert:
            self._auto_upgrades = not self._auto_upgrades
            if self._auto_upgrades:
                self.lbl_auto_upgrade.configure(text="On", foreground="green")
            else:
                self.lbl_auto_upgrade.configure(text="Off", foreground="red")
            print(key, self._auto_upgrades)
        elif key == Key.page_up:
            self._auto_improvments = not self._auto_improvments
            if self._auto_improvments:
                self.lbl_auto_improvments.configure(text="On", foreground="green")
            else:
                self.lbl_auto_improvments.configure(text="Off", foreground="red")
            print(key, self._auto_improvments)

    def toggle_btn_click(self):
        if self._driver:
            self._clicking_big_cookie = not self._clicking_big_cookie
            if self._clicking_big_cookie:
                self.lbl_auto_click.configure(text="On", foreground="green")
            else:
                self.lbl_auto_click.configure(text="Off", foreground="red")

    def toggle_btn_upgrade(self):
        if self._driver:
            self._auto_upgrades = not self._auto_upgrades
            if self._auto_upgrades:
                self.lbl_auto_upgrade.configure(text="On", foreground="green")
            else:
                self.lbl_auto_upgrade.configure(text="Off", foreground="red")

    def toggle_btn_improvment(self):
        if self._driver:
            self._auto_improvments = not self._auto_improvments
            if self._auto_improvments:
                self.lbl_auto_improvments.configure(text="On", foreground="green")
            else:
                self.lbl_auto_improvments.configure(text="Off", foreground="red")

    def big_cookie_clicker(self):
        try:
            while True:
                if self._clicking_big_cookie and self._driver:
                    big_cookie = self._driver.find_element(By.ID, "bigCookie")
                    big_cookie.click()
        except StaleElementReferenceException:
            pass

    def do_upgrades(self):
        try:
            while True:
                if self._auto_upgrades and self._driver:
                    products = self._driver.find_elements(
                        By.CSS_SELECTOR, "div.product.unlocked.enabled"
                    )
                    if products:
                        try:
                            products[-1].click()
                        except:
                            pass
                time.sleep(0.5)
        except StaleElementReferenceException:
            pass

    def do_improvments(self):
        try:
            while True:
                if self._auto_improvments:
                    improvments = self._driver.find_elements(
                        By.CSS_SELECTOR, "div.crate.upgrade.enabled"
                    )
                    if improvments:
                        try:
                            random.choice(improvments).click()
                        except:
                            pass
                time.sleep(0.5)
        except StaleElementReferenceException:
            pass

    def run_threads(self):
        do_upgrades_t = threading.Thread(target=self.do_upgrades)
        do_upgrades_t.start()
        big_cookie_clicker_t = threading.Thread(target=self.big_cookie_clicker)
        big_cookie_clicker_t.start()
        do_improvments_t = threading.Thread(target=self.do_improvments)
        do_improvments_t.start()

    def create_widgets(self):
        # Cria os frames
        self.frm_img_cookie = ttk.Frame(self._raiz, padding=10)
        self.frm_img_cookie.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.frm_open_game = ttk.Frame(self._raiz, padding=10)
        self.frm_open_game.grid(row=2, column=0, sticky="nsew")
        self.frm_auto_click = ttk.Frame(self._raiz, padding=10)
        self.frm_auto_click.grid(row=0, column=1, sticky="nsew")
        self.frm_auto_upgrade = ttk.Frame(self._raiz, padding=10)
        self.frm_auto_upgrade.grid(row=1, column=1, sticky="nsew")
        self.frm_auto_improvments = ttk.Frame(self._raiz, padding=10)
        self.frm_auto_improvments.grid(row=2, column=1, sticky="nsew")

        # Criando Labels
        self.lbl_frm_open_game = ttk.Label(
            self.frm_open_game, text="Off", foreground="red"
        )
        self.lbl_auto_click = ttk.Label(
            self.frm_auto_click, text="Off", foreground="red"
        )
        self.lbl_auto_upgrade = ttk.Label(
            self.frm_auto_upgrade, text="Off", foreground="red"
        )
        self.lbl_auto_improvments = ttk.Label(
            self.frm_auto_improvments, text="Off", foreground="red"
        )
        self.lbl_auto_click.grid(row=1, column=0, padx=1, pady=1)
        self.lbl_auto_upgrade.grid(row=1, column=0, padx=1, pady=1)
        self.lbl_auto_improvments.grid(row=1, column=0, padx=1, pady=1)
        self.lbl_frm_open_game.grid(row=1, column=0, padx=1, pady=1)

        # Criando botões (widgets)
        self.open_cookie_game_browser_btn = ttk.Button(
            self.frm_open_game,
            text="Abrir Cookie Clicker Game",
            command=self.open_cookie_game_browser,
            width=25,
        )
        self.auto_clicker_btn = ttk.Button(
            self.frm_auto_click,
            text="Auto Clicker",
            command=self.toggle_btn_click,
            width=25,
        )
        self.auto_upgrade_btn = ttk.Button(
            self.frm_auto_upgrade,
            text="Auto Upgrade",
            command=self.toggle_btn_upgrade,
            width=25,
        )
        self.auto_improvment_btn = ttk.Button(
            self.frm_auto_improvments,
            text="Auto Improvments",
            command=self.toggle_btn_improvment,
            width=25,
        )
        # Colocando imagem
        self.img_cookie = ImageTk.PhotoImage(
            Image.open("pngwing.com.png").resize((140, 140))
        )
        self.panel = ttk.Label(self.frm_img_cookie, image=self.img_cookie)
        self.panel.pack(
            fill=tk.BOTH,
        )

        # Posicionando os botões (widgets)
        self.open_cookie_game_browser_btn.grid(row=0, column=0, padx=5, pady=5)
        self.auto_upgrade_btn.grid(row=0, column=0, padx=5, pady=5)
        self.auto_clicker_btn.grid(row=0, column=0, padx=5, pady=5)
        self.auto_improvment_btn.grid(row=0, column=0, padx=5, pady=5)

    def on_closing(self):
        if self._driver:
            self._driver.quit()
        self._raiz.destroy()
        sys.exit()

    def __del__(self):
        self._listener.stop()


if __name__ == "__main__":
    janela = tk.Tk()
    auto_cookie = AutoCookieClicker(janela)
    auto_cookie.create_widgets()
    janela.protocol("WM_DELETE_WINDOW", auto_cookie.on_closing)
    janela.mainloop()

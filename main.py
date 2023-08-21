import random
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

from PIL import Image, ImageTk
from pynput.keyboard import Key, KeyCode, Listener
from pynput.mouse import Button, Controller
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
        self._clicando = False
        self._driver = None
        self.mouse = Controller()

        # Iniciando Listener para capturar a tecla pressionada durante a execução da aplicação
        self._listener = Listener(self.toggle_key)
        self._listener.start()

    def open_cookie_game_browser(self):
        """
        Opens the cookie game browser.

        This function opens the browser and navigates to the cookie game website (https://orteil.dashnet.org/cookieclicker/). It checks if the browser is already open and raises an error if it is. It then opens the browser using the ChromeDriverManager and ChromeOptions. The browser window is maximized and the game website is loaded.

        After opening the browser, the function updates the status of the game on the GUI. If the browser is open, the label text is set to "On" and the foreground color is set to green. Otherwise, the label text is set to "Off" and the foreground color is set to red.

        The function waits for 1.5 seconds and then clicks on the cookie acceptance button and the language selection button on the game website.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
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

    def toggle_key(self, key):
        """
        Toggles the state of a key and updates the corresponding label and color.

        Parameters:
            key (Key or KeyCode): The key to toggle.

        Returns:
            None
        """
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
        elif key == KeyCode(char="]"):
            self._clicando = not self._clicando
            print(key, self._clicando)

    def toggle_btn_click(self):
        """
        Toggles the state of the button click.

        This function is called when the toggle button is clicked. It checks the current state of the
        self._clicking_big_cookie attribute and toggles its value. If the attribute is True, it changes
        the text of self.lbl_auto_click to "On" and sets the foreground color to green. If the attribute
        is False, it changes the text of self.lbl_auto_click to "Off" and sets the foreground color to red.
        """
        if self._driver:
            self._clicking_big_cookie = not self._clicking_big_cookie
            if self._clicking_big_cookie:
                self.lbl_auto_click.configure(text="On", foreground="green")
            else:
                self.lbl_auto_click.configure(text="Off", foreground="red")

    def toggle_btn_upgrade(self):
        """
        Toggles the upgrade button.

        This function is responsible for toggling the upgrade button in the UI. It checks the current state of the `_auto_upgrades` flag and updates it accordingly. If the flag is `True`, it sets it to `False`, and vice versa.

        The function also updates the text and foreground color of the `lbl_auto_upgrade` label based on the new state of `_auto_upgrades`. If the flag is `True`, the label text is set to "On" and the foreground color is set to "green". If the flag is `False`, the label text is set to "Off" and the foreground color is set to "red".

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        if self._driver:
            self._auto_upgrades = not self._auto_upgrades
            if self._auto_upgrades:
                self.lbl_auto_upgrade.configure(text="On", foreground="green")
            else:
                self.lbl_auto_upgrade.configure(text="Off", foreground="red")

    def toggle_btn_improvment(self):
        """
        Toggles the button improvement feature.

        This function toggles the state of the button improvement feature. If the feature is currently enabled, it will be disabled, and vice versa. The state of the feature is stored in the `_auto_improvements` variable.

        Parameters:
            self (_): The instance of the class.

        Returns:
            None
        """
        if self._driver:
            self._auto_improvments = not self._auto_improvments
            if self._auto_improvments:
                self.lbl_auto_improvments.configure(text="On", foreground="green")
            else:
                self.lbl_auto_improvments.configure(text="Off", foreground="red")

    def create_widgets(self):
        """
        Creates and positions frames, labels, and buttons for the UI.
        """
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
        """
        Closes the application by quitting the driver and destroying the root window.

        No parameters.

        No return value.
        """
        if self._driver:
            self._driver.quit()
        self._raiz.destroy()
        sys.exit()

    def __del__(self):
        """
        Delete the object and stop the listener.
        """
        self._listener.stop()


class GameThreads:
    def __init__(self, game: AutoCookieClicker) -> None:
        self.game = game

    def clicker(self):
        """
        Clicks the mouse repeatedly while the game is running.

        This function checks if the game is currently in clicking mode and if so, it
        simulates a left mouse click. It then pauses for a very short amount of time
        before repeating the process.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        while True:
            if self.game._clicando:
                self.game.mouse.click(Button.left, 1)
            time.sleep(0.0001)

    def big_cookie_clicker(self):
        """
        Clicks on the big cookie element as long as the game's clicking big cookie flag is set to True
        and the game's driver is available.

        Parameters:
            self: The instance of the class.

        Returns:
            None
        """
        try:
            while True:
                if self.game._clicking_big_cookie and self.game._driver:
                    big_cookie = self.game._driver.find_element(By.ID, "bigCookie")
                    big_cookie.click()
        except StaleElementReferenceException:
            pass

    def do_upgrades(self):
        """
        Runs an upgrade loop that continuously checks for unlocked and enabled products and clicks on the last one.

        Parameters:
            None

        Returns:
            None
        """
        try:
            while True:
                if self.game._auto_upgrades and self.game._driver:
                    products = self.game._driver.find_elements(
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
        """
        Executes a loop that continuously checks for available improvements in the game and clicks on a random improvement element if found.

        This function is executed by the `do_improvements` method of the `self` object.

        Parameters:
            None

        Returns:
            None
        """
        try:
            while True:
                if self.game._auto_improvments:
                    improvments = self.game._driver.find_elements(
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
        """
        Runs multiple threads concurrently to perform various tasks.
        This function creates three threads: `do_upgrades_t`, `big_cookie_clicker_t`, and `do_improvments_t`.
        Each thread is responsible for executing a specific method in a separate thread.
        The `do_upgrades_t` thread executes the `do_upgrades` method.
        The `big_cookie_clicker_t` thread executes the `big_cookie_clicker` method.
        The `do_improvments_t` thread executes the `do_improvments` method.
        """
        do_upgrades_t = threading.Thread(target=self.do_upgrades)
        do_upgrades_t.start()
        big_cookie_clicker_t = threading.Thread(target=self.big_cookie_clicker)
        big_cookie_clicker_t.start()
        do_improvments_t = threading.Thread(target=self.do_improvments)
        do_improvments_t.start()

    def run_auto_click_mouse(self):
        """
        Run the auto click mouse function.

        This function creates a new thread to execute the `clicker` method.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        clicker_t = threading.Thread(target=self.clicker)
        clicker_t.start()


if __name__ == "__main__":
    janela = tk.Tk()
    auto_cookie = AutoCookieClicker(janela)
    game_threads = GameThreads(auto_cookie)
    game_threads.run_auto_click_mouse()
    game_threads.run_threads()
    auto_cookie.create_widgets()
    janela.protocol("WM_DELETE_WINDOW", auto_cookie.on_closing)
    janela.mainloop()

import selenium.webdriver.remote.webelement
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
from pyautogui import press


URL = "https://www.ktuvit.me/"
WAIT = 5


def get_element(driver: webdriver.Chrome, kind: By, search: str, clear: bool = False, multiple: bool = False) \
        -> list[selenium.webdriver.remote.webelement.WebElement] | selenium.webdriver.remote.webelement.WebElement:

    WebDriverWait(driver, WAIT).until(ec.presence_of_element_located((kind, search)))

    if multiple:
        e = driver.find_elements(kind, search)
    else:
        e = driver.find_element(kind, search)

    if clear:
        e.clear()

    return e


def get_element_if_contains(driver: webdriver.Chrome, kind: By, search: str, contain: str,
                            func=lambda a, b: a.text == b) -> selenium.webdriver.remote.webelement.WebElement | None:
    elements = get_element(driver, kind, search, False, True)
    element = None

    for elem in elements:
        if func(elem, contain):
            element = elem
            break

    return element


def login(driver: webdriver.Chrome, username: str, password: str) -> None:
    login_button = get_element_if_contains(driver, By.CLASS_NAME, "dropdown-toggle", "התחברות")
    login_button.click()

    email_field = get_element(driver, By.ID, "navbarlogin_tb_loginEmail")
    password_field = get_element(driver, By.ID, "navbarlogin_tb_loginPassword")

    email_field.send_keys(username)
    password_field.send_keys(password + Keys.ENTER)


def search_and_click(driver: webdriver.Chrome, movie_name: str):
    search_tab = get_element(driver, By.ID, "tb_searchAssistance")
    search_tab.send_keys(movie_name)

    movie_options = get_element(driver, By.CLASS_NAME, "ui-menu-item", multiple=True)

    if len(movie_options) == 0:
        return None

    movie_options[0].click()


def select_subtitles(driver: webdriver.Chrome):
    i = 1
    sub = (0, None)

    while True:
        try:
            downloads = int(get_element(driver, By.XPATH, f"""//*[@id="subtitlesList"]/tbody/tr[{i}]/td[5]""").text)
            download_link = get_element(driver, By.XPATH, f"""//*[@id="subtitlesList"]/tbody/tr[{i}]/td[6]/a[2]""")
        except Exception:
            break

        if sub[0] < downloads:
            sub = downloads, download_link

        i += 1

    sub[1].click()

    sleep(1)
    press('enter')


def main(movie_name):
    chrome_driver_path = ChromeDriverManager().install()
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Open incognito window
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get(URL)

    search_and_click(driver, movie_name)
    login(driver, "jonathan.lichtermiron@gmail.com", "4090dina")
    sleep(1)
    select_subtitles(driver)
    sleep(1)
    driver.quit()


if __name__ == "__main__":
    main("פורסט גאמפ")

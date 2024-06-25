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
import helper
from os import system


URL = "https://www.ktuvit.me/"
WAIT = 5


def get_element(driver: webdriver.Chrome, kind: By, search: str, clear: bool = False, multiple: bool = False, wait=WAIT) \
        -> list[selenium.webdriver.remote.webelement.WebElement] | selenium.webdriver.remote.webelement.WebElement:

    WebDriverWait(driver, wait).until(ec.presence_of_element_located((kind, search)))

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
    sleep(1)


def search_and_click(driver: webdriver.Chrome, movie_name: str):
    search_tab = get_element(driver, By.ID, "tb_searchAssistance")
    search_tab.send_keys(movie_name)

    try:
        movie_options = get_element(driver, By.CLASS_NAME, "ui-menu-item", multiple=True)

        if len(movie_options) == 0:
            helper.pop_msg("Error subtitles", "Could not find movie")
            return False

        movie_options[0].click()
        return True

    except Exception:
        helper.pop_msg("Error subtitles", "Could not find movie")
        return False


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

    try:
        btn = get_element(driver, By.ID, "closePopup", wait=0.5)
        btn.click()

    except Exception:
        pass

    sub[1].click()
    sleep(2)


def main(movie_name: str, progress=helper.Progress(6)):
    progress.add_one()

    folder = helper.change_dir_to("Downloads")

    chrome_driver_path = ChromeDriverManager().install()
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Open incognito window
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': folder,  # Specify your download directory
        'download.prompt_for_download': False,  # Disable prompting for download
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(URL)
    progress.add_one()

    val = search_and_click(driver, movie_name)

    if not val:
        progress.set(0)
        driver.quit()
        return

    progress.add_one()

    login(driver, "jonathan.lichtermiron@gmail.com", "4090dina")
    progress.add_one()

    select_subtitles(driver)
    progress.add_one()

    driver.quit()
    file = helper.get_file(folder, lambda f:  f.endswith(".srt"))
    system(f'ren "{file}" "{movie_name}.srt"')
    progress.add_one()


def call_main(movie_name: str, progress=helper.Progress(6)):
    try:
        main(movie_name, progress)

    except Exception as e:
        helper.pop_msg("Error subtitles", "Error happened in getSubtitles:\n" + str(e))
        progress.set(0)


if __name__ == "__main__":
    main("forrest gump")

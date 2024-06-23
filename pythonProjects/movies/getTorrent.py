import selenium.webdriver.remote.webelement
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import requests
import helper
from multiprocessing import Value


URL = "https://yts.mx/"
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


def search_and_click(driver: webdriver.Chrome, movie_name: str):
    search_tab = get_element(driver, By.ID, "quick-search-input", clear=True)
    search_tab.send_keys(movie_name)

    sleep(1)

    try:
        movie = get_element(driver, By.XPATH, "/html/body/div[4]/div[2]/ul/li/a")
        new_url = movie.get_attribute("href")

    except Exception:  # it means that more than one option was popped out or no option was popped out
        try:
            movie = get_element(driver, By.XPATH, "/html/body/div[4]/div[2]/ul/li[1]/a")  # pick the first option
            new_url = movie.get_attribute("href")

        except Exception:
            raise RuntimeError("Could not find movie")

    driver.get(new_url)
    sleep(1)


def select_torrent(driver: webdriver.Chrome, movie: str):
    valid = True
    i = 1

    torrent = None

    while valid:
        try:
            option = get_element(driver, By.XPATH, f"""//*[@id="movie-info"]/p/a[{i}]""")
            title = option.get_attribute("title")

            # the 720p option is one of the firsts. We want to download it instead of iterating all the options

            if "Torrent" in title:
                if "720p" in title:  # first we check for the 720p version
                    torrent = option
                    valid = False

                if "1080p" in title:
                    torrent = option
                    valid = False

                if "2160p" in title:
                    torrent = option
                    valid = False

            i += 1

        except Exception:
            valid = False

    if torrent is None:
        raise RuntimeError("Cannot find torrent")

    url_torrent = torrent.get_attribute("href")

    r = requests.get(url_torrent, allow_redirects=True)

    helper.change_dir_to('Downloads')
    with open(f'{movie}.torrent', 'wb') as file:
        file.write(r.content)

    sleep(1)


def main(movie_name, progress: Value = Value('i', 0)):
    chrome_driver_path = ChromeDriverManager().install()
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Open incognito window
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(URL)
    progress.value += 1

    search_and_click(driver, movie_name)
    progress.value += 1

    select_torrent(driver, movie_name)
    progress.value += 1

    driver.quit()
    progress.value += 1


if __name__ == "__main__":
    main("forrest gump")


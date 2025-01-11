
from helper import *


class ChromeDriverManager64(ChromeDriverManager):
    def __init__(self):
        super().__init__(os_system_manager="win64")

    def get_os_type(self):
        return "win64"


URL = "https://yts.mx/"


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
            pop_msg("Error torrent", "Could not find movie")
            return False

    driver.get(new_url)
    sleep(1)

    return True


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

    return url_torrent


def main(movie_name, progress=Progress(5)):
    progress.add_one()

    chrome_driver_path = ChromeDriverManager(os_system_manager=OperationSystemManager("win32")).install()

    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Open incognito window
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(URL)
    progress.add_one()

    val = search_and_click(driver, movie_name)

    if not val:
        progress.set_end()
        driver.quit()
        return

    progress.add_one()

    url_torrent = select_torrent(driver, movie_name)
    progress.add_one()

    driver.quit()

    r = requests.get(url_torrent, allow_redirects=True, stream=True)

    with open(f'{DOWNLOADS_PATH}\\{movie_name}.torrent', 'wb') as file:
        for chunk in r.iter_content(chunk_size=8192):  # Stream the file in chunks
            file.write(chunk)

    progress.add_one()


def call_main(movie_name: str, progress=Progress(6)):
    try:
        main(movie_name, progress)

    except Exception as e:
        pop_msg("Error torrent", f"Unexpected error happened while downloading torrent")
        progress.set_end()
        print(e)


if __name__ == "__main__":
    main("forrest gump")

from ultralytics import download

from helper import *


URL = "https://www.ktuvit.me/"


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
            pop_msg("Error subtitles", "Could not find movie")
            return False

        movie_options[0].click()
        return True

    except Exception:
        pop_msg("Error subtitles", "Could not find movie")
        return False


def select_subtitles(driver: webdriver.Chrome):
    i = 1
    sub = ("", 0)

    while True:
        try:
            downloads = int(get_element(driver, By.XPATH, f"""//*[@id="subtitlesList"]/tbody/tr[{i}]/td[5]""").text)
            subs_element = get_element(driver, By.XPATH, f"""//*[@id="subtitlesList"]/tbody/tr[{i}]/td[6]/a[2]""")
            subs_id = subs_element.get_attribute("data-subtitle-id")

        except Exception:
            break

        if sub[1] < downloads:
            sub = subs_id, downloads

        i += 1

    try:
        btn = get_element(driver, By.ID, "closePopup", wait=0.5)
        btn.click()

    except Exception:
        pass

    return sub[0]


def download_subtitles(base_url: str, film_id: str, subtitle_id: str, output_path: str, font_size=0, font_color="", predefined_layout=-1) -> dict | None:
    # Construct the full URL
    url = f"{base_url}/Services/ContentProvider.svc/RequestSubtitleDownload"

    # Create the payload
    data = {
        "request": {
            "FilmID": film_id,
            "SubtitleID": subtitle_id,
            "FontSize": font_size,
            "FontColor": font_color,
            "PredefinedLayout": predefined_layout
        }
    }

    # Set headers
    headers = {
        "Content-Type": "application/json"
    }

    # Send the POST request
    try:
        response = requests.post(url, json=data, headers=headers)

    except Exception as e:
        pop_msg("Error subtitles", "Error while getting download ID\n" + e)
        return False

    if response:
        d = json.loads(response.json()["d"])  # d is the dictionary with data about the subtitles downloads info

    else:
        return False

    valid_in = d["ValidIn"]
    download_id = d["DownloadIdentifier"]  # download id of the subtitles

    if valid_in > 0:
        print(f"Waiting {valid_in} seconds before downloading...")
        time.sleep(valid_in)

    download_url = f"{base_url}/Services/DownloadFile.ashx?DownloadIdentifier={download_id}"

    sleep(0.2)
    try:
        response = requests.get(download_url, stream=True)

        # Save the file to the specified output path
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  # Stream the file in chunks
                file.write(chunk)

        return True

    except Exception as e:
        pop_msg("Error subtitles", "Error while downloading subtitles\n" + e)
        return False


def main(movie_name: str, progress=Progress(6)):
    progress.add_one()

    chrome_driver_path = ChromeDriverManager(os_system_manager=OperationSystemManager("win32")).install()
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Open incognito window
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': DOWNLOADS_PATH,  # Specify your download directory
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
        progress.set_end()
        driver.quit()
        return

    film_id = execute(driver, "return filmID;")
    progress.add_one()

    login(driver, "jonathan.lichtermiron@gmail.com", "4090dina")
    progress.add_one()

    subs_id = select_subtitles(driver)
    progress.add_one()

    driver.quit()

    if not download_subtitles(URL, film_id, subs_id, DOWNLOADS_PATH + "\\" + movie_name + ".srt"):
        pop_msg("Error subtitles", "Could not download movie")

    progress.add_one()


def call_main(movie_name: str, progress=Progress(6)):
    try:
        main(movie_name, progress)

    except Exception as e:
        pop_msg("Error subtitles", "Unexpected error happened while downloading subtitles")
        progress.set_end()
        print(e)


if __name__ == "__main__":
    main("forrest gump")

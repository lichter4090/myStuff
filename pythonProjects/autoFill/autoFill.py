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
import continue_window


URL = "https://auth.greeninvoice.co.il/signin?rurl=https://app.greeninvoice.co.il/lobby?login=true&t=1714293791090"
WAIT = 5
CNT = 0


def scroll(driver: webdriver.Chrome, amount: int):
    driver.execute_script(f"window.scrollBy(0, {amount});")


def get_element(driver: webdriver.Chrome, kind: By, search: str, clear: bool = False, multiple: bool = False) \
        -> list[selenium.webdriver.remote.webelement.WebElement] | selenium.webdriver.remote.webelement.WebElement:
    WebDriverWait(driver, WAIT).until(
        ec.presence_of_element_located((kind, search))
    )

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
    username_element = get_element(driver, By.ID, "email", True)
    password_element = get_element(driver, By.ID, "password", True)

    username_element.send_keys(username)
    password_element.send_keys(password + Keys.ENTER)


def get_to_receipt_page(driver) -> bool:
    #  the only button with this class so no need for get_element_if_contains
    plus_button = get_element(driver, By.CLASS_NAME, "plus__btn")
    plus_button.click()

    sleep(0.5)
    receipt_button = get_element_if_contains(driver, By.CLASS_NAME, "dropdown-plus__list-item", "חשבונית מס / קבלה")

    if receipt_button is None:
        return False

    receipt_button.click()
    return True


def put_date(driver: webdriver.Chrome, date: list) -> bool:
    day, month, year = date
    date_panel = get_element(driver, By.XPATH, '//*[@id="app"]/div[1]/main/section/div[2]/div/div/form/div[2]/div[1]/div[2]/div/div/div/label/span')
    date_panel.click()

    date_button = get_element_if_contains(driver, By.CLASS_NAME, "cell", f"{year}-{month}-{day}",
                                          func=lambda a, b: a.get_attribute("title") == b)

    if date_button is None:
        print(f"Invalid date {year}-{month}-{day}")
        print("Probably because it is too far to the past")
        return False

    date_button.click()

    return True


def add_single_item(driver: webdriver.Chrome, item: dict):
    global CNT
    sleep(1)
    if CNT > 0:
        #  the only button with this class so no need for get_element_if_contains
        add_line_button = get_element(driver, By.XPATH, '//*[@id="income-table"]/div/table/tfoot[1]/tr[2]/td[1]/button/span')
        add_line_button.click()

    type_button_input = get_element(driver, By.XPATH, '//*[@id="income-item-description"]')
    type_button_input.send_keys(item["kind"])  # send kind of service

    amount_button = get_element(driver, By.ID, "income-item-quantity", clear=True)
    amount_button.send_keys(Keys.BACKSPACE + item["amount"])  # add amount

    price_button = get_element(driver, By.ID, "income-item-price", clear=True)
    price_button.send_keys(item["price_per"])

    open_vat_option = get_element(driver, By.ID, "income-item-vat-type")
    open_vat_option.click()  # opens options of vat

    sleep(0.5)  # wait for the options to pop up

    vat_option = get_element(driver, By.XPATH, '//*[@id="income-item-vat-type"]/div[2]/ul/li[2]/span')
    vat_option.click()  # click the include vat option

    #  the only button with this class so no need for get_element_if_contains (the final submit is also the same, but it is later...)
    submit_button = get_element(driver, By.XPATH, '//*[@id="income-table"]/div/table/tbody[1]/tr/td[8]/div/button/span')
    submit_button.click()

    CNT += 1
    return True


def load_one_receipt(driver, data: dict) -> bool:
    get_to_receipt_page(driver)
    sleep(1)

    client_name = get_element_if_contains(driver, By.CLASS_NAME, "gi-input-new__input", "שם הלקוח", lambda a, b: a.get_attribute("aria-label") == b)
    description = get_element(driver, By.ID, "description")

    client_name.send_keys(data["name"])
    description.send_keys(data["description"])

    if not put_date(driver, data["date"]):
        return False

    scroll(driver, 400)

    for item in data["items"]:
        add_single_item(driver, item)
        scroll(driver, 75)

    scroll(driver, 600)
    sleep(1)

    open_income_options = get_element(driver, By.XPATH, '//*[@id="type"]/div[1]/span')
    open_income_options.click()

    sleep(2)

    income_option = get_element_if_contains(driver, By.CLASS_NAME, "gi-select-new__list-option", data["income_kind"])
    income_option.click()

    sum_label = get_element(driver, By.XPATH, '//*[@id="income-table"]/div/table/tfoot[1]/tr[4]/td[7]')

    if not sum_label:
        return False

    sum_button = get_element(driver, By.ID, "price", clear=True)
    sum_button.send_keys(sum_label.text[1:])

    submit_button = get_element(driver, By.XPATH, '//*[@id="app"]/div[1]/main/section/div[2]/div/div/form/div[2]/div[4]/div/table/tbody/tr/td[6]/button/span')
    submit_button.click()


def main(data):
    chrome_driver_path = ChromeDriverManager().install()
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Open incognito window
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get(URL)

    login(driver, "ofra.miron@gmail.com", "4090Oכרש")

    for client in data:
        sleep(2)
        load_one_receipt(driver, client)
        if not continue_window.main():
            exit(0)

    driver.quit()


data_ = [
        {"name": "צוראל קרסנטי",
         "date": ["08", "04", "2024"],
         "description": "פסיכותרפיה",
         "items": [{"kind": "פסיכותרפיה", "amount": "1", "price_per": "360"}],
         "income_kind": "PayBox"},
         ]

if __name__ == "__main__":
    main(data_)

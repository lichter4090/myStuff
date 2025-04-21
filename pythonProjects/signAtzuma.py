import selenium.webdriver.remote.webelement
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import OperationSystemManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import random
import string
import pyautogui

names = [
    "אביתר", "אביחי", "אביגדור", "אבינועם", "אבירם", "אדם", "אדיר", "אהוד", "אהרן", "אופיר",
    "אופק", "אור", "אוראל", "אורון", "אוריה", "אורי", "אוריאל", "אורן", "אושרי", "אייל",
    "איילון", "איילן", "איתמר", "אלדד", "אלון", "אליאור", "אליה", "אליהו", "אלימלך", "אלירן",
    "אלישע", "אמנון", "אמיר", "ארד", "אריאל", "ארז", "בן", "בן ציון", "בנימין", "בר",
    "ברוך", "ברק", "גד", "גדעון", "גולן", "גונן", "גיא", "גיורא", "גלעד", "דביר",
    "דניאל", "דוד", "דולב", "דור", "דורון", "דותן", "הדס", "הראל", "זאב", "זוהר",
    "זיו", "חגי", "חיים", "חנן", "טוביה", "טל", "טמיר", "יאיר", "יואל", "יואב",
    "יובל", "יהודה", "יהונתן", "יוחאי", "יוסי", "יוסף", "יותם", "יניב", "ירון", "יריב",
    "ליאור", "ליעד", "מאור", "מיכאל", "מנחם", "מתן", "נבו", "נדב", "נועם", "נחום",
    "ניב", "ניר", "נתן", "נתנאל", "סהר", "סיני", "סיון", "עומר", "עידו", "עידן",
    "עמוס", "עמיחי", "עמיר", "עמית", "ערן", "פנחס", "צבי", "צחי", "קובי", "קדם",
    "ראובן", "רביב", "רון", "רוני", "רועי", "רפאל", "שגיא", "שחר", "שלו", "שלומי",
    "שמואל", "שמעון", "שקד", "שרון", "תום", "תומר", "תמיר",

    "אביגיל", "אביטל", "אביה", "אגם", "אדווה", "אודיה", "אוולין", "אור", "אוראל", "אורטל",
    "אוריה", "אורין", "אושרת", "איילה", "אילנית", "אלומה", "אלינור", "אליסה", "אליענה", "אלמוג",
    "אלנה", "אלסנדרה", "אמונה", "אסתר", "אפרת", "אריאל", "בת אל", "בת חן", "בתיה", "בר",
    "ברכה", "גבריאלה", "גילי", "גלית", "דבורה", "דנה", "דניאלה", "הדס", "הלל", "ורד",
    "זהבה", "חגית", "חן", "חני", "טובה", "טל", "טליה", "יוכבד", "יולי", "יונה",
    "יונית", "יעל", "ירדן", "כרמל", "ליאל", "ליה", "ליהי", "לימור", "לירון", "מאיה",
    "מזל", "מיכל", "מירב", "מירית", "נעמה", "נופר", "נורית", "נעמי", "ניצן", "נילי",
    "סיון", "סיגל", "ספיר", "עדן", "עדי", "עומר", "עליזה", "עלמה", "עמית", "ענבל",
    "ערגה", "פנינה", "צופית", "קרן", "רבקה", "רות", "רונית", "רוני", "רעות", "שגית",
    "שולמית", "שחר", "שירה", "שני", "שלומית", "שרונה", "שרית", "תאיר", "תהל", "תמר"
]
last_names = [
    "אבוטבול", "אביחיל", "אבידן", "אביטן", "אבנרי", "אברג'יל", "אברהמי", "אבשלום", "אגמון", "אדרי",
    "אוחיון", "אולמן", "אורן", "אורנשטיין", "איילון", "אלבז", "אלדר", "אלון", "אלחיאני", "אלמוג",
    "אלעזר", "אלקבץ", "אלקיים", "אלתר", "אמסלם", "אפלבוים", "אפרתי", "ארד", "אריאלי", "אריה",
    "אשכנזי", "בוחבוט", "בוזגלו", "בוסקילה", "בן אהרון", "בן ארי", "בן בסט", "בן דוד", "בן יוסף", "בן לולו",
    "בן מאיר", "בן סימון", "בן עטר", "בן צבי", "בן שושן", "בן שמעון", "בנימיני", "בר-לב", "ברוך", "ברוקמן",
    "ברוש", "ברזילי", "ברנד", "ברנס", "גבאי", "גבעון", "גולן", "גולדברג", "גולדמן", "גולדשטיין",
    "גורדון", "גורן", "גזית", "גל", "גלבוע", "גלזר", "גלילי", "גלר", "גרוס", "גרשון",
    "דביר", "דובדבני", "דויטש", "דוניץ", "דקל", "דרור", "האוזר", "הורוביץ", "הכט", "הנדל",
    "הררי", "וייס", "וינברג", "וינשטוק", "וינטר", "ורדי", "זוהר", "זיו", "זליג", "זלמנסון",
    "חג'אג'", "חדד", "חזן", "חייט", "חיימוביץ", "חרמון", "טבת", "טופז", "טולידנו", "טמיר",
    "יאיר", "ידידיה", "יוגב", "יוספוב", "יוסטר", "יעקובי", "יצחקי", "כהן", "כץ", "לביא",
    "לבנון", "לוין", "לוי", "ליפשיץ", "מאירי", "מגיד", "מוחמד", "מולכו", "מור", "מורד",
    "מזרחי", "מנחם", "משה", "משיח", "נבון", "נגר", "נוימן", "נחום", "ניסים", "נרקיס",
    "סביון", "סויסה", "סולומון", "סלע", "סמדג'ה", "סמואל", "עברי", "עוזרי", "עופר", "עזריה",
    "פומרנץ", "פורת", "פרידמן", "פרלמן", "פרנקו", "צדוק", "צמח", "צוקרמן", "צור", "קדוש",
    "קוגן", "קוטלר", "קול", "קורן", "קושניר", "קליין", "קלמנוביץ", "קרול", "קרני", "קשאני",
    "ראובני", "רבינוביץ", "רביבו", "רוזנברג", "רוזנטל", "רומנו", "רון", "רז", "רסלר", "שבח",
    "שדה", "שטרן", "שטיינברג", "שיינפלד", "שכטר", "שלו", "שלומוביץ", "שמאי", "שמש", "שרעבי",
    "תבור", "תדהר", "תורג'מן", "תימור"
]


WAIT = 5

class ChromeDriverManager64(ChromeDriverManager):
    def __init__(self):
        super().__init__(os_system_manager="win64")

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


URL = "https://petitions.center/he/p/diverse/"

def main():
    chrome_driver_path = ChromeDriverManager(os_system_manager=OperationSystemManager("win32")).install()

    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Open incognito window
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(URL)


    for i in range(73):
        driver.execute_script("window.scrollBy(0, 400);")
        name_bar = get_element(driver, By.ID, "Content_txtSignFullName1", clear=True)
        mail_bar = get_element(driver, By.ID, "Content_txtSignEmail1", clear=True)
        submit = get_element(driver, By.XPATH, """/html/body/form/div[3]/div[2]/section/div/div[2]/div[4]""")
        n = random.choice(names)
        l = random.choice(last_names)

        name_bar.send_keys(f"{n} {l}")
        mail_bar.send_keys(''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + "@gmail.com")

        submit.click()
        sleep(1)
        driver.get(URL)

        print(f"Signed {i}")


    driver.quit()

    print("Finished")

if __name__ == "__main__":
    main()

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import *

# used in function below, numbers represent power of 10 (6 --> 10^6)
powers = {
    "million": 6,
    "billion": 9,
    "trillion": 12,
    "quadrillion": 15,
    "quintillion": 18,
    "sextillion": 21,
    "septillion": 24,
    "octillion": 27,
}


# converts string into integer (e.g. 1.7 million cookies --> 1700000)
def numconvert(words):
    words = words.replace(",", "").replace("\n", " ")
    if len(words.split(" ")) <= 1:
        return float(words)
    if len(words.split(" ")) > 1 and words.split(" ")[1] != "cookies" and words.split(" ")[1] != "cookie":
        words = words.split(" ")
        words[1] = pow(10, powers[words[1]])
        words = float(float(words[0]) * float(words[1]))
        return words
    else:
        words = words.split(" ")
        return float(words[0])


# prevents error message popping up whenever the program is turned off
try:

    # opens Chrome and maximizes window, also makes actions more manageable by making it into a variable
    usb = input("type file location of chromedriver.exe ")
    driver = webdriver.Chrome(str(usb.upper()) + "chromedriver.exe")
    driver.maximize_window()
    actions = ActionChains(driver, 1)

    # opens Cookie Clicker
    driver.get("https://orteil.dashnet.org/cookieclicker")
    sleep(5)

    # defines clickable cookie (big cookie), amount of cookies in the bank, and golden cookies
    cookie = driver.find_element(By.ID, "bigCookie")
    banked = driver.find_element(By.ID, "cookies")
    golden = driver.find_element(By.ID, "shimmers")

    # defines each buildings' base output (how many cookies they produce, in reverse order)
    output = [
        numconvert("8.3 trillion"),
        numconvert("1.1 trillion"),
        numconvert("150 billion"),
        numconvert("21 billion"),
        numconvert("2.9 billion"),
        "430000000.0",
        "65000000.0",
        "10000000.0",
        "1600000.0",
        "260000.0",
        "44000.0",
        "7800.0",
        "1400.0",
        "260.0",
        "47.0",
        "8.0",
        "1.0",
        "0.1"
    ]

    # goes to the stats page on startup
    actions.click(driver.find_element(By.ID, "statsButton")).perform()

    while True:
        # defines the prices of all the buildings (in reverse order)
        buildingPrice = [driver.find_element(By.ID, "productPrice" + str(i)) for i in range(17, -1, -1)]

        # defines amount of buildings owned (in reverse order)
        owned = [driver.find_element(By.ID, "productOwned" + str(i)) for i in range(17, -1, -1)]

        # clicks on golden cookies
        if golden.is_displayed():
            actions.click(driver.find_element(By.CLASS_NAME, "shimmer")).perform()

        # click
        actions.click(cookie).perform()

        # checks for whether upgrades are available, then buys them if they're buy-able
        if driver.find_element(By.ID, "productOwned0").text.replace(",", "") != "":
            upgrades = driver.find_element(By.ID, "upgrade0")
            if upgrades.get_attribute("class") == "crate upgrade enabled":
                actions.click(upgrades).perform()
                sleep(0.2)
                # re-checks the output values of all buildings (since upgrades tend to change them)
                for item in range(18):
                    if buildingPrice[item].text != "" and buildingPrice[item - 1].text != "" and \
                            numconvert(banked.text) > numconvert(buildingPrice[item].text) and \
                            owned[item].text != "":
                        actions.move_to_element(buildingPrice[item]).perform()
                        output[item] = driver.find_element(By.CLASS_NAME, "data").text.split("\n")[0].split(" ")[4]
                        sleep(0.2)

        # click
        actions.click(cookie).perform()

        # for every building
        for item in range(18):
            # if they have a price (i.e. price greater than 0) and it's possible to buy
            if buildingPrice[item].text != "" and buildingPrice[item - 1].text != "" and \
                    numconvert(banked.text) > numconvert(buildingPrice[item].text):
                # if its more cost-effective (cookie production divided by price) to buy this building
                # compared to buying the previous building
                if numconvert(buildingPrice[item - 1].text) / numconvert(buildingPrice[item].text) > \
                            (numconvert(output[item - 1]) + 0.001) / (numconvert(output[item]) + 0.001):
                    # buy a building
                    actions.click(buildingPrice[item]).perform()
                    # re-checks building output whenever a building is bought,
                    # skips this step in case the element can't be found
                    if owned[item].text != "" and numconvert(owned[item].text) > 1:
                        actions.move_to_element(buildingPrice[item]).perform()
                        try:
                            output[item] = driver.find_element(By.CLASS_NAME, "data").text.split("\n")[0].split(" ")[4]
                            sleep(0.2)
                        except StaleElementReferenceException:
                            pass

        # click
        actions.click(cookie).perform()

# program closed
except KeyboardInterrupt:
    print("turned off bot")
# browser closed
except NoSuchWindowException or WebDriverException:
    print("window closed")

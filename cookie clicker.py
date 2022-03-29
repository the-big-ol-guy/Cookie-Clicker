from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import *

driver = webdriver.Chrome("E:\chromedriver.exe")
driver.maximize_window()
actions = ActionChains(driver)

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
    # opens Cookie Clicker
    driver.get("https://orteil.dashnet.org/cookieclicker")
    driver.implicitly_wait(10)

    # defines clickable cookie (big cookie), amount of cookies in the bank, and golden cookies
    cookie = driver.find_element(By.ID, "bigCookie")
    banked = driver.find_element(By.ID, "cookies")
    golden = driver.find_element(By.ID, "shimmers")
    # defines each buildings' base output (from most powerful to least)
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

    while True:
        # defines the prices of all the buildings (from most powerful to least)
        buildingPrice = [driver.find_element(By.ID, "productPrice" + str(i)) for i in range(17, -1, -1)]

        # clicks on golden cookies
        if golden.is_displayed():
            actions.click(driver.find_element(By.CLASS_NAME, "shimmer")).perform()

        actions.click(cookie).perform()

        # checks for whether upgrades are available, then buys them if they're buy-able
        if driver.find_element(By.ID, "productOwned0").text.replace(",", "") != "":
            upgrades = driver.find_element(By.ID, "upgrade0")
            if upgrades.get_attribute("class") == "crate upgrade enabled":
                actions.click(upgrades).perform()
                sleep(0.1)

        actions.click(cookie).perform()

        for item in range(18):
            # if they have a price (i.e. price greater than 0)
            if buildingPrice[item].text != "" and buildingPrice[item - 1].text != "":
                # if it's possible to buy it (i.e. if you have enough cookies to buy it)
                if numconvert(banked.text) > numconvert(buildingPrice[item].text):
                    # don't even know how to explain this one
                    if numconvert(buildingPrice[item - 1].text) / (numconvert(output[item - 1]) + 0.001) > \
                            numconvert(buildingPrice[item].text) / (numconvert(output[item]) + 0.001):
                        pass
                    else:
                        actions.click(buildingPrice[item]).perform()
                        actions.move_to_element(buildingPrice[item]).perform()
                        sleep(0.2)
                        try:
                            output[item] = driver.find_element(By.CLASS_NAME, "data").text.split("\n")[0].split(" ")[4]
                            sleep(0.2)
                        except StaleElementReferenceException:
                            pass

        actions.click(cookie).perform()

except KeyboardInterrupt:
    print("ended early")
